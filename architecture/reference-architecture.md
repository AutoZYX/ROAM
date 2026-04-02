# ROAM Reference Architecture: Three-Layer Remote Operations Platform

**Version:** 1.0
**Last Updated:** 2026-04-02
**Status:** Initial Release

---

## Important Notice

This is a **reference architecture** — a starting point, not a prescription. Companies should customize this for their specific ADS technology stack, fleet size, regulatory environment, and operational maturity. The layer boundaries, automation targets, and escalation logic described here represent what we consider best practice based on analysis of known incidents, but every deployment has unique constraints.

---

## 1. Architecture Overview

The ROAM Reference Architecture defines a three-layer decision model for handling robotaxi operational anomalies. The core principle: **AI handles routine anomalies autonomously; humans handle the exceptions.**

```
                    ROAM Three-Layer Architecture
   ================================================================

   Anomaly            Layer 1              Layer 2              Layer 3
   Detection    AI Autonomous Response  AI + Human Confirm   Remote Drive/On-Site
   --------     --------------------    ------------------   -------------------

   Vehicle      +-------------------+   +-----------------+  +------------------+
   Sensors  --> | Scenario Classify  |   | AI Proposes     |  | Remote Driving   |
   Fleet    --> | Risk Assessment    |-->| Human Reviews   |->| Physical Dispatch|
   Telemetry--> | Automated Action   |   | Confirm/Modify  |  | Emergency Coord  |
                +-------------------+   +-----------------+  +------------------+

   Target:          70%                     25%                    5%

   Latency:      < 2 seconds             < 60 seconds          < 5 minutes

   Human:           None                 Confirm/Override     Direct Control
```

### Design Principles

1. **AI-First, Human-on-Exception** — The default path is autonomous resolution. Human operators are a scarce, expensive resource reserved for situations that genuinely require judgment.
2. **Fail-Safe Defaults** — When in doubt, the system chooses the conservative option (stop, pull over, unlock doors) rather than waiting for human input.
3. **Graceful Degradation** — If Layer 1 cannot resolve, it escalates to Layer 2. If Layer 2 cannot resolve, it escalates to Layer 3. No anomaly should fall through all layers without response.
4. **Time-Bounded Escalation** — Each layer has a maximum resolution time. Exceeding it triggers automatic escalation to the next layer.
5. **Passenger Communication at Every Layer** — Regardless of which layer handles the anomaly, the passenger receives status updates.

---

## 2. Layer 1: AI Autonomous Response (AI自主响应)

**Target:** 70% of all anomalies
**Latency:** < 2 seconds from detection to action
**Human Involvement:** None

### 2.1 What Layer 1 Handles

Layer 1 handles anomalies where the correct response is deterministic or where a conservative default is always safe:

| Scenario | Layer 1 Action |
|----------|---------------|
| B1 — Intersection hesitation | Timeout -> conservative proceed or reroute |
| B2 — Object misidentification | Treat as solid obstacle, conservative path |
| B3 — Weather degradation | Graduated ODD restriction -> safe stop |
| B4 — Abnormal human behavior | Conservative yield/stop |
| B5 — Localization drift | Speed reduction -> safe stop |
| C2 — Unexpected braking | Post-event logging (no real-time intervention possible) |
| C3 — Dangerous lane change | Abort -> return to original lane |
| C4 — Static object collision | Emergency stop, post-collision protocol |
| C5 — Pedestrian collision | Emergency stop, auto-notify emergency services |
| D1 — Sensor failure | Redundancy failover, ODD restriction |
| D4 — Actuator failure | Redundant actuator failover, safe stop |
| E1 — Struck by other vehicle | Post-collision protocol |
| F2 — Dangerous pickup/dropoff | Select from validated safe point database |

### 2.2 Decision Flow

```
  Anomaly Detected (vehicle telemetry / sensor / fleet monitor)
       |
       v
  +---------------------------+
  | Scenario Classification   |  <-- ML classifier + rule engine
  | (which taxonomy code?)    |
  +---------------------------+
       |
       v
  +---------------------------+
  | Risk Assessment            |  <-- Severity + Urgency scoring
  | S? x U? = Priority         |
  +---------------------------+
       |
       v
  +---------------------------+
  | Layer 1 Handler Lookup     |  <-- Scenario-to-handler mapping
  | Is this a Layer 1 scenario?|
  +---------------------------+
       |           |
       | YES       | NO -> Escalate to Layer 2
       v
  +---------------------------+
  | Execute Automated Action   |
  | (safe stop / reroute /     |
  |  ODD restrict / pullover)  |
  +---------------------------+
       |
       v
  +---------------------------+
  | Verify Outcome             |  <-- Did action resolve the anomaly?
  +---------------------------+
       |           |
       | YES       | NO -> Escalate to Layer 2
       v
  +---------------------------+
  | Log & Close Incident       |
  | Notify passenger if needed |
  +---------------------------+
```

