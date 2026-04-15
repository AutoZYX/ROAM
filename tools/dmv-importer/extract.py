#!/usr/bin/env python3
"""
DMV OL 316 PDF → ROAM Tier 2 YAML converter.

Parses California DMV autonomous vehicle collision reports (Form OL 316)
and converts them into ROAM-compatible YAML records with tier: 2.

Usage:
    python extract.py --pdf-dir pdfs/ --output-dir ../../incidents/dmv/
"""
import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path


OPERATOR_MAP = {
    "waymo": "Waymo",
    "zoox": "Zoox",
    "cruise": "Cruise (GM)",
    "gm cruise": "Cruise (GM)",
    "general motors": "Cruise (GM)",
    "apple": "Apple",
    "nuro": "Nuro",
    "weride": "WeRide",
    "pony": "Pony.ai",
    "apollo": "Apollo (Baidu)",
    "baidu": "Apollo (Baidu)",
    "mercedes": "Mercedes-Benz",
    "lyft": "Lyft",
    "aimotive": "AImotive",
    "argo": "Argo AI",
    "aurora": "Aurora",
    "may mobility": "May Mobility",
    "beep": "Beep",
    "ohmio": "Ohmio",
    "tensor": "Tensor",
    "gatik": "Gatik",
    "motional": "Motional",
    "toyota": "Toyota Research",
    "nvidia": "NVIDIA",
    "udelv": "Udelv",
    "ghost": "Ghost Autonomy",
    "phantom": "Phantom AI",
    "embark": "Embark",
    "plus": "Plus",
    "tusimple": "TuSimple",
    "kodiak": "Kodiak",
    "applied intuition": "Applied Intuition",
    "imagry": "Imagry",
    "qualcomm": "Qualcomm",
    "valeo": "Valeo",
    "bosch": "Bosch",
    "continental": "Continental",
    "mobileye": "Mobileye",
}


def parse_operator_from_text(text: str) -> str | None:
    """Extract MANUFACTURER'S NAME from Section 1 of the PDF text."""
    # Match: "MANUFACTURER'S NAME ... AVT NUMBER\n <name>"
    # The name is the line after the "MANUFACTURER'S NAME" header.
    # PDF text uses both ' and ' (curly and straight).
    m = re.search(
        r"MANUFACTURER[\u2019']S NAME[^\n]*\n\s*([^\n]+?)\s*\n",
        text,
    )
    if not m:
        return None
    raw = m.group(1).strip()
    # Clean up common suffixes
    cleaned = re.sub(r",?\s*(LLC|Inc\.?|Corp\.?|Corporation|Ltd\.?|Company|Co\.?)$", "", raw, flags=re.IGNORECASE).strip()
    if not cleaned:
        return None
    # Match against known operators
    lower = cleaned.lower()
    for key, name in OPERATOR_MAP.items():
        if key in lower:
            return name
    # Unknown operator — return cleaned raw name, not "Unknown"
    return cleaned


