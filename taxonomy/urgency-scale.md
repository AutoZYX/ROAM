# ROAM Urgency Scale

**Version:** 1.0
**Last Updated:** 2026-04-02

---

## Overview

The urgency scale classifies how quickly an operational anomaly requires response. Unlike severity (which measures outcome impact), urgency measures **time sensitivity** — how fast the situation will deteriorate without intervention.

Urgency is assessed in real-time and drives the dispatching priority of the operations platform.

---

## Urgency Levels

### U0 — Low (低优先级)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly has no active time pressure. Can be resolved during the next scheduled maintenance cycle or shift review. No passengers at risk, no traffic impact, no ongoing degradation. |
| **Response Window** | Next maintenance cycle (hours to days) |
| **Operator Action** | No real-time response needed. Logged for batch review. |
| **Escalation Trigger** | Escalate to U1 if pattern repeats 3+ times within 24 hours |
| **Examples** | Single phantom braking event with no traffic consequence; minor sensor calibration drift within tolerance; pickup point feedback from passenger; non-critical OTA update available |
| **Typical Scenarios** | S0 near-misses, post-incident reporting tasks, fleet analytics alerts |

---

### U1 — Medium (中优先级)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly requires human attention within 30 minutes. Situation is stable but will worsen or accumulate if not addressed. May involve degraded vehicle performance or minor operational disruption. |
| **Response Window** | Within 30 minutes |
| **Operator Action** | Review and resolve during current shift. May require remote command or dispatch. |
| **Escalation Trigger** | Escalate to U2 if vehicle enters active traffic lane OR passenger reports distress |
| **Examples** | Vehicle in safe stop at roadside requiring recovery dispatch; sensor failure with redundancy still active but ODD restricted; multiple vehicles encountering same construction zone; passenger complaint requiring callback |
| **Typical Scenarios** | D1 (sensor failure, redundant), D2 (powertrain degradation), E2 (construction), F2 (pickup issues) |

---

### U2 — High (高优先级)

| Field | Description |
|-------|-------------|
| **Definition** | Anomaly requires resolution within 10 minutes. Active traffic disruption or passenger distress is occurring. Situation is degrading and will escalate to U3 if not addressed. |
| **Response Window** | Within 10 minutes |
| **Operator Action** | Immediate operator engagement. Remote intervention, command dispatch, or emergency coordination required. |
| **Escalation Trigger** | Escalate to U3 if passenger safety is at immediate risk OR emergency vehicle is blocked |
| **Examples** | Vehicle frozen in active traffic lane; passenger trapped in vehicle (doors locked); multiple vehicles affected by same fault; emergency vehicle approaching and vehicle not yielding properly |
| **Typical Scenarios** | C1 (mid-road freeze), F1 (passenger trapped), A1 (cloud failure affecting active vehicles), E3 (emergency vehicle interaction) |

---

### U3 — Immediate (紧急)

| Field | Description |
|-------|-------------|
| **Definition** | Passenger safety is at immediate risk, emergency vehicle is actively blocked, or situation involves imminent danger to life. Requires instant response with no queue delay. |
| **Response Window** | Immediate (seconds, not minutes) |
| **Operator Action** | Override all other tasks. Dedicated operator assigned. Emergency services dispatched if not already. Direct voice contact with passenger if applicable. |
| **Escalation Trigger** | Already at maximum urgency. If unresolved within 5 minutes, trigger executive notification and public safety authority contact. |
| **Examples** | Passenger medical emergency; vehicle fire; vehicle blocking active ambulance or fire truck; pedestrian contact; passenger reporting threat or assault; vehicle on elevated highway with imminent collision risk |
| **Typical Scenarios** | F4 (medical emergency), D3 (vehicle fire), C5 (pedestrian collision), E3 (emergency vehicle actively blocked), F1 (passenger trapped in dangerous location) |

---

## Urgency Assessment Flowchart

```
Anomaly Detected
    |
    v
Immediate life safety risk? (fire, medical, collision, blocked emergency vehicle)
    |-- YES --> U3
    |-- NO
    v
Active traffic disruption OR passenger trapped?
    |-- YES --> U2
    |-- NO
    v
Degraded performance requiring same-shift resolution?
    |-- YES --> U1
    |-- NO --> U0
```

---

## Urgency-Severity Matrix

The combination of severity and urgency determines the overall priority:

|  | U0 (Low) | U1 (Medium) | U2 (High) | U3 (Immediate) |
|--|:--------:|:-----------:|:---------:|:--------------:|
| **S0** | Routine | Monitor | Unusual | Investigate |
| **S1** | Log | Resolve | Priority | Priority |
| **S2** | Review | Priority | Critical | Critical |
| **S3** | — | Critical | Critical | Emergency |
| **S4** | — | — | Emergency | Emergency |

**Priority Definitions:**
- **Routine** — Batch processing, trend analysis
- **Log** — Record and review in daily summary
- **Monitor** — Watch for pattern development
- **Resolve** — Assign to operator this shift
- **Investigate** — Unusual combination, check for misclassification
- **Priority** — Top of operator queue
- **Critical** — Dedicated operator, management notification
- **Emergency** — All available resources, emergency services, executive notification

---

## Queue Management Rules

1. **U3 events always preempt all other tasks.** An operator handling a U1 event must immediately switch to a U3 event.
2. **U2 events preempt U0 and U1.** Operators can finish a U1 action in progress but must not start new U0/U1 work.
3. **Maximum queue depth per operator:** 1 x U3, 2 x U2, 5 x U1 at any time. Exceeding these limits triggers additional operator activation.
4. **Automatic escalation:** U2 events unresolved for >10 minutes automatically escalate to U3. U1 events unresolved for >30 minutes escalate to U2.

---

## Notes

1. Urgency is a **real-time** assessment that can change as the situation evolves. A U1 event (vehicle at roadside) becomes U2 if the passenger reports feeling unsafe, and U3 if the vehicle is on a highway shoulder with approaching traffic.
2. Urgency is independent of severity. A U3/S0 combination is valid — for example, a near-miss where a passenger is panicking and pressing SOS.
3. Time windows are **maximum response times**, not target times. Target response times should be significantly shorter (see KPI definitions).
