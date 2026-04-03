# ROAM — RoboTaxi Operations Anomaly Management

**Open-Source Incident Database, Scenario Taxonomy & Reference Architecture for L4+ Robotaxi Remote Operations**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Incidents](https://img.shields.io/badge/Incidents-16-red.svg)](#incident-database)
[![Scenarios](https://img.shields.io/badge/Scenarios-6%20categories-orange.svg)](#scenario-taxonomy)

🌐 **Website:** [AutoZYX.github.io/ROAM](https://AutoZYX.github.io/ROAM)

---

## Why ROAM?

On March 31, 2026, nearly 100 Baidu Apollo robotaxis simultaneously shut down on elevated highways in Wuhan, China. Passengers were trapped for 2 hours. SOS buttons went unanswered. The only resolution? **Police officers manually rescuing vehicles one by one.**

Three months earlier, a power outage in San Francisco left Waymo vehicles stranded across the city. Emergency services called Waymo's hotline 31 times, waiting a combined 2.5 hours.

These aren't edge cases — they're previews of what happens when L4 robotaxi fleets scale without adequate remote operations infrastructure.

**ROAM provides the open-source foundation for solving this problem:**

1. 📋 **Incident Database** — Structured, searchable records of every known robotaxi anomaly
2. 🏷️ **Scenario Taxonomy** — 6 categories, 20+ sub-scenarios for classifying operational anomalies
3. 🏗️ **Reference Architecture** — Three-layer decision model for AI-first remote operations
4. 📊 **Evaluation Benchmarks** — KPIs and baseline data for measuring platform performance

## Who Is This For?

| Audience | Value |
|----------|-------|
| **Robotaxi Operators** (Baidu, Pony.ai, WeRide) | Reference architecture for building remote ops platforms |
| **OEMs** (SAIC, FAW, Changan) | Scenario database for L4 service planning |
| **Startups** building teleops solutions | Open baseline to build upon, not from scratch |
| **Regulators & Standards Bodies** | Evidence-based incident data for policy development |
| **Researchers** | Structured dataset for autonomous vehicle safety research |

## Quick Start

### Browse Incidents

Each incident is a YAML file in `incidents/YYYY/`:

```bash
ls incidents/2026/
# ROAM-2026-001-waymo-santa-monica-child.yaml
# ROAM-2026-002-waymo-austin-ambulance.yaml
# ROAM-2026-003-waymo-sf-two-vehicle-collision.yaml
# ROAM-2026-004-apollo-wuhan-mass-shutdown.yaml
# ...
```

### Understand the Taxonomy

See [`taxonomy/scenario-taxonomy-v1.0.md`](taxonomy/scenario-taxonomy-v1.0.md) for the full classification:

```
A. System-Wide Failure          (系统性故障)
B. Perception/Decision Failure  (感知/决策失效)
C. Planning/Execution Anomaly   (规划/执行异常)
D. Vehicle Hardware Failure     (车辆硬件故障)
E. External Conflict            (外部环境冲突)
F. Passenger-Side Issue         (乘客端异常)
```

### Reference Architecture

See [`architecture/reference-architecture.md`](architecture/reference-architecture.md) for the three-layer decision model:

```
Layer 1: AI Autonomous Response     (target: 70% of anomalies)
Layer 2: AI-Assisted + Human Confirm (target: 25%)
Layer 3: Remote Driving / On-Site    (target: 5%)
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**How to contribute:**
- 🐛 **Report an incident**: Use the [incident template](.github/ISSUE_TEMPLATE/new-incident.md)
- 📝 **Improve documentation**: Submit a PR
- 🔬 **Add analysis**: Contribute root cause analysis or scenario mapping
- 📊 **Share data**: Contribute baseline data or evaluation results

## Project Structure

```
ROAM/
├── incidents/          # Incident database (YAML files)
├── taxonomy/           # Scenario classification system
├── architecture/       # Reference architecture & API specs
├── benchmarks/         # KPIs and baseline data
├── website/            # GitHub Pages website
└── docs/               # White papers and research
```

## Supported By

- **Jilin University AD Safety Joint Lab** (吉林大学自动驾驶安全联合实验室) — Scenario taxonomy, SOTIF methodology, academic research
- **DRIVEResearch** (驭研科技) — Naturalistic driving baseline data (750h+ aerial UAV, 10.5M+ trajectories)

## Related Standards

| Standard | Full Title | Relevance to ROAM |
|----------|-----------|-------------------|
| GB XXXXX—XXXX | 智能网联汽车 自动驾驶系统安全要求 (Draft, 2026-02) | Appendix C.2 defines L4 remote assistance requirements; Appendix D defines Safety Case structure |
| UN GTR on ADS | GRVA draft GTR (ECE-TRANS-WP.29-GRVA-2026-02e) | Global safety baseline: "competent and careful human driver" standard |
| ISO 34502 | Road vehicles — Test scenarios for automated driving systems (2022) | Scenario taxonomy alignment — functional, logical, and concrete scenario layers |
| ISO 21448 | Road vehicles — Safety of the intended functionality / SOTIF (2022) | SOTIF methodology for identifying unknown unsafe scenarios and triggering conditions |
| ISO 26262 | Road vehicles — Functional safety (2018, 2nd ed.) | Functional safety framework, ASIL classification, safety analysis methods |
| ISO 22737 | Low-speed automated driving systems — Predefined routes (2021) | L4 shuttle operations, includes "driverless operation dispatcher" (DOD) role |
| ISO/PAS 8800 | Road vehicles — Safety and artificial intelligence (2024) | AI safety lifecycle for ADS perception and decision components |
| SAE J3016 | Taxonomy and Definitions for Driving Automation Systems (Rev. May 2024) | Level definitions, remote support terminology (remote driving, remote assistance) |
| UK AV Act 2024 | Automated Vehicles Act 2024 | ASDE concept (legal responsibility entity), NUIC operation mode |
| German StVFernLV | Straßenverkehr-Fernlenk-Verordnung (Dec 2025) | Europe's first teleoperated driving legal framework |
| NHTSA SGO | Standing General Order on Crash Reporting (2021, amended 2024) | ADS crash reporting requirements and data elements |
| CSAE 316.1/316.2 | 智能网联汽车 环境感知系统预期功能安全 (2023) | SOTIF triggering condition analysis for perception systems |
| CSAE 336 | 智能网联汽车预期功能安全场景要素及管理要求 (2024) | Scenario element framework and management requirements |

> For detailed standard-to-module mapping, see [`docs/related-standards.md`](docs/related-standards.md).
> 中文对齐分析见 [`docs/standard-alignment-cn.md`](docs/standard-alignment-cn.md).

## Regulatory Alignment

ROAM is designed to support compliance efforts across multiple regulatory jurisdictions. Three regulatory frameworks are of particular relevance:

**China GB ADS Safety Requirements (Appendix C.2 — Remote Assistance)**
The draft GB standard's Appendix C.2 defines functional requirements for L4 remote assistance, including communication latency thresholds, operator qualification, and fallback procedures. ROAM's three-layer architecture (AI Autonomous / AI-Assisted + Human / Remote Driving) directly maps to the GB standard's graduated remote intervention model. ROAM's Incident Database provides the operational evidence required for the Safety Case (安全档案) structure defined in Appendix D.

**WP.29 GTR Safety Case Requirements**
The GRVA draft Global Technical Regulation requires manufacturers to demonstrate that their ADS performs at least as safely as a "competent and careful human driver." ROAM's Benchmarks module provides quantitative KPIs (response time, resolution rate, escalation frequency) that support this demonstration. ROAM's Incident Database offers structured records that feed into the evidence base of manufacturer safety cases.

**Germany StVFernLV Teleoperation Framework**
Germany's Road Traffic Remote Driving Ordinance (December 2025) is Europe's first comprehensive legal framework for teleoperated driving. It specifies operator training requirements, communication infrastructure standards, and operational constraints. ROAM's Architecture Layer 3 (Remote Driving / On-Site) aligns with these requirements, and ROAM's Benchmarks include communication performance KPIs that map to StVFernLV's minimum bandwidth and latency mandates.

## License

Apache License 2.0 — free for commercial use, modification, and distribution.

## Citation

If you use ROAM in your research, please cite:

```bibtex
@misc{roam2026,
  title={ROAM: RoboTaxi Operations Anomaly Management},
  author={Zhang, Yuxin and Contributors},
  year={2026},
  url={https://github.com/AutoZYX/ROAM}
}
```