### 2.3 Key Requirements

- **On-board fallback logic**: Vehicles must be able to execute Layer 1 actions WITHOUT cloud connectivity (edge-cached decision logic)
- **Scenario classifier accuracy**: >95% correct primary scenario classification
- **Action library**: Pre-programmed action sequences for each Layer 1 scenario
- **Passenger notification**: Automated in-vehicle messages for relevant events (e.g., "Your vehicle is rerouting due to road construction")

---

## 3. Layer 2: AI-Assisted + Human Confirm (AI辅助 + 人工确认)

**Target:** 25% of all anomalies
**Latency:** < 60 seconds from escalation to resolution
**Human Involvement:** Operator reviews AI recommendation and confirms/modifies

### 3.1 What Layer 2 Handles

Layer 2 handles anomalies where AI can propose a solution but human judgment is needed for confirmation:

| Scenario | AI Proposal | Operator Role |
|----------|-------------|---------------|
| A2 — OTA failure | Recommend rollback | Confirm rollback scope |
| A3 — Infrastructure failure | Propose fleet reroute | Confirm geo-fence boundary |
| C1 — Mid-road freeze | Plot exit path | Confirm path is safe |
| D2 — Powertrain failure | Route to nearest safe stop | Confirm recovery dispatch |
| E2 — Construction zone | Propose reroute | Confirm if ambiguous flaggers |
| E3 — Emergency vehicle | Propose yield maneuver | Confirm appropriate response |
| E4 — Police gesture | Interpret gesture, propose action | Confirm via camera feed |
| F1 — Passenger trapped | Propose door unlock | Verify safe to open doors |
| F3 — Passenger interference | Propose intercom message | Deliver and escalate if needed |

### 3.2 Escalation Triggers (Layer 1 -> Layer 2)

Layer 1 escalates to Layer 2 when:

1. **Timeout** — Layer 1 action did not resolve anomaly within time limit (scenario-specific, typically 30-120 seconds)
2. **Low confidence** — AI classifier confidence below threshold (e.g., <80% for scenario classification)
3. **Novel scenario** — No matching Layer 1 handler found
4. **Multi-factor** — Anomaly involves multiple concurrent scenario codes
5. **Passenger-initiated** — Passenger pressed SOS or called support

### 3.3 Operator Workflow

```
  Escalation arrives in operator queue
       |
       v
  +-----------------------------------+
  | Alert Panel                        |
  | - Vehicle ID, location (map)       |
  | - Live camera feeds (4+ angles)    |
  | - Scenario classification          |
  | - AI recommended action            |
  | - Severity/Urgency assessment      |
  | - Passenger status                 |
  +-----------------------------------+
       |
       v
  Operator reviews (target: <30 seconds)
       |
       +--- Agree with AI recommendation --> Confirm (one-click)
       |
       +--- Modify recommendation --> Adjust parameters, confirm
       |
       +--- Override with different action --> Select from action menu
       |
       +--- Escalate to Layer 3 --> Remote driving / dispatch request
       |
       v
  Action executed on vehicle
       |
       v
  Operator verifies outcome via camera/telemetry
       |
       v
  Close incident or escalate to Layer 3
```

### 3.4 Key Requirements

- **Operator interface**: Single-screen dashboard with live video, map, telemetry, and action controls
- **AI recommendation quality**: >80% of AI recommendations accepted by operator without modification
- **Queue management**: Priority queuing based on Urgency level (U3 preempts all)
- **Communication tools**: Two-way intercom with passenger, text messaging, pre-recorded announcements
- **Decision audit trail**: Every operator decision logged with timestamp, context, and rationale

---

## 4. Layer 3: Remote Driving / On-Site (远程驾驶 / 现场处置)

**Target:** 5% of all anomalies
**Latency:** < 5 minutes from escalation to intervention start
**Human Involvement:** Direct human control of vehicle or physical on-site presence

### 4.1 What Layer 3 Handles

Layer 3 is the last resort — situations that cannot be resolved by automated action or operator commands:

