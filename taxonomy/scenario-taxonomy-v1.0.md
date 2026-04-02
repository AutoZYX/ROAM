# ROAM Scenario Taxonomy v1.0

**Version:** 1.0
**Last Updated:** 2026-04-02
**Status:** Initial Release

---

## Overview

This taxonomy classifies operational anomalies encountered by L4+ robotaxi fleets into 6 major categories and 27 sub-scenarios. Each sub-scenario is assigned a recommended response layer (1/2/3) based on the typical complexity and risk level.

The taxonomy is designed to be:
- **Exhaustive** — covers all known incident types from public reports and operator disclosures
- **Mutually exclusive at L1** — each incident has one primary category (secondary codes allowed)
- **Actionable** — each sub-scenario maps to a recommended response layer

### Category Index

| Code | Category (EN) | Category (CN) | Sub-scenarios |
|------|--------------|---------------|---------------|
| A | System-Wide Failure | 系统性故障 | A1 - A4 |
| B | Perception/Decision Failure | 感知/决策失效 | B1 - B5 |
| C | Planning/Execution Anomaly | 规划/执行异常 | C1 - C5 |
| D | Vehicle Hardware Failure | 车辆硬件故障 | D1 - D4 |
| E | External Conflict | 外部环境冲突 | E1 - E4 |
| F | Passenger-Side Issue | 乘客端异常 | F1 - F4 |

### Response Layer Key

| Layer | Name | Target % | Description |
|-------|------|----------|-------------|
| 1 | AI Autonomous Response | 70% | System resolves without human involvement |
| 2 | AI-Assisted + Human Confirm | 25% | AI proposes action, human operator confirms |
| 3 | Remote Driving / On-Site | 5% | Direct human control or physical intervention |

---

## A. System-Wide Failure (系统性故障)

Anomalies affecting multiple vehicles simultaneously due to infrastructure, cloud, or platform-level failures. These are the highest-stakes scenarios because they can paralyze an entire fleet in minutes.

### A1 - Cloud/Network Mass Failure (云端/网络大面积故障)

| Field | Value |
|-------|-------|
| **ID** | A1 |
| **Name (EN)** | Cloud/Network Mass Failure |
| **Name (CN)** | 云端/网络大面积故障 |
| **Description** | Loss of connectivity between fleet vehicles and the cloud platform due to network outage, cloud provider failure, or communication infrastructure breakdown. Vehicles lose access to remote operations, routing updates, and fleet management commands. |
| **Real Example** | ROAM-2026-004: Apollo Wuhan mass shutdown where nearly 100 vehicles simultaneously lost cloud connectivity on elevated highways, trapping passengers for up to 2 hours. |
| **Typical Frequency** | Rare (1-2 per fleet per year), but extremely high impact when it occurs |
| **Recommended Layer** | **Layer 1** for individual vehicle fallback (safe stop); **Layer 3** for fleet-wide recovery coordination |

**Typical Handling:**
- Vehicles execute pre-programmed Minimum Risk Condition (MRC) — pull over, hazard lights, unlock doors
- Edge-cached decision logic handles immediate safety without cloud
- Fleet-wide recovery requires coordinated Layer 3 response after connectivity restores

---

### A2 - OTA Update Failure (OTA升级故障)

| Field | Value |
|-------|-------|
| **ID** | A2 |
| **Name (EN)** | OTA Update Failure |
| **Name (CN)** | OTA升级故障 |
| **Description** | Over-the-air software update causes system instability, partial module failure, or version incompatibility across the fleet. May affect perception, planning, or vehicle control modules. Can trigger simultaneous failures if update is pushed fleet-wide. |
| **Real Example** | ROAM-2023-002: Cruise unexpected braking recall — software defect introduced via OTA update caused 594 vehicles to exhibit hard braking behavior in certain conditions. |
| **Typical Frequency** | Low (1-3 per fleet per year for significant OTA issues) |
| **Recommended Layer** | **Layer 2** (AI detects anomalous behavior patterns post-update, human confirms rollback decision) |

**Typical Handling:**
- Automated monitoring detects post-update anomaly spike
- AI recommends fleet-wide rollback; operator confirms
- Affected vehicles enter conservative driving mode or safe stop pending rollback
- Staged rollout policies prevent fleet-wide simultaneous failure

