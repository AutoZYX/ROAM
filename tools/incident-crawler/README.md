# ROAM Incident Crawler

Automated collection system for L4+ robotaxi operational incidents from public sources worldwide.

## Purpose

The ROAM project relies on a structured database of real-world robotaxi incidents to enable evidence-based safety research, regulatory analysis, and insurance actuarial work. Manually monitoring dozens of news sources across multiple languages is impractical at scale. This crawler automates incident discovery, performs LLM-based structured extraction, and generates ROAM-format YAML files ready for human review.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Incident Crawler Pipeline                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │  Sources │───▶│ Crawlers │───▶│Raw Items │             │
│  │  (YAML)  │    │(RSS/API/ │    │  (JSON)  │             │
│  │          │    │   HTML)  │    │          │             │
│  └──────────┘    └──────────┘    └──────────┘             │
│                                        │                    │
│                                        ▼                    │
│                                 ┌──────────────┐           │
│                                 │LLM Extractor │           │
│                                 │   (Claude)   │           │
│                                 └──────┬───────┘           │
│                                        │                    │
│                                        ▼                    │
│                                 ┌──────────────┐           │
│                                 │ YAML Output  │           │
│                                 │(ROAM Schema) │           │
│                                 └──────┬───────┘           │
│                                        │                    │
│                                        ▼                    │
│                                 ┌──────────────┐           │
│                                 │ Human Review │           │
│                                 │  (via PR)    │           │
│                                 └──────┬───────┘           │
│                                        │                    │
│                                        ▼                    │
│                                 ┌──────────────┐           │
│                                 │ ROAM Database│           │
│                                 └──────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Data Sources (Tiered)

### S-Tier: Official Incident Databases
Highest quality, structured, regulator-verified:
- **NHTSA Standing General Order database** - US federal incident reporting
- **OECD.AI Incidents Database** - curated international incidents

### A-Tier: Established News Outlets
English: TechCrunch, CNBC, Reuters, NBC News, SF Standard, Autoblog, Futurism
Chinese: 虎嗅网, 36kr, 光明网, 新浪汽车, 澎湃新闻

### B-Tier: Community Sources
- Reddit r/SelfDrivingCars
- Twitter/X keyword monitoring

## LLM Extraction Pipeline

Raw article text is passed to Claude via a structured prompt that:
1. Extracts required ROAM schema fields
2. Maps natural language descriptions to scenario codes (27 sub-scenarios)
3. Assigns severity (S0-S4) and urgency (U0-U3) ratings
4. Flags uncertain fields with REVIEW_NEEDED markers
5. Outputs strict YAML matching `incidents/schema.json`

The extractor is **conservative by design**: it flags uncertainty rather than fabricating values. Every output requires human review before merging to the main database.

## Deployment Options

### Local Development
```bash
cd tools/incident-crawler
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python crawler.py --source nhtsa --days 7
python extractor.py --input raw_incidents/2026-04-05/nhtsa/incident_001.json
```

### GitHub Actions (Production)
The workflow in `.github/workflows/daily-crawl.yml` runs daily at 02:00 UTC:
1. Crawls all configured sources
2. Runs LLM extraction on new items
3. Opens a PR with new YAML files for human review

### Cron (Self-Hosted)
```cron
0 2 * * * cd /path/to/ROAM/tools/incident-crawler && python crawler.py --all
```

## Human Review Workflow

See `review-workflow.md` for complete reviewer guidelines. Key principles:
- Every URL must be accessible (verify before merging)
- Scenario classification requires domain knowledge
- Severity/urgency assignment follows explicit criteria
- Cross-reference with existing incidents for deduplication

## Contribution

1. **Add a new source**: Edit `config/sources.yaml`, no code changes needed
2. **Refine keywords**: Edit `config/keywords.yaml`
3. **Improve extraction**: Edit `prompts/extraction-prompt.md`
4. **Fix bugs**: Submit PR against `crawler.py` or `extractor.py`

## Design Principles

- **Privacy**: No paywalled content scraping, respect robots.txt
- **Conservatism**: LLM flags uncertainty, never fabricates values
- **Reproducibility**: Every incident has verifiable source URL
- **Scalability**: New sources added via YAML config without code changes
- **Multilingual**: Chinese and English sources native-supported

## License

Apache 2.0 (same as ROAM main project)