def pdftotext(pdf_path: Path) -> str:
    """Extract text from PDF using pdftotext -layout."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, check=True
    )
    return result.stdout


def parse_operator(filename: str, text: str = "") -> str:
    """Prefer PDF content (Section 1 MANUFACTURER'S NAME), fall back to filename."""
    if text:
        from_text = parse_operator_from_text(text)
        if from_text:
            return from_text

    stem = filename.lower().replace("_redacted", "").replace("-pdf", "")
    for key, name in OPERATOR_MAP.items():
        if stem.startswith(key) or f"-{key}-" in stem or f"_{key}_" in stem:
            return name
    return "Unknown"


def parse_date(filename: str, text: str) -> str:
    """Extract ISO date from form field (most reliable), then narrative, then filename."""
    # Best: form field "DATE OF ACCIDENT\n01/12/2024"
    m = re.search(
        r'DATE OF ACCIDENT[^\n]*\n\s*(\d{1,2})/(\d{1,2})/(\d{4})',
        text
    )
    if m:
        mm, dd, yyyy = m.groups()
        yyyy_int = int(yyyy)
        if 2010 <= yyyy_int <= 2030:
            return f"{yyyy}-{int(mm):02d}-{int(dd):02d}"

    # Narrative: "On April 1, 2026" or "On 03/30/2026"
    m = re.search(
        r'On\s+(?:(\d{1,2})/(\d{1,2})/(\d{4})|'
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4}))',
        text
    )
    if m:
        if m.group(1):
            mm, dd, yyyy = m.group(1), m.group(2), m.group(3)
            return f"{yyyy}-{int(mm):02d}-{int(dd):02d}"
        else:
            months = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            return f"{m.group(6)}-{months[m.group(4)]:02d}-{int(m.group(5)):02d}"

    # Last resort: filename (e.g., waymo_040126 = 04/01/26)
    # Only use 6-digit compact format, reject if adjacent to other digits
    m = re.search(r'_(\d{6})(?!\d)', filename)
    if m:
        mmddyy = m.group(1)
        mm, dd, yy = int(mmddyy[:2]), int(mmddyy[2:4]), int(mmddyy[4:6])
        year = 2000 + yy if yy < 50 else 1900 + yy
        if 1 <= mm <= 12 and 1 <= dd <= 31 and year >= 2014:
            return f"{year}-{mm:02d}-{dd:02d}"

    return "UNKNOWN"


def parse_time(text: str) -> str:
    """Extract HH:MM time from narrative."""
    m = re.search(r'at\s+(\d{1,2}):(\d{2})\s*(?:AM|PM|a\.m\.|p\.m\.)?\s*(?:PT|PST|PDT)?', text, re.IGNORECASE)
    if m:
        h, mm = int(m.group(1)), m.group(2)
        # Check AM/PM context
        after = text[m.end():m.end()+20]
        if re.search(r'PM|p\.m\.', after, re.IGNORECASE) and h < 12:
            h += 12
        elif re.search(r'AM|a\.m\.', after, re.IGNORECASE) and h == 12:
            h = 0
        return f"{h:02d}:{mm}"
    return None


def parse_location(full_text: str, narrative: str) -> dict:
    """Extract city, specific address from form fields or narrative."""
    # Try form fields first (Section 2 has CITY, COUNTY, STATE, ZIP)
    # Format: "Electric Avenue near Milwood Avenue     Venice            Los Angeles   CA    90291"
    loc_match = re.search(
        r'ADDRESS/LOCATION OF ACCIDENT.*?\n\s*([^\n]+?)\s{3,}([A-Z][a-zA-Z\s.]*?)\s{3,}([A-Z][a-zA-Z\s.]*?)\s+(CA)\s+(\d{5})',
        full_text, re.IGNORECASE
    )
    if loc_match:
        address = loc_match.group(1).strip()
        city = loc_match.group(2).strip()
        return {
            "city": f"{city}, USA",
            "country": "USA",
            "road_type": "urban_street",
            "specific": address[:120],
        }

    # Fallback: narrative parsing
    city_match = re.search(
        r'(?:operating in|in)\s+([A-Z][a-zA-Z\s.]+?),?\s+(?:California|CA)\b',
        narrative
    )
    city = city_match.group(1).strip() if city_match else "California"

    specific_match = re.search(r'on\s+([A-Z][^.]{5,80}?)(?:\.|(?:\s+(?:in|near|when|while)))', narrative[:500])
    specific = specific_match.group(1).strip()[:120] if specific_match else None

    return {
        "city": f"{city}, USA",
        "country": "USA",
        "road_type": "urban_street",
        "specific": specific,
    }


