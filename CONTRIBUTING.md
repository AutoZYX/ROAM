# Contributing to ROAM

Thank you for your interest in contributing to ROAM (RoboTaxi Operations Anomaly Management). This project aims to build the open-source foundation for robotaxi remote operations safety, and community contributions are essential to that mission.

---

## Ways to Contribute

### 1. Submit a New Incident

The most valuable contribution is a well-documented incident report. Every public robotaxi anomaly should be captured in our database.

#### YAML Format

Each incident is a YAML file following the schema defined in `incidents/schema.json`. Place files in `incidents/YYYY/` using the naming convention:

```
ROAM-YYYY-NNN-operator-city-brief-description.yaml
```

#### Required Fields

```yaml
id: "ROAM-YYYY-NNN"           # Unique ID (request next available number in your PR)
date: "YYYY-MM-DD"            # Date of incident
operator: "Company Name"       # Operating company
location:
  city: "City, Country"
  road_type: "urban_street"    # See schema.json for valid values
scenario:
  primary: "C1"                # Primary taxonomy code (see taxonomy/)
severity: "S2"                 # S0-S4 (see taxonomy/severity-scale.md)
description: |
  Clear, factual description of what happened.
  Include timeline, vehicles affected, and resolution.
sources:
  - url: "https://..."
    title: "Source Title"
contributor: "Your Name or GitHub handle"
last_updated: "YYYY-MM-DD"
```

#### Optional but Encouraged Fields

```yaml
time: "HH:MM"                 # Local time of incident
vehicle_model: "Model Name"
urgency: "U2"                 # U0-U3 (see taxonomy/urgency-scale.md)
impact:
  vehicles_affected: 1
  duration_minutes: 15
  traffic_disruption: "moderate"  # none/minor/moderate/severe/critical
  injuries: 0
  fatalities: 0
emergency_response:
  sos_button: "functional"     # functional/non_functional/delayed/not_applicable
  customer_service: "responsive"  # responsive/delayed/overloaded/unavailable
  remote_intervention: "successful"  # none/attempted/successful/partial
  on_site_response: "none"     # none/company_team/police_manual/tow_truck/fire_department/ambulance
  resolution_method: "Brief description of how it was resolved"
root_cause:
  category: "Brief category"
  description: "What caused this incident"
  confirmed: false             # true only if officially confirmed by operator/regulator
systemic_issues:
  - "Broader systemic issue this incident reveals"
regulatory_action: "Any regulatory response"
```

#### Submission Checklist

- [ ] YAML file validates against `incidents/schema.json`
- [ ] At least one source URL is provided (news article, regulatory filing, social media post)
- [ ] Description is factual and neutral (no editorializing)
- [ ] Scenario code(s) match the taxonomy in `taxonomy/scenario-taxonomy-v1.0.md`
- [ ] Severity score follows `taxonomy/severity-scale.md`
- [ ] No personally identifiable information (names of victims, bystanders, etc.)
- [ ] File is placed in the correct `incidents/YYYY/` directory

### 2. Improve the Taxonomy

The scenario taxonomy is a living document. We welcome proposals to:

- **Add a new sub-scenario**: If you identify a robotaxi anomaly type not covered by the existing A1-F4 codes
- **Refine an existing scenario**: Improve the description, add examples, or adjust the recommended layer
- **Propose a new category**: If the existing 6 categories (A-F) cannot accommodate a fundamentally new type

#### How to Propose Taxonomy Changes

1. Open an issue with the title: `[Taxonomy] Proposal: <brief description>`
2. Include:
   - Proposed scenario ID and name (EN/CN)
   - Description and real-world examples
   - Justification for why the current taxonomy does not cover this
   - Recommended response layer with reasoning
3. The core team will review and discuss in the issue thread
4. If accepted, submit a PR modifying `taxonomy/scenario-taxonomy-v1.0.md`

### 3. Contribute to the Reference Architecture