---

### A3 - External Infrastructure Failure (外部基础设施故障)

| Field | Value |
|-------|-------|
| **ID** | A3 |
| **Name (EN)** | External Infrastructure Failure |
| **Name (CN)** | 外部基础设施故障 |
| **Description** | Failure of external systems the ADS depends on — power grid outage (affecting charging/V2X), traffic signal system failure, V2X communication breakdown, or third-party map data corruption. |
| **Real Example** | Waymo SF power outage (2025-12): city-wide power disruption left vehicles stranded, emergency services called Waymo hotline 31 times with a combined 2.5-hour wait. |
| **Typical Frequency** | Moderate (varies by city infrastructure reliability) |
| **Recommended Layer** | **Layer 2** (AI reroutes around affected area, human confirms fleet-wide response strategy) |

**Typical Handling:**
- Real-time infrastructure health monitoring triggers alerts
- AI reroutes vehicles away from affected zones
- Operator coordinates with city authorities on scope and timeline
- Vehicles in affected area execute safe stop if no viable reroute exists

---

### A4 - Server Decision System Crash (服务端决策系统崩溃)

| Field | Value |
|-------|-------|
| **ID** | A4 |
| **Name (EN)** | Server Decision System Crash |
| **Name (CN)** | 服务端决策系统崩溃 |
| **Description** | The centralized decision-making or dispatch system crashes, leaving vehicles unable to receive new routing commands, dynamic rerouting, or escalation responses. Different from A1 (connectivity intact but server logic fails). |
| **Real Example** | No public ROAM incident yet. Analogous to cloud platform outages reported by multiple operators during rapid scaling phases. |
| **Typical Frequency** | Rare (robust operators have redundancy), but catastrophic without failover |
| **Recommended Layer** | **Layer 1** (vehicles operate on cached local logic); **Layer 3** (system-level recovery by engineering team) |

**Typical Handling:**
- Vehicles fall back to on-board cached routing and local decision logic
- Automated failover to backup decision server
- No new trip assignments until system recovers
- Engineering team restores service; operator coordinates fleet re-activation

---

## B. Perception/Decision Failure (感知/决策失效)

Anomalies where the vehicle's perception system or decision-making logic fails to correctly interpret the driving environment, leading to inappropriate or absent responses.

### B1 - Complex Intersection Hesitation (复杂路口犹豫不决)

| Field | Value |
|-------|-------|
| **ID** | B1 |
| **Name (EN)** | Complex Intersection Hesitation |
| **Name (CN)** | 复杂路口犹豫不决 |
| **Description** | Vehicle stops or hesitates excessively at complex intersections — unprotected left turns, multi-way stops, roundabouts with heavy traffic, or intersections with ambiguous right-of-way. Blocks traffic and frustrates other road users. |
| **Real Example** | Widely reported across Waymo and Cruise deployments in San Francisco. Vehicles repeatedly yielded at 4-way stops, causing traffic backup. Common in unprotected left-turn scenarios. |
| **Typical Frequency** | High (most common single-vehicle anomaly in urban deployment) |
| **Recommended Layer** | **Layer 1** (AI times out and executes conservative merge/turn) or **Layer 2** (operator confirms "proceed" command) |

**Typical Handling:**
- AI detects hesitation exceeding threshold (e.g., 30 seconds at intersection)
- Layer 1: automated conservative proceed or reroute to avoid the intersection
- Layer 2: operator reviews live feed, confirms proceed or reroute
- Long-term: intersection-specific tuning based on accumulated data

---

### B2 - Object Misidentification (目标误识别)

| Field | Value |
|-------|-------|
| **ID** | B2 |
| **Name (EN)** | Object Misidentification |
| **Name (CN)** | 目标误识别 |
| **Description** | Perception system misclassifies an object — phantom braking for shadows/overpasses, failing to recognize a stopped vehicle, misinterpreting a plastic bag as a solid obstacle, or failing to detect a pedestrian in unusual posture. |
| **Real Example** | ROAM-2023-002: Cruise recall due to hard braking from perception misclassification. Uber ATG fatal crash (2018) — system failed to correctly classify a pedestrian pushing a bicycle. |
| **Typical Frequency** | Moderate-High (perception errors are a leading cause of disengagements) |
| **Recommended Layer** | **Layer 1** (conservative fallback — treat ambiguous object as solid obstacle) |