def extract_narrative(text: str) -> str:
    """Extract Section 5 narrative."""
    m = re.search(
        r'(?:Autonomous Mode|Conventional Mode)\s*\n(.*?)(?:Additional information attached|ITEMS MARKED BELOW)',
        text, re.DOTALL
    )
    if m:
        narrative = m.group(1).strip()
        # Clean up: collapse multiple spaces, remove leading checkbox text
        narrative = re.sub(r'[ \t]+', ' ', narrative)
        narrative = re.sub(r'\n\s*\n', '\n\n', narrative)
        return narrative
    return ""


def is_autonomous(narrative: str) -> bool:
    """Determine if vehicle was in autonomous mode at time of collision.

    Filter out incidents where the operator explicitly notes conventional/manual mode.
    These are NOT autonomy failures and shouldn't dilute the dataset.
    """
    n = narrative.lower()
    # Strong negative signals
    manual_patterns = [
        "in manual mode",
        "operating in manual",
        "in conventional mode",
        "was in manual mode",
        "was driving manually",
        "test driver was operating",
        "manually operated",
        "under manual control",
    ]
    for p in manual_patterns:
        if p in n:
            return False
    return True


def classify_scenario(narrative: str) -> dict:
    """Map narrative to ROAM taxonomy scenario code."""
    n = narrative.lower()

    # Pedestrian/cyclist collision
    if re.search(r'\bpedestrian\b|\bbicycl(?:e|ist)\b|\bcyclist\b|\bscooter\b', n):
        if "struck" in n or "hit" in n or "contact" in n or "collision" in n:
            return {"primary": "C5", "secondary": []}

    # Rear end
    if "rear-end" in n or "rear end" in n:
        # If AV was rear-ended while stopped, it's E1 (struck by other vehicle)
        if "av was stopped" in n or "av stopped" in n or "av was stationary" in n or "vehicle 1 was stopped" in n:
            return {"primary": "E1", "secondary": []}
        # AV rear-ended another vehicle (rare)
        return {"primary": "C2", "secondary": []}

    # Side swipe
    if "side" in n and ("swipe" in n or "contact" in n):
        if "av was stopped" in n or "stationary" in n or "parked" in n:
            return {"primary": "E1", "secondary": []}
        return {"primary": "C3", "secondary": []}

    # Struck while stopped/parked
    if ("stopped" in n or "stationary" in n) and ("struck" in n or "contact" in n or "collision" in n):
        return {"primary": "E1", "secondary": []}

    # Hit parked vehicle / static object
    if "parked" in n and ("contact" in n or "hit" in n) and ("av" in n or "vehicle 1" in n):
        return {"primary": "C4", "secondary": []}

    # Emergency vehicle
    if "ambulance" in n or "fire truck" in n or "emergency" in n:
        return {"primary": "E3", "secondary": []}

    # Construction
    if "construction" in n or "work zone" in n or "cone" in n:
        return {"primary": "E2", "secondary": []}

    # Head-on / opposing lane
    if "head-on" in n or "opposing" in n:
        return {"primary": "E1", "secondary": []}

    # Default: external conflict
    return {"primary": "E1", "secondary": []}


def parse_severity(narrative: str) -> str:
    """Map to S0-S4 based on injuries and damage."""
    n = narrative.lower()

    if "fatal" in n or "deceased" in n or "killed" in n:
        return "S4"
    if "hospital" in n or "serious injur" in n or "major injur" in n or "severe injur" in n:
        return "S3"
    if "injur" in n or "taken to" in n or "ambulance transported" in n or "complained of" in n:
        return "S2"
    if "damage" in n or "contact" in n or "minor" in n:
        return "S1"
    return "S0"  # No visible damage or injury