| Scenario | Layer 3 Action |
|----------|---------------|
| A1 — Mass cloud failure (recovery) | Coordinated fleet reactivation |
| C1 — Freeze (unresponsive to commands) | Remote driving to safe location |
| D3 — Vehicle fire | Emergency services coordination, on-site |
| F4 — Medical emergency | Emergency dispatch + hospital routing |
| E3 — Active emergency scene (complex) | On-site coordinator |
| Tow truck dispatch | Physical vehicle recovery |

### 4.2 When Layer 3 Is Needed

Layer 3 is triggered when:

1. **Remote driving required** — Vehicle is in a position where only direct human driving control can move it safely (e.g., frozen in complex intersection, no automated path available)
2. **Physical intervention required** — Hardware failure requiring tow, door mechanism jammed, vehicle fire
3. **Emergency services coordination** — Fatality, serious injury, or fire requires on-site incident commander
4. **Fleet-wide crisis** — Mass failure requiring coordinated recovery of 10+ vehicles

### 4.3 Remote Driving Operations

```
  Remote driving station
  +------------------------------------------------------------+
  |                                                            |
  |  +------------------+  +----------------------------+     |
  |  | Steering wheel   |  | Multi-screen display:      |     |
  |  | Brake/gas pedals |  | - Front camera (primary)   |     |
  |  | Turn signals     |  | - Left/right/rear cameras  |     |
  |  | Horn             |  | - Bird's-eye view (LiDAR)  |     |
  |  +------------------+  | - Map with route overlay   |     |
  |                        | - Vehicle telemetry panel   |     |
  |  Latency monitor:     | - Latency indicator         |     |
  |  [||||||    ] 120ms   +----------------------------+     |
  |                                                            |
  +------------------------------------------------------------+

  Requirements:
  - Network latency: < 150ms round-trip (hard cutoff: 300ms -> auto-stop)
  - Video resolution: 1080p minimum, 30fps minimum
  - Redundant network path (4G + 5G or dual carrier)
  - Operator certification: remote driving license + AV-specific training
```

### 4.4 On-Site Dispatch

For scenarios requiring physical presence:

| Dispatch Type | Response Time Target | Scenarios |
|---------------|---------------------|-----------|
| Recovery vehicle (tow) | < 30 minutes | C1 (unrecoverable freeze), D2, D4 |
| Mobile technician | < 45 minutes | D1 (sensor replacement), general hardware |
| Emergency services (911/119) | < 5 minutes | D3 (fire), F4 (medical), C5 (pedestrian injury) |
| Security personnel | < 20 minutes | F3 (passenger threat), vandalism |
| On-site coordinator | < 30 minutes | A1 (mass failure recovery), complex multi-vehicle |

---

## 5. System Component Diagram

```
+============================================================================+
|                         ROAM Platform Architecture                          |
+============================================================================+

+---------------------------+        +----------------------------------+
|     Vehicle Fleet         |        |     Cloud Platform               |
|                           |  5G/4G |                                  |
| +--------+ +--------+    |<=======>| +----------------------------+  |
| |Vehicle | |Vehicle |    |        | | Fleet Management System    |  |
| | ADS    | | ADS    |... |        | | - Vehicle registry         |  |
| | Edge   | | Edge   |    |        | | - Trip management          |  |
| | Logic  | | Logic  |    |        | | - OTA management           |  |
| +--------+ +--------+    |        | +----------------------------+  |
|                           |        |                                  |
| - Sensor suite            |        | +----------------------------+  |
| - Compute platform        |        | | Anomaly Detection Engine   |  |
| - Edge AI (Layer 1)       |        | | - Telemetry aggregation    |  |
| - Local MRC fallback      |        | | - Pattern detection        |  |
| - Vehicle-to-cloud link   |        | | - Scenario classifier (ML) |  |
+---------------------------+        | | - Severity/Urgency scorer  |  |
                                     | +----------------------------+  |
                                     |                                  |
+---------------------------+        | +----------------------------+  |
|  Operator Console         |        | | Decision Engine            |  |
|                           |        | | - Layer routing logic      |  |
| +---------------------+  |        | | - Action library           |  |
| | Layer 2 Dashboard    |  |<======>| | - Escalation rules         |  |
| | - Live video feeds   |  |        | | - AI recommendation gen    |  |
| | - Map + telemetry    |  |        | +----------------------------+  |
| | - Action controls    |  |        |                                  |
| | - Intercom           |  |        | +----------------------------+  |
| | - Queue management   |  |        | | Incident Database          |  |
| +---------------------+  |        | | - Event log                |  |
|                           |        | | - Decision audit trail     |  |
| +---------------------+  |        | | - Analytics + KPI          |  |
| | Layer 3: Remote      |  |        | +----------------------------+  |
| | Driving Station      |  |        |                                  |
| | - Steering + pedals  |  |        | +----------------------------+  |
| | - Multi-camera view  |  |        | | Passenger Communication    |  |
| | - Latency monitor    |  |        | | - Push notifications       |  |
| +---------------------+  |        | | - In-vehicle intercom      |  |
+---------------------------+        | | - SOS handling             |  |
                                     | +----------------------------+  |
+---------------------------+        |                                  |
|  External Integrations    |        | +----------------------------+  |
|                           |        | | External API Gateway       |  |
| - Emergency services API  |<======>| | - Emergency dispatch       |  |
| - Traffic authority API   |        | | - Traffic authority        |  |
| - Weather data feed       |        | | - Weather ingestion        |  |
| - Map provider API        |        | | - Map update pipeline      |  |
| - Dispatch (tow/tech)     |        | +----------------------------+  |
+---------------------------+        +----------------------------------+
```