**Typical Handling:**
- Conservative default: treat any ambiguous object as solid obstacle
- Multi-sensor fusion cross-checks (LiDAR + camera + radar)
- If object persists as ambiguous for >5 seconds, escalate to Layer 2
- Post-incident perception log review for model improvement

---

### B3 - Extreme Weather Perception Degradation (极端天气感知退化)

| Field | Value |
|-------|-------|
| **ID** | B3 |
| **Name (EN)** | Extreme Weather Perception Degradation |
| **Name (CN)** | 极端天气感知退化 |
| **Description** | Heavy rain, snow, fog, dust storm, or direct sun glare degrades sensor performance below safe operating thresholds. LiDAR returns scatter in rain, cameras saturate in glare, radar noise increases in heavy precipitation. |
| **Real Example** | Multiple Waymo disengagement reports in heavy rain conditions. Apollo vehicles in Wuhan experience performance degradation during seasonal heavy rain. |
| **Typical Frequency** | Moderate (seasonal, geography-dependent) |
| **Recommended Layer** | **Layer 1** (automated speed reduction and ODD exit when thresholds exceeded) |

**Typical Handling:**
- Real-time sensor confidence monitoring
- Graduated response: reduce speed -> increase following distance -> limit ODD -> safe stop
- Pre-trip weather check prevents dispatch into known severe conditions
- If degradation occurs mid-trip, AI executes safe pullover; operator confirms passenger communication

---

### B4 - Abnormal Human Behavior (异常人类行为)

| Field | Value |
|-------|-------|
| **ID** | B4 |
| **Name (EN)** | Abnormal Human Behavior |
| **Name (CN)** | 异常人类行为 |
| **Description** | Unexpected actions by other road users — jaywalking, running red lights, wrong-way driving, children darting into road, intoxicated pedestrians, or deliberate antagonism toward AV (standing in front, hitting vehicle). |
| **Real Example** | ROAM-2026-001: Waymo Santa Monica incident involving a child near the vehicle. San Francisco residents reported repeatedly blocking Cruise vehicles. |
| **Typical Frequency** | High (especially in dense urban environments with mixed traffic) |
| **Recommended Layer** | **Layer 1** (conservative yield/stop) escalating to **Layer 2** if sustained antagonism |

**Typical Handling:**
- Conservative default: yield and stop for any abnormal pedestrian/cyclist behavior
- If behavior is sustained (deliberate blocking), escalate to Layer 2
- Operator may advise reroute or contact local authorities
- If physical threat to vehicle, Layer 3 (dispatch on-site security)

---

### B5 - GPS/Localization Drift (GPS/定位漂移)

| Field | Value |
|-------|-------|
| **ID** | B5 |
| **Name (EN)** | GPS/Localization Drift |
| **Name (CN)** | GPS/定位漂移 |
| **Description** | Vehicle's localization system experiences significant drift — GPS multipath in urban canyons, HD map mismatch, SLAM failure in feature-poor areas, or post-construction environment change that invalidates stored maps. |
| **Real Example** | Commonly reported in dense urban environments with tall buildings (Shanghai Lujiazui, San Francisco Financial District). Construction zone map mismatches documented across multiple operators. |
| **Typical Frequency** | Moderate (higher in specific urban corridors) |
| **Recommended Layer** | **Layer 1** (automated safe stop when localization confidence drops below threshold) |

**Typical Handling:**
- Real-time localization confidence score monitoring
- Automated speed reduction when confidence degrades
- Safe stop when localization falls below minimum threshold
- Operator dispatches recovery vehicle if safe self-recovery impossible

---

## C. Planning/Execution Anomaly (规划/执行异常)

Anomalies where the vehicle's planning or control system produces dangerous, inappropriate, or frozen output despite correct (or near-correct) perception.

### C1 - Mid-Road Freeze (路中间冻住/停死)