def to_yaml(record: dict) -> str:
    """Generate YAML manually to preserve field order and readability."""
    lines = [f'id: "{record["id"]}"']
    lines.append(f'tier: {record["tier"]}')
    lines.append(f'date: "{record["date"]}"')
    if record.get("time"):
        lines.append(f'time: "{record["time"]}"')
    lines.append(f'operator: "{record["operator"]}"')
    if record.get("vehicle_model"):
        lines.append(f'vehicle_model: "{record["vehicle_model"]}"')

    loc = record["location"]
    lines.append("location:")
    lines.append(f'  city: "{loc["city"]}"')
    if loc.get("country"):
        lines.append(f'  country: "{loc["country"]}"')
    if loc.get("road_type"):
        lines.append(f'  road_type: "{loc["road_type"]}"')
    if loc.get("specific"):
        specific = loc["specific"].replace('"', "'")
        lines.append(f'  specific: "{specific}"')

    sc = record["scenario"]
    lines.append("scenario:")
    lines.append(f'  primary: "{sc["primary"]}"')
    if sc.get("secondary"):
        sec = ", ".join(f'"{s}"' for s in sc["secondary"])
        lines.append(f'  secondary: [{sec}]')

    lines.append(f'severity: "{record["severity"]}"')
    if record.get("urgency"):
        lines.append(f'urgency: "{record["urgency"]}"')

    # Description with literal block scalar
    desc = record["description"].strip()
    lines.append("description: |")
    for l in desc.split("\n"):
        lines.append(f"  {l}")

    if record.get("sources"):
        lines.append("sources:")
        for src in record["sources"]:
            lines.append(f'  - url: "{src["url"]}"')
            lines.append(f'    title: "{src["title"]}"')

    lines.append(f'contributor: "CA DMV OL 316 (auto-imported)"')
    lines.append(f'last_updated: "{datetime.now().strftime("%Y-%m-%d")}"')

    return "\n".join(lines) + "\n"


def process_pdf(pdf_path: Path, id_counter: dict) -> tuple[str, dict]:
    """Extract a single PDF and return (year, record dict)."""
    text = pdftotext(pdf_path)
    narrative = extract_narrative(text)

    if not narrative:
        return None, None

    # Skip if vehicle was in manual/conventional mode
    if not is_autonomous(narrative):
        return "MANUAL", None

    operator = parse_operator(pdf_path.stem, text)
    date = parse_date(pdf_path.stem, text)
    time = parse_time(narrative)
    location = parse_location(text, narrative)
    scenario = classify_scenario(narrative)
    severity = parse_severity(narrative)

    if date == "UNKNOWN":
        return None, None

    year = date[:4]
    id_counter[year] = id_counter.get(year, 0) + 1
    record_id = f"ROAM-DMV-{year}-{id_counter[year]:03d}"

    # URL reconstruction
    pdf_slug = pdf_path.stem
    source_url = f"https://www.dmv.ca.gov/portal/file/{pdf_slug}-pdf/"

    record = {
        "id": record_id,
        "tier": 2,
        "date": date,
        "time": time,
        "operator": operator,
        "location": location,
        "scenario": scenario,
        "severity": severity,
        "urgency": "U0",
        "description": narrative,
        "sources": [{
            "url": source_url,
            "title": f"{operator} collision report {date} (CA DMV OL 316)"
        }]
    }

    return year, record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", default="pdfs", help="Directory containing DMV PDFs")
    ap.add_argument("--output-dir", default="output", help="Output YAML directory")
    args = ap.parse_args()

    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    id_counter = {}
    success = 0
    skipped_manual = 0
    skipped_other = 0

    for pdf_path in sorted(pdf_dir.glob("*.pdf")):
        try:
            year, record = process_pdf(pdf_path, id_counter)
            if year == "MANUAL":
                skipped_manual += 1
                continue
            if not record:
                skipped_other += 1
                continue

            year_dir = out_dir / year
            year_dir.mkdir(exist_ok=True)

            yaml_path = year_dir / f"{record['id']}-{pdf_path.stem}.yaml"
            yaml_path.write_text(to_yaml(record))
            success += 1
        except Exception as e:
            print(f"ERROR {pdf_path.name}: {e}")
            skipped_other += 1

    print(f"\n{success} extracted, {skipped_manual} skipped (manual mode), {skipped_other} other skips")


if __name__ == "__main__":
    main()