---

## 6. Complete Scenario-to-Handler Mapping

This table maps every taxonomy sub-scenario to its primary handling layer, automated action, and escalation path.

| ID | Scenario | Primary Layer | Automated Action (Layer 1) | Layer 2 Action | Layer 3 Trigger |
|----|----------|:----:|-----|-----|-----|
| **A1** | Cloud/Network Mass Failure | 1 | Vehicle MRC (safe stop, unlock doors, hazard lights) | Fleet-wide status assessment | Coordinated recovery if >10 vehicles |
| **A2** | OTA Update Failure | 2 | Detect anomaly spike post-update | Operator confirms fleet rollback | Engineering team if rollback fails |
| **A3** | External Infrastructure | 2 | Reroute away from affected zone | Operator confirms geo-fence | On-site if vehicles stranded in zone |
| **A4** | Server Decision Crash | 1 | Fall back to cached local logic | — | Engineering restores server |
| **B1** | Intersection Hesitation | 1 | Timeout -> conservative proceed/reroute | Operator confirms "proceed" | — |
| **B2** | Object Misidentification | 1 | Treat as solid obstacle | Operator reviews if persistent | — |
| **B3** | Weather Degradation | 1 | ODD restriction -> safe stop | Operator confirms safe stop location | — |
| **B4** | Abnormal Human Behavior | 1 | Conservative yield/stop | Operator advises reroute or authorities | Security dispatch if threat |
| **B5** | Localization Drift | 1 | Speed reduce -> safe stop | Operator confirms recovery | Tow truck if unrecoverable |
| **C1** | Mid-Road Freeze | 2 | Detect freeze state, alert | Operator sends pullover command | Remote driving / tow truck |
| **C2** | Unexpected Braking | 1 | Post-event log + pattern detect | — (too fast for real-time) | — |
| **C3** | Dangerous Lane Change | 1 | Abort -> return to original lane | — | — |
| **C4** | Static Object Collision | 1 | Emergency stop, post-collision protocol | — | Emergency services if injury |
| **C5** | Pedestrian Collision | 1 | Emergency stop + auto 911/119 | Operator confirms scene | Emergency services on-site |
| **D1** | Sensor Failure | 1 | Redundancy failover, ODD restrict | Operator confirms return-to-base | Mobile technician |
| **D2** | Powertrain/Battery | 2 | Route to nearest safe stop | Operator dispatches recovery | Tow truck |
| **D3** | Vehicle Fire | 3 | Emergency stop, unlock doors | — | Emergency services immediate |
| **D4** | Actuator Failure | 1 | Redundant actuator failover | — | Tow truck if redundancy fails |
| **E1** | Struck by Other Vehicle | 1 | Post-collision protocol, eCall | Operator assesses scene | Emergency services if injury |
| **E2** | Construction/Closure | 2 | Reroute if detected early | Operator interprets flaggers | — |
| **E3** | Emergency Vehicle | 2 | Pull over, yield | Operator confirms response | On-site if complex scene |
| **E4** | Police Gesture Failure | 2 | Stop, flag low confidence | Operator interprets via camera | — |
| **F1** | Passenger Trapped | 2 | — | Operator remote unlock (if safe) | Fire dept extraction |
| **F2** | Dangerous Pickup/Dropoff | 1 | Select from validated safe points | Operator suggests alternative | — |
| **F3** | Passenger Interference | 2 | Interior monitoring alert | Operator intercom + warning | Security dispatch |
| **F4** | Medical Emergency | 3 | — | — | Emergency services + hospital routing |