| Field | Value |
|-------|-------|
| **ID** | C1 |
| **Name (EN)** | Mid-Road Freeze |
| **Name (CN)** | 路中间冻住/停死 |
| **Description** | Vehicle stops in a live traffic lane and cannot self-recover — planning system enters deadlock, conflicting constraints prevent any safe maneuver, or system enters undefined state. Different from B1 (not at intersection, not hesitation — complete system freeze). |
| **Real Example** | ROAM-2026-004: Apollo vehicles frozen on elevated highway lanes during Wuhan mass shutdown. Multiple Cruise vehicles documented frozen in SF traffic lanes requiring tow truck removal. |
| **Typical Frequency** | Moderate (one of the most visible and disruptive single-vehicle anomalies) |
| **Recommended Layer** | **Layer 2** (operator confirms pullover or reroute command) escalating to **Layer 3** (remote driving or on-site tow) |

**Typical Handling:**
- AI detects freeze state (zero motion, no active maneuver, >15 seconds)
- Layer 2: operator sends pullover command or manually plots exit path
- If vehicle cannot execute command, Layer 3: remote driving to safe location
- If remote driving fails, dispatch tow truck

---

### C2 - Unexpected Hard Braking (意外急刹车)

| Field | Value |
|-------|-------|
| **ID** | C2 |
| **Name (EN)** | Unexpected Hard Braking |
| **Name (CN)** | 意外急刹车 |
| **Description** | Vehicle executes sudden, hard braking without visible cause — phantom braking from perception false positives, overly conservative collision avoidance triggering, or planning/control oscillation. Risk of rear-end collision by following vehicle. |
| **Real Example** | ROAM-2023-002: Cruise hard braking recall affecting 594 vehicles. Widely documented in Waymo vehicles on highways due to overpass shadow detection. |
| **Typical Frequency** | High (among the most frequently reported AV anomalies) |
| **Recommended Layer** | **Layer 1** (post-event logging and automated pattern detection; no real-time intervention possible for braking events) |

**Typical Handling:**
- Event occurs too fast for real-time human intervention
- Automated post-event analysis flags phantom braking clusters
- Batch fix through perception model update and OTA deployment
- Persistent patterns trigger fleet-wide operational restriction

---

### C3 - Dangerous Lane Change (危险变道)

| Field | Value |
|-------|-------|
| **ID** | C3 |
| **Name (EN)** | Dangerous Lane Change |
| **Name (CN)** | 危险变道 |
| **Description** | Vehicle executes a lane change that creates a hazardous situation — cutting off other vehicles, merging into occupied space, excessive swerving, or lane change into oncoming traffic due to map/localization error. |
| **Real Example** | ROAM-2026-003: Waymo SF two-vehicle collision during lane change maneuver. Multiple documented cases of aggressive merge behavior in dense traffic. |
| **Typical Frequency** | Moderate |
| **Recommended Layer** | **Layer 1** (automated conservative lane-change policy) |

**Typical Handling:**
- Conservative lane-change parameters (larger gaps, slower execution)
- Multi-sensor blind-spot monitoring with redundancy
- If lane change aborted mid-maneuver, AI recovers to original lane
- Post-event analysis for planning algorithm improvement

---

### C4 - Static Object Collision (静态障碍物碰撞)

| Field | Value |
|-------|-------|
| **ID** | C4 |
| **Name (EN)** | Static Object Collision |
| **Name (CN)** | 静态障碍物碰撞 |
| **Description** | Vehicle collides with a stationary object — parked vehicle, bollard, construction barrier, curb, median, or building. Usually indicates fundamental perception or planning failure rather than dynamic tracking error. |
| **Real Example** | Multiple documented Cruise and Waymo minor collisions with parked vehicles and curbs during pullover maneuvers. Apollo vehicles hitting construction barriers in Wuhan. |
| **Typical Frequency** | Low-Moderate (often low speed, but indicates serious system issues) |
| **Recommended Layer** | **Layer 1** (collision avoidance is fundamental automated safety function) |

**Typical Handling:**
- Automated collision avoidance is a baseline safety function
- Any static object collision triggers immediate disengagement investigation
- Vehicle enters safe stop mode post-collision
- Root cause analysis mandatory before vehicle returns to service

---

### C5 - Low-Speed Pedestrian Collision (低速行人碰撞)