The reference architecture benefits from real-world operational experience. Contributions may include:

- **Operational insights**: Lessons learned from deploying remote operations platforms
- **API design improvements**: Better endpoint definitions, message formats, or interaction patterns
- **Scaling data**: Real-world operator-to-vehicle ratios, latency measurements, or throughput data
- **Alternative architectures**: Different approaches that worked in specific contexts

#### Guidelines

- The reference architecture is intentionally a starting point, not a prescription
- Contributions should be generalizable (not specific to one vendor's proprietary system)
- Include evidence or reasoning for proposed changes (not just opinions)
- Respect confidentiality: do not share proprietary information from your employer

### 4. Contribute Benchmark Data

Help the industry establish baselines by contributing:

- **Anonymized KPI data**: MTTR, resolution rates, escalation rates from real deployments
- **Simulation results**: Scenario coverage test results from your simulation platform
- **Comparative analysis**: Studies comparing different approaches to the same scenarios

Place benchmark data in `benchmarks/baseline-data/` with clear documentation of methodology and context.

---

## Submission Process

### For All Contributions

1. **Fork** the repository
2. **Create a branch** with a descriptive name:
   - `incident/ROAM-2026-015-waymo-chicago-freeze`
   - `taxonomy/add-v2x-failure-scenario`
   - `architecture/improve-layer2-escalation-flow`
3. **Make your changes** following the guidelines above
4. **Submit a Pull Request** with:
   - Clear title describing the contribution
   - Description of what was added/changed and why
   - References to any related issues
5. **Respond to review feedback** from the core team

### Review Process

- Incident submissions are typically reviewed within 1 week
- Taxonomy and architecture changes require at least 2 core team members to approve
- We may ask for additional sources, clarification, or modifications
- All contributions must pass schema validation (for incident YAML files)

---

## Code of Conduct

### Our Standards

- **Be respectful and constructive.** This project involves sensitive topics (traffic safety, injuries, fatalities). Treat all incidents and the people involved with appropriate gravity.
- **Be factual.** Incident reports must be based on verifiable sources. Do not speculate about root causes without evidence. Clearly distinguish confirmed facts from analysis.
- **Be inclusive.** We welcome contributors from all backgrounds, organizations, and countries. Contributions in English or Chinese are both accepted.
- **No vendor bashing.** The purpose of ROAM is to improve the industry, not to attack specific companies. Report facts, not opinions about corporate competence.
- **Respect confidentiality.** Do not share proprietary information, trade secrets, or non-public data from your employer or business partners.

### Unacceptable Behavior

- Publishing personally identifiable information of accident victims or witnesses
- Deliberately misrepresenting incident facts or fabricating data
- Using the incident database for competitive intelligence attacks against specific operators
- Harassment, trolling, or personal attacks against other contributors

### Enforcement

Violations of this code of conduct may result in:
1. Comment or contribution removal
2. Temporary or permanent ban from the project
3. Reporting to GitHub for Terms of Service violations

Report concerns to the core team via email or by opening a confidential issue.

---

## Issue Templates

The repository includes the following issue templates in `.github/ISSUE_TEMPLATE/`:

| Template | Purpose | When to Use |
|----------|---------|-------------|
| `new-incident.md` | Report a new robotaxi incident | You found a public report of an AV anomaly not yet in the database |
| `taxonomy-proposal.md` | Propose taxonomy change | You want to add, modify, or restructure scenario codes |
| `architecture-feedback.md` | Reference architecture feedback | You have operational experience that could improve the architecture |
| `benchmark-submission.md` | Submit benchmark data | You have KPI data or simulation results to share |
| `bug-report.md` | Report a bug | Schema validation error, broken link, factual error in existing data |

---

## Questions?

- Open a GitHub Discussion for general questions
- Tag `@roam-core-team` in issues for questions about contribution guidelines
- See the [README](README.md) for project overview and quick start

---

## License

By contributing to ROAM, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
