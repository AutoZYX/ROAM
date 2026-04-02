# ROAM — RoboTaxi Operations Anomaly Management

**Open-Source Incident Database, Scenario Taxonomy & Reference Architecture for L4+ Robotaxi Remote Operations**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Incidents](https://img.shields.io/badge/Incidents-16-red.svg)](#incident-database)
[![Scenarios](https://img.shields.io/badge/Scenarios-6%20categories-orange.svg)](#scenario-taxonomy)

🌐 **Website:** [roam-robotaxi.github.io](https://roam-robotaxi.github.io) (coming soon)

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

| Standard | Relevance |
|----------|-----------|
| ISO 34502 | Scenario-based testing framework |
| ISO 21448 (SOTIF) | Safety of the intended functionality |
| ISO 22737 | Low-speed automated driving — performance requirements |
| SAE J3016 | Levels of driving automation |
| ISO/PAS 8800 | Road vehicles — Safety and AI |

## License

Apache License 2.0 — free for commercial use, modification, and distribution.

## Citation

If you use ROAM in your research, please cite:

```bibtex
@misc{roam2026,
  title={ROAM: RoboTaxi Operations Anomaly Management},
  author={Zhang, Yuxin and Contributors},
  year={2026},
  url={https://github.com/roam-robotaxi/ROAM}
}
```