| Field | Value |
|-------|-------|
| **ID** | C5 |
| **Name (EN)** | Low-Speed Pedestrian/Cyclist Collision |
| **Name (CN)** | 低速行人/骑行者碰撞 |
| **Description** | Vehicle contacts a pedestrian or cyclist at low speed — during pullover, parking, creeping through intersection, or in parking lot. Includes entrapment scenarios where pedestrian is trapped under or against vehicle. |
| **Real Example** | ROAM-2023-001: Cruise SF pedestrian dragging — vehicle ran over and dragged a pedestrian 20 feet during post-collision pullover maneuver. |
| **Typical Frequency** | Rare (but highest consequence single-vehicle scenario) |
| **Recommended Layer** | **Layer 1** (automated emergency stop on contact detection); **Layer 3** (emergency services dispatch) |

**Typical Handling:**
- Immediate automated emergency stop on any pedestrian/cyclist contact
- Automatic emergency services notification
- Remote operator confirms scene status and coordinates response
- Vehicle locked in place until emergency services clear

---

## D. Vehicle Hardware Failure (车辆硬件故障)

Anomalies caused by failure of vehicle hardware components — sensors, powertrain, battery, or actuators.

### D1 - Sensor Hardware Failure (传感器硬件故障)

| Field | Value |
|-------|-------|
| **ID** | D1 |
| **Name (EN)** | Sensor Hardware Failure |
| **Name (CN)** | 传感器硬件故障 |
| **Description** | Physical failure of one or more perception sensors — LiDAR unit malfunction, camera lens obstruction/failure, radar hardware fault, or IMU drift. Reduces perception coverage and may create blind spots. |
| **Real Example** | Documented across multiple operators. LiDAR units particularly susceptible to vibration-induced failure. Camera lens contamination in rain/dust common. |
| **Typical Frequency** | Moderate (individual sensor failures relatively common; full redundancy loss rare) |
| **Recommended Layer** | **Layer 1** (automated ODD restriction based on remaining sensor coverage) |

**Typical Handling:**
- Real-time sensor health monitoring detects failure immediately
- AI calculates remaining perception coverage
- If coverage is above minimum threshold: reduce ODD (lower speed, avoid complex scenarios)
- If below threshold: safe stop and dispatch maintenance vehicle

---

### D2 - Powertrain/Battery Failure (动力/电池故障)

| Field | Value |
|-------|-------|
| **ID** | D2 |
| **Name (EN)** | Powertrain/Battery Failure |
| **Name (CN)** | 动力/电池故障 |
| **Description** | Loss of propulsion — electric motor failure, battery management system fault, high-voltage disconnect, or unexpected range depletion leaving vehicle stranded. |
| **Real Example** | No specific ROAM incident yet. EV range anxiety and battery management issues documented across the broader EV fleet. |
| **Typical Frequency** | Low (modern EV powertrains are highly reliable) |
| **Recommended Layer** | **Layer 2** (AI navigates to nearest safe stop, operator coordinates recovery) |

**Typical Handling:**
- Continuous powertrain health monitoring
- Low battery triggers proactive end-of-trip routing to charging station
- If propulsion lost mid-trip: coast to safe stop, hazard lights, unlock doors
- Operator dispatches tow truck or mobile charging unit

---

### D3 - Vehicle Fire (车辆火灾)

| Field | Value |
|-------|-------|
| **ID** | D3 |
| **Name (EN)** | Vehicle Fire |
| **Name (CN)** | 车辆火灾 |
| **Description** | Battery thermal runaway, electrical short circuit, or other fire event. Immediate life safety risk to passengers and surrounding vehicles/structures. |
| **Real Example** | No ROAM-specific incident. Multiple EV fire incidents documented industry-wide; thermal runaway risk is a known concern for high-voltage battery packs. |
| **Typical Frequency** | Very Rare |
| **Recommended Layer** | **Layer 3** (immediate emergency services dispatch, highest priority) |

**Typical Handling:**
- Automated thermal monitoring triggers immediate alert
- Vehicle executes emergency stop, unlocks all doors, opens windows if equipped
- Automatic 911/119 dispatch with GPS coordinates
- Operator provides real-time passenger guidance via intercom
- Surrounding fleet vehicles rerouted away from scene

---

### D4 - Brake/Steering Actuator Failure (制动/转向执行器故障)

