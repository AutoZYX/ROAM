# ROAM Severity Scale

**Version:** 1.0
**Last Updated:** 2026-04-02

---

## Overview

The severity scale classifies the **outcome impact** of a robotaxi operational anomaly. Severity is assessed after the incident based on actual consequences, not predicted risk.

Severity and urgency are orthogonal dimensions: a near-miss (S0) can have immediate urgency (U3) if passengers are at risk, while a severe traffic disruption (S3) may have low urgency (U0) if it is already resolved.

---

## Severity Levels

### S0 — Near-Miss (未遂事件)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly detected and resolved with no impact on traffic, passengers, or other road users. System self-recovered or operator resolved before any consequence materialized. |
| **Traffic Impact** | None |
| **Injury** | None |
| **Duration** | N/A (resolved before impact) |
| **Vehicles Affected** | Typically 1 |
| **Examples** | Phantom braking detected and logged but no following vehicle close enough to matter; hesitation at intersection resolved within 10 seconds; sensor failover to redundant unit with no performance gap |
| **Reporting** | Internal log only; aggregated for trend analysis |
| **Regulatory Relevance** | Not individually reportable, but aggregate S0 patterns may indicate systemic risk |

---

### S1 — Minor (轻微事件)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly caused minor traffic disruption with no injuries. Vehicle may have stopped briefly or caused other vehicles to slow down. Resolved within 5 minutes. |
| **Traffic Impact** | Minor — brief slowdown, one lane partially blocked for <5 minutes |
| **Injury** | None |
| **Duration** | < 5 minutes |
| **Vehicles Affected** | 1-2 |
| **Examples** | Vehicle stops in traffic lane for 2 minutes before self-recovering; incorrect pickup location requires passenger to walk 50 meters; minor curb contact during parking with no damage |
| **Reporting** | Internal incident report; aggregate reporting to fleet safety dashboard |
| **Regulatory Relevance** | Typically below reporting thresholds in most jurisdictions |

---

### S2 — Moderate (中等事件)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly caused significant traffic disruption OR minor injury. Required human intervention to resolve. Duration between 5 and 30 minutes. |
| **Traffic Impact** | Significant — lane blocked for 5-30 minutes, visible traffic queue, or multiple vehicles affected |
| **Injury** | None or minor (first-aid level, no hospitalization) |
| **Duration** | 5 - 30 minutes |
| **Vehicles Affected** | 1-5 |
| **Examples** | Vehicle frozen in traffic lane requiring remote driving to move; minor collision with property damage; passenger trapped for 10 minutes before door unlock; emergency vehicle delayed by AV |
| **Reporting** | Formal incident report; root cause analysis within 48 hours |
| **Regulatory Relevance** | May trigger reporting requirements depending on jurisdiction (e.g., collision with property damage) |

---

### S3 — Severe (严重事件)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly caused major traffic paralysis OR serious injury. Multiple vehicles or road users significantly affected. Duration exceeds 30 minutes. May involve emergency services response. |
| **Traffic Impact** | Major — multiple lanes or road segment blocked for >30 minutes, significant area-wide disruption |
| **Injury** | Serious (hospitalization required) or multiple minor injuries |
| **Duration** | > 30 minutes |
| **Vehicles Affected** | Multiple (>5) or significant third-party impact |
| **Examples** | Multi-vehicle collision requiring ambulance; vehicle fire with road closure; fleet-level software fault causing 10+ vehicles to stop in traffic; passenger medical emergency with delayed response |
| **Reporting** | Formal incident report; root cause analysis within 24 hours; executive notification |
| **Regulatory Relevance** | Reportable to NHTSA (SGO), local DMV, or equivalent authority in most jurisdictions |

---

### S4 — Critical (致命/系统性事件)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly resulted in fatality OR mass system failure affecting more than 50 vehicles simultaneously. The most severe category — triggers industry-wide scrutiny and potential regulatory action. |
| **Traffic Impact** | Critical — city-level disruption, emergency services overwhelmed, public safety impact |
| **Injury** | Fatality or life-threatening injury; OR mass passenger entrapment |
| **Duration** | Extended (often hours) |
| **Vehicles Affected** | 1 (if fatality) or >50 (if mass system failure) |
| **Examples** | ROAM-2023-001: Cruise pedestrian dragging (S4 — life-altering injury, 950 vehicles recalled); ROAM-2026-004: Apollo Wuhan mass shutdown (~100 vehicles, passengers trapped for 2 hours on elevated highway) |
| **Reporting** | Immediate executive and board notification; formal regulatory report within 24 hours; public disclosure likely |
| **Regulatory Relevance** | Mandatory reporting in all jurisdictions; likely triggers investigation, potential recall, license suspension, or operational restriction |

---

## Severity Assessment Flowchart

```
Incident Occurs
    |
    v
Any fatality or life-threatening injury?
    |-- YES --> S4
    |-- NO
    v
Mass system failure (>50 vehicles)?
    |-- YES --> S4
    |-- NO
    v
Serious injury (hospitalization) OR major traffic paralysis (>30 min)?
    |-- YES --> S3
    |-- NO
    v
Significant disruption (5-30 min) OR minor injury?
    |-- YES --> S2
    |-- NO
    v
Minor disruption (<5 min, no injury)?
    |-- YES --> S1
    |-- NO --> S0 (Near-miss)
```

---

## Severity Distribution Target

For a mature robotaxi operations platform, the target severity distribution is:

| Severity | Target % of All Incidents |
|----------|:------------------------:|
| S0 | > 80% |
| S1 | 10-15% |
| S2 | 3-5% |
| S3 | < 1% |
| S4 | < 0.01% |

A platform where >80% of anomalies are caught as S0 near-misses indicates effective proactive monitoring. A rising S2+ percentage is a leading indicator of systemic risk.

---

## Notes

1. Severity is assigned based on **actual outcome**, not worst-case potential. A vehicle frozen on a highway is S2 if resolved in 15 minutes, even though the potential outcome could have been S3+.
2. When an incident involves both injury and traffic disruption, use the **higher** severity level.
3. Multi-vehicle incidents are assessed as a **single event** with combined impact, not per-vehicle.
4. Severity can be **upgraded** during investigation if additional consequences are discovered.