---

## 7. API Interaction Flow

The following sequence describes the typical API interaction between vehicle, cloud platform, and operator console for a Layer 2 escalation.

```
Vehicle              Cloud Platform           Operator Console
  |                       |                        |
  |--[1] Telemetry------->|                        |
  |  (anomaly detected)   |                        |
  |                       |--[2] Classify---------->|
  |                       |  scenario + S/U score   |
  |                       |                        |
  |                       |--[3] Route to Layer---->|
  |                       |  (L1 failed, -> L2)     |
  |                       |                        |
  |                       |                  [4] Queue alert
  |                       |                  Operator reviews
  |                       |                  AI recommendation
  |                       |                        |
  |                       |<--[5] Operator action---|
  |                       |  (confirm/modify/       |
  |                       |   override/escalate)    |
  |                       |                        |
  |<--[6] Command---------|                        |
  |  (pullover/reroute/   |                        |
  |   unlock/remote drive) |                        |
  |                       |                        |
  |--[7] Execution ACK--->|                        |
  |                       |--[8] Status update----->|
  |                       |                        |
  |--[9] Resolution------>|                        |
  |  (anomaly resolved)   |--[10] Close incident-->|
  |                       |                        |
```

### Key API Endpoints (Reference)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/anomaly/report` | POST | Vehicle reports anomaly with telemetry snapshot |
| `/v1/anomaly/{id}/classify` | GET | Returns scenario classification + S/U scores |
| `/v1/anomaly/{id}/action` | POST | Execute automated action or operator command |
| `/v1/anomaly/{id}/escalate` | POST | Escalate to next layer |
| `/v1/anomaly/{id}/status` | GET | Current anomaly status and resolution progress |
| `/v1/vehicle/{id}/command` | POST | Send direct command to vehicle (pullover, unlock, etc.) |
| `/v1/vehicle/{id}/remote-drive` | POST | Initiate remote driving session |
| `/v1/vehicle/{id}/telemetry` | WS | WebSocket stream for real-time telemetry |
| `/v1/fleet/status` | GET | Fleet-wide anomaly summary |
| `/v1/operator/queue` | GET | Operator's current task queue |
| `/v1/passenger/{trip_id}/notify` | POST | Send notification to passenger |

---

## 8. Deployment Considerations

### 8.1 Scaling

| Fleet Size | Recommended Operators (Layer 2) | Remote Drivers (Layer 3) | Target Ratio |
|-----------|:-----:|:-----:|:-----:|
| 50 vehicles | 2-3 | 1 | 1:20 |
| 200 vehicles | 5-8 | 2-3 | 1:30 |
| 1,000 vehicles | 15-25 | 5-8 | 1:50 |
| 5,000+ vehicles | 50-80 | 15-20 | 1:80 |

Note: These ratios assume Layer 1 resolves 70%+ of anomalies. If Layer 1 resolution rate is lower, more operators are needed.

### 8.2 Network Requirements

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| Uplink bandwidth (per vehicle) | 2 Mbps | 10 Mbps |
| Downlink bandwidth (per vehicle) | 500 Kbps | 2 Mbps |
| Round-trip latency (vehicle-cloud) | < 200ms | < 100ms |
| Round-trip latency (remote driving) | < 300ms | < 150ms |
| Network availability | 99.9% | 99.99% |
| Redundant network paths | 1 (4G or 5G) | 2 (4G + 5G or dual carrier) |

### 8.3 Customization Guidance

This reference architecture should be adapted for:

1. **Regulatory environment** — Some jurisdictions require human-in-the-loop for all operational decisions; others allow autonomous operation with remote monitoring only.
2. **ADS capability** — More capable ADS shifts the Layer 1/2 boundary (more scenarios handled autonomously).
3. **Service area** — Urban vs. suburban vs. highway deployments have different scenario frequency profiles.
4. **Fleet size** — Small fleets (<50 vehicles) may not need a dedicated Decision Engine; large fleets (>1000) need distributed architecture.
5. **Technology stack** — The API endpoints, message formats, and integration patterns should match your existing platform.

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-02 | Initial release |