| Field | Value |
|-------|-------|
| **ID** | D4 |
| **Name (EN)** | Brake/Steering Actuator Failure |
| **Name (CN)** | 制动/转向执行器故障 |
| **Description** | Failure of primary braking or steering actuator. Redundant system must take over. If redundancy also fails, vehicle is in critical uncontrolled state. |
| **Real Example** | No specific ROAM incident. Covered under ISO 26262 functional safety ASIL-D requirements for by-wire systems. |
| **Typical Frequency** | Very Rare (by design — dual redundancy required by safety standards) |
| **Recommended Layer** | **Layer 1** (automated failover to redundant actuator + safe stop) |

**Typical Handling:**
- Redundant actuator takes over immediately (<50ms failover)
- Vehicle enters degraded mode: reduced speed, straight-line driving priority
- Automated safe stop at earliest safe location
- Vehicle removed from service for hardware inspection
- If both primary and redundant fail: mechanical/hydraulic backup (if equipped)

---

## E. External Conflict (外部环境冲突)

Anomalies caused by external events or road users that the ADS must respond to, but which originate outside the vehicle's control.

### E1 - Struck by Other Vehicle (被其他车辆撞击)

| Field | Value |
|-------|-------|
| **ID** | E1 |
| **Name (EN)** | Struck by Other Vehicle |
| **Name (CN)** | 被其他车辆撞击 |
| **Description** | Robotaxi is hit by another vehicle — rear-ended at stop, T-boned at intersection, sideswiped during lane change. ADS may have no ability to avoid the collision. Post-collision response is critical. |
| **Real Example** | ROAM-2023-001 (secondary): pedestrian initially struck by human-driven vehicle was thrown into path of Cruise robotaxi. Multiple documented rear-end collisions of stopped AVs. |
| **Typical Frequency** | Moderate (AVs are disproportionately rear-ended due to conservative driving) |
| **Recommended Layer** | **Layer 1** (automated post-collision protocol) escalating to **Layer 3** (emergency response) |

**Typical Handling:**
- Automated post-collision protocol: stop, hazard lights, assess damage, unlock doors
- Automated crash notification to emergency services (eCall/bCall)
- Operator reviews scene via cameras, confirms passenger status
- If passengers injured: Layer 3 emergency dispatch
- If vehicle drivable: operator may remotely move to safer location

---

### E2 - Road Construction/Closure (道路施工/封闭)

| Field | Value |
|-------|-------|
| **ID** | E2 |
| **Name (EN)** | Road Construction/Closure |
| **Name (CN)** | 道路施工/封闭 |
| **Description** | Vehicle encounters unexpected road construction, temporary closure, detour, or modified lane configuration not reflected in current map data. Includes temporary traffic control (flaggers, cones, barriers). |
| **Real Example** | Widely documented across all operators. San Francisco construction zones are a known challenge area. Wuhan rapid infrastructure development creates frequent map mismatches. |
| **Typical Frequency** | High (daily occurrence for large fleets in construction-active cities) |
| **Recommended Layer** | **Layer 2** (AI proposes reroute, operator confirms if construction worker gestures are ambiguous) |

**Typical Handling:**
- If closure is detected early: AI reroutes automatically (Layer 1)
- If vehicle is already in construction zone: AI attempts to follow temporary markings
- If temporary traffic control is ambiguous: escalate to Layer 2
- Operator interprets flagger gestures or temporary signage via camera feed
- Post-event map update to prevent repeat encounters

---

### E3 - Emergency Vehicle Blocking (紧急车辆阻塞)

| Field | Value |
|-------|-------|
| **ID** | E3 |
| **Name (EN)** | Emergency Vehicle Interaction |
| **Name (CN)** | 紧急车辆交互 |
| **Description** | Vehicle encounters active emergency scene — needs to yield to approaching emergency vehicles, navigate around parked fire trucks/ambulances, or is blocked by emergency cordon. Failure to yield properly is both dangerous and illegal. |
| **Real Example** | ROAM-2026-002: Waymo Austin ambulance blocking — vehicle failed to properly yield and navigate around an active emergency scene. SF reports of AVs driving into active emergency zones. |
| **Typical Frequency** | Moderate |
| **Recommended Layer** | **Layer 2** (AI detects emergency vehicles, operator confirms appropriate response) |

**Typical Handling:**
- Siren/light detection triggers emergency vehicle response mode
- AI pulls over to nearest safe location and waits
- If blocked by emergency scene: operator assesses and commands reroute
- If emergency personnel direct traffic: operator interprets gestures (Layer 2/3)
- Compliance with local emergency vehicle yield laws is mandatory

---

### E4 - Police/Traffic Officer Gesture Failure (交警手势理解失败)

| Field | Value |
|-------|-------|
| **ID** | E4 |
| **Name (EN)** | Police/Traffic Officer Gesture Failure |
| **Name (CN)** | 交警手势理解失败 |
| **Description** | Vehicle fails to understand or respond to manual traffic direction by police officer or traffic controller. Especially common in China where traffic police manually direct at major intersections during peak hours or after signal failures. |
| **Real Example** | Common operational challenge in Chinese deployments. No specific ROAM incident documented but widely acknowledged as an unsolved problem for L4 systems. |
| **Typical Frequency** | Moderate-High (in markets with manual traffic direction) |
| **Recommended Layer** | **Layer 2** (operator interprets gestures and sends proceed/stop commands) |

**Typical Handling:**
- AI detects presence of traffic officer (uniform, gesture recognition)
- If gestures are recognized with high confidence: follow gestures (Layer 1)
- If confidence is low: stop and escalate to Layer 2
- Operator watches camera feed, interprets gestures, sends commands
- Long-term: gesture recognition model improvement through data collection

---

## F. Passenger-Side Issue (乘客端异常)

Anomalies originating from or primarily affecting passengers. These scenarios require the operations platform to balance passenger safety, comfort, and operational efficiency.

### F1 - Passenger Trapped in Vehicle (乘客被困车内)

| Field | Value |
|-------|-------|
| **ID** | F1 |
| **Name (EN)** | Passenger Trapped in Vehicle |
| **Name (CN)** | 乘客被困车内 |
| **Description** | Passenger cannot exit the vehicle — doors locked due to system error, child lock engaged inappropriately, vehicle stopped in unsafe location where doors should not open (highway, flooded area), or door mechanism physically jammed. |
| **Real Example** | ROAM-2026-004: Wuhan mass shutdown — passengers trapped in stationary vehicles on elevated highway with SOS button unresponsive. Widely reported as the most distressing passenger experience. |
| **Typical Frequency** | Low (but extremely high passenger distress and regulatory risk) |
| **Recommended Layer** | **Layer 2** (operator remotely unlocks doors after safety check) escalating to **Layer 3** (emergency dispatch) |

**Typical Handling:**
- Passenger presses SOS button or calls support
- Operator assesses safety of door opening (location, traffic, weather)
- If safe: remote door unlock
- If unsafe to exit (highway, flooding): operator communicates with passenger, dispatches help
- If door mechanism fails: emergency dispatch (fire department for extraction)
- Maximum acceptable trapped duration: 5 minutes before emergency escalation

---

### F2 - Dangerous Pickup/Dropoff Location (危险接驳位置)

| Field | Value |
|-------|-------|
| **ID** | F2 |
| **Name (EN)** | Dangerous Pickup/Dropoff Location |
| **Name (CN)** | 危险接驳位置 |
| **Description** | Vehicle selects or is directed to a pickup/dropoff point that is unsafe — bus lane, highway shoulder, blind curve, double-parked blocking traffic, no sidewalk access, or flooded/obstructed curb. |
| **Real Example** | Frequently documented in Waymo and Apollo operations. Vehicles stopping in active traffic lanes for passenger pickup/dropoff. Complaints about inaccessible dropoff locations for elderly/disabled passengers. |
| **Typical Frequency** | High (one of the most common operational complaints) |
| **Recommended Layer** | **Layer 1** (AI selects safe pickup/dropoff points from pre-validated database) |

**Typical Handling:**
- Pre-validated pickup/dropoff point database for each service area
- AI selects nearest safe point, considering time of day, traffic, and construction
- If no safe point available within reasonable distance: operator assists (Layer 2)
- Passenger app shows exact pickup point with walking directions
- Post-trip feedback loop improves point database

---

### F3 - Passenger Interference with Vehicle (乘客干扰车辆)

| Field | Value |
|-------|-------|
| **ID** | F3 |
| **Name (EN)** | Passenger Interference with Vehicle |
| **Name (CN)** | 乘客干扰车辆 |
| **Description** | Passenger deliberately or accidentally interferes with vehicle operation — pulling emergency brake, blocking sensors from inside, opening doors while moving, placing objects on sensors, vandalism, or refusing to exit at destination. |
| **Real Example** | Documented in Cruise and Waymo operations — passengers pulling emergency stop handles, placing items over interior cameras, attempting to "test" the AV system. |
| **Typical Frequency** | Low-Moderate |
| **Recommended Layer** | **Layer 2** (operator communicates with passenger via intercom) escalating to **Layer 3** (security dispatch) |

**Typical Handling:**
- Interior monitoring detects interference behavior
- Operator communicates with passenger via intercom (Layer 2)
- If interference continues: safe stop, request passenger exit
- If passenger refuses or becomes threatening: security/police dispatch (Layer 3)
- Post-incident account review and potential service ban

---

### F4 - Passenger Medical Emergency (乘客医疗紧急情况)

| Field | Value |
|-------|-------|
| **ID** | F4 |
| **Name (EN)** | Passenger Medical Emergency |
| **Name (CN)** | 乘客医疗紧急情况 |
| **Description** | Passenger experiences a medical emergency during trip — cardiac event, seizure, loss of consciousness, allergic reaction, or childbirth. No safety driver present to assist. Vehicle must facilitate fastest possible emergency response. |
| **Real Example** | No specific ROAM incident yet. Anticipated as fleet scale increases. Medical emergency protocols are a regulatory requirement in many jurisdictions. |
| **Typical Frequency** | Rare (but frequency increases linearly with fleet size and trip volume) |
| **Recommended Layer** | **Layer 3** (immediate emergency services dispatch + reroute to nearest hospital) |

**Typical Handling:**
- Passenger presses SOS button or interior monitoring detects distress
- Operator assesses situation via camera and intercom
- Automatic 911/120 dispatch with vehicle location and passenger condition
- AI reroutes to nearest hospital emergency entrance
- Operator maintains voice contact with passenger until help arrives
- If passenger is unconscious: emergency stop at nearest safe location, doors unlocked for first responders

---

## Cross-Reference: Scenario-to-Layer Mapping Summary

| ID | Scenario | Primary Layer | Escalation Layer |
|----|----------|:------------:|:----------------:|
| A1 | Cloud/Network Mass Failure | 1 | 3 |
| A2 | OTA Update Failure | 2 | 3 |
| A3 | External Infrastructure Failure | 2 | 3 |
| A4 | Server Decision System Crash | 1 | 3 |
| B1 | Complex Intersection Hesitation | 1 | 2 |
| B2 | Object Misidentification | 1 | 2 |
| B3 | Extreme Weather Degradation | 1 | 2 |
| B4 | Abnormal Human Behavior | 1 | 2 |
| B5 | GPS/Localization Drift | 1 | 2 |
| C1 | Mid-Road Freeze | 2 | 3 |
| C2 | Unexpected Hard Braking | 1 | — |
| C3 | Dangerous Lane Change | 1 | — |
| C4 | Static Object Collision | 1 | 3 |
| C5 | Low-Speed Pedestrian Collision | 1 | 3 |
| D1 | Sensor Hardware Failure | 1 | 2 |
| D2 | Powertrain/Battery Failure | 2 | 3 |
| D3 | Vehicle Fire | 3 | — |
| D4 | Brake/Steering Actuator Failure | 1 | 3 |
| E1 | Struck by Other Vehicle | 1 | 3 |
| E2 | Road Construction/Closure | 2 | 3 |
| E3 | Emergency Vehicle Interaction | 2 | 3 |
| E4 | Police Gesture Failure | 2 | 3 |
| F1 | Passenger Trapped | 2 | 3 |
| F2 | Dangerous Pickup/Dropoff | 1 | 2 |
| F3 | Passenger Interference | 2 | 3 |
| F4 | Passenger Medical Emergency | 3 | — |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-02 | Initial release: 6 categories, 26 sub-scenarios |

## Contributing

To propose a new sub-scenario or modify an existing one, see [CONTRIBUTING.md](../CONTRIBUTING.md).
