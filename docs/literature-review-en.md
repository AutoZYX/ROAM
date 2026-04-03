# Literature Review: Remote Operations and Safety Management for L4 Robotaxis

---

> Author: [Yuxin Zhang](https://www.linkedin.com/in/zhangyuxin/)
> Date: April 2026
> Document Version: v1.0

---

## Abstract

Remote operations constitute a critical enabling capability for the large-scale commercial deployment of Level 4 (L4) robotaxis. As companies including Waymo, Baidu Apollo, and Tesla accelerate the commercialization of driverless mobility, fundamental questions surrounding Remote Operations Center (ROC) architecture design, communication reliability, operator-to-vehicle ratio economics, and systemic failure emergency response have become increasingly urgent. Three recent incidents underscore the fragility of current remote operations frameworks under extreme conditions: the Cruise pedestrian dragging accident in October 2023 [1], the Waymo San Francisco network outage in December 2025 [2], and the Baidu Apollo Go mass shutdown in Wuhan in March 2026 [3][4]. Concurrently, multiple regulatory tracks -- UN WP29/GRVA, China's national standards, US NHTSA, the UK Automated Vehicles Act, and Germany's remote driving ordinance -- are converging toward operational requirements that directly implicate remote operations. This review systematically examines the international regulatory landscape, industry practices in remote operations architecture, academic research frontiers, and accident data. It identifies critical research gaps and articulates the positioning of the ROAM (RoboTaxi Operations Anomaly Management) project within this evolving domain.

---

## 1 Introduction

L4 Automated Driving Systems (ADS) operate without human driver intervention within their defined Operational Design Domain (ODD), yet their large-scale commercial deployment continues to face substantial practical challenges. Remote operations serve as the essential bridge between autonomous vehicles and human supervisors, fulfilling indispensable roles in anomalous scenario handling, passenger services, fleet dispatch, and emergency intervention.

Several recent incidents have sounded alarm bells across the industry. In October 2023, a Cruise autonomous vehicle struck and dragged a pedestrian in San Francisco. The remote operator failed to intervene effectively in time, leading to a full fleet recall and a $1.5 million fine [1]. In December 2025, Waymo experienced a regional network outage in San Francisco that left a portion of its fleet in a communication-disrupted state [2]. On March 31, 2026, Baidu Apollo's robotaxi service Apollo Go suffered a mass system shutdown in Wuhan, exposing systemic deficiencies including the absence of a dedicated roadside assistance team, ineffective remote intervention mechanisms, non-functional SOS buttons, and an overwhelmed customer service system [3][4].

These events demonstrate that current L4 robotaxi remote operations frameworks remain significantly deficient in system resilience, emergency response, and human-machine collaboration. These deficiencies define the core problem domain of this review.

## 2 International Regulatory Landscape

### 2.1 UN WP29/GRVA Framework

The Working Party on Automated/Autonomous and Connected Vehicles (GRVA), operating under the United Nations World Forum for Harmonization of Vehicle Regulations (WP.29), serves as the central global platform for ADS regulatory coordination. In January 2026, GRVA adopted a draft Global Technical Regulation (GTR) on Automated Driving Systems at its 22nd session [5]. The GTR's core requirements stipulate that ADS performance must meet or exceed that of a "competent and careful human driver," and that deployers must submit a Safety Case incorporating a Safety Management System (SMS) [6]. The GTR is expected to receive formal adoption in June 2026 [7].

The framework carries implicit requirements for remote operations: the Safety Case must address risk analysis and mitigation measures pertaining to remote operations, and the SMS must encompass operational protocols for Remote Operations Centers.

### 2.2 China's Standards

China's regulatory progress on autonomous driving has accelerated considerably, establishing a dual-layer architecture of national standards and local legislation.

At the national level, the draft standard GB XXXXX--XXXX "Intelligent and Connected Vehicles -- Safety Requirements for Automated Driving Systems" [Zhinian Wanglian Qiche -- Zidong Jiashi Xitong Anquan Yaoqiu] was published for public comment in February 2026 [8]. Appendix C.2 of this standard specifically defines remote assistance requirements for L4 systems, with significant implications:

- **C.2.1.2** explicitly stipulates that ADS shall not rely on remote assistance to perform the Dynamic Driving Task (DDT) -- remote assistance supplements rather than substitutes for autonomous capability;
- **C.2.2** establishes communication requirements covering signal strength, latency, and jitter detection metrics, mandating activation of a Minimal Risk Maneuver (MRM) upon communication failure;
- **C.2.3** specifies information exchange content, including vehicle status, ADS status, environmental information, and command confirmation;
- **C.2.1.4** requires ADS to respond to remote commands based on assessed driving environment safety rather than executing them unconditionally.

Appendix D of the standard defines the Safety Case structure, including hazard analysis and residual risk acceptance criteria. Residual risk targets are set at: collision rate below 10^-4/h, minor injury rate below 10^-5/h, severe injury rate below 10^-6/h, and fatality rate below 10^-7/h [8]. The standard further mandates that L3/L4 vehicles be equipped with a Data Storage System for Automated Driving (DSSAD). This mandatory national safety standard takes effect on July 1, 2027 [8].

Regarding remote operator-to-vehicle ratios, current Chinese regulations set a maximum of 1:3 (one safety operator supervising at most three vehicles) [9].

At the local legislation level, Shenzhen enacted the "Shenzhen Special Economic Zone Regulations on the Management of Intelligent and Connected Vehicles" [Shenzhen Jingji Tequ Zhinian Wanglian Qiche Guanli Tiaoli] in 2022, becoming China's first comprehensive legislation governing connected autonomous vehicles [10]. The "Beijing Autonomous Vehicle Regulations" [Beijing Shi Zidong Jiashi Qiche Tiaoli] took effect in April 2025, providing a legal framework for road testing and demonstration applications [11].

### 2.3 US NHTSA

The National Highway Traffic Safety Administration (NHTSA) has adopted a data-driven regulatory approach. Its Standing General Order (SGO) requires that crashes involving ADS in an activated state be reported within 30 seconds [12]. In April 2025, NHTSA released its AV framework articulating three foundational principles: ensure safety, remove barriers, and promote deployment [13]. The framework streamlined crash reporting procedures while maintaining safety baselines, creating greater policy flexibility for industry development [14].

### 2.4 UK Automated Vehicles Act

The United Kingdom passed the Automated Vehicles Act 2024 on May 20, 2024, establishing a relatively comprehensive liability allocation framework [15]. The Act created the role of "Authorised Self-Driving Entity" (ASDE) and explicitly distinguished between two operational modes: "User-in-Charge" (UIC) and "No-User-in-Charge" (NUIC) [16]. The safety standard is defined as "equal to or higher than careful and competent human drivers" [15]. Commercial pilot operations carrying paying passengers are expected to commence in spring 2026 [17].

The UK Act's ASDE model represents the clearest liability delineation in current global regulation, offering an important reference point for legal responsibility allocation in remote operations.

### 2.5 German StVFernLV

Germany published the "Ordinance on Remote Driving of Motor Vehicles on Public Roads" (Stra&szlig;enverkehrs-Fernlenkungs-Verordnung, StVFernLV) on December 1, 2025, becoming Europe's first regulatory framework for teleoperated driving [18]. The ordinance permits remote-controlled vehicles to operate at speeds up to 80 km/h within approved zones, with a five-year trial period [19]. Vay Technology plans to launch commercial driverless carsharing services under this framework [20].

What distinguishes this regulation is its explicit coverage of the remote "direct control" mode, rather than limiting scope to remote assistance alone -- a notable departure from the regulatory orientation of other jurisdictions.

### 2.6 Japan SIP-adus

Japan's Cross-ministerial Strategic Innovation Promotion Program for Automated Driving for Universal Services (SIP-adus), launched in 2014, incorporates remote monitoring and control as essential capability requirements for automated driving buses [21]. The program has conducted systematic field operational tests through the coordination of Roadside Units (RSU) and vehicle-mounted cameras [22]. Japan's practical experience offers valuable insights for remote operations in low-speed autonomous driving scenarios.

### 2.7 SAE/ISO Standards

SAE J3016 was updated in May 2024 (jointly published with ISO), adding terminology definitions related to Remote Support [23]. Notably, the standard deliberately avoids the term "teleoperation" due to significant semantic inconsistencies across different contexts [23].

ISO 22737:2021 defines operational requirements for low-speed automated driving systems on predefined routes, with a maximum speed limit of 32 km/h, and introduces the role of "Driverless Operation Dispatcher" [24]. This standard provides a normative foundation for remote operations in low-speed closed or semi-closed environments.

## 3 Industry Practice: Remote Operations Architecture

### 3.1 Waymo Fleet Response

Waymo's remote operations employ an advisory model whose core principle is that the ADS maintains full vehicle control at all times, with remote personnel providing only contextual information to support decision-making -- analogous to a "phone-a-friend" paradigm [25].

As of late 2025, Waymo operates over 3,000 vehicles with approximately 70 on-duty remote agents, yielding an operator-to-vehicle ratio of roughly 1:41 [26]. Its Remote Operations Centers are distributed across Arizona, Michigan, and two sites in the Philippines [25]. In terms of operational scale, Waymo completes over 400,000 paid trips per week with cumulative autonomous mileage exceeding 4 million miles [26]. In November 2025, Waymo published an independent safety audit report [27].

Regarding communication latency, the median latency from US-based operations centers is approximately 150 ms, compared with approximately 250 ms from the Philippines centers [26]. Whether this cross-border latency differential affects decision quality warrants further investigation.

### 3.2 Tesla Teleops

Tesla launched its teleoperation service in Austin in June 2025, transitioning to unsupervised vehicle operations in January 2026 [28]. Unlike Waymo's advisory model, Tesla's remote operators can assume full vehicle control in extreme situations, limited to speeds below 10 mph [29]. Tesla is developing a custom teleoperation system with plans to expand to seven cities in H1 2026 [30].

Tesla's technical approach reflects a fundamental divergence between "direct control" and "advisory assistance" paradigms. Under the direct control model, the impact of communication latency and bandwidth on safety becomes substantially more critical.

### 3.3 Baidu Apollo Go

Baidu Apollo's robotaxi service Apollo Go completed over 3.4 million orders in Q4 2025 [31]. However, the mass system shutdown in Wuhan on March 31, 2026 exposed systemic deficiencies in its remote operations: the absence of a professional roadside assistance team, substantially ineffective remote intervention capabilities, and ultimate reliance on traffic police for on-site incident management [3]. Passenger-side SOS buttons failed to function, and the customer service system became severely overloaded [4].

This incident exhibits the hallmarks of a systemic failure -- not an isolated malfunction of a single vehicle, but the simultaneous incapacitation of an entire fleet. Such scenarios are inadequately addressed in any operator's existing emergency protocols, representing one of the most pressing research challenges in remote operations.

### 3.4 Teleoperation Startups

Remote operations technology is fostering a specialized startup ecosystem. Vay Technology deployed 30 rental vehicles in Las Vegas in February 2025, completing over 17,000 trips by July 2025 [32]. Ottopia has developed an AI-powered teleoperation platform supporting collaborative human-machine remote intervention [33]. GetUgo focuses on communication security, providing end-to-end encrypted teleoperation communication solutions [33]. An estimated 13 companies globally operate in the autonomous vehicle teleoperation space [34].

The divergent technical approaches of these startups reflect the absence of unified industry standards and established best practices in remote operations.

## 4 Academic Research Frontiers

### 4.1 Network Latency and Communication

Communication latency represents the core technical bottleneck for teleoperation. A systematic review published in MDPI Sensors in 2024 comprehensively analyzed network latency challenges in the teleoperation of connected and automated vehicles, synthesizing latency mitigation and compensation strategies [35]. The study found that remote operator driving performance degrades significantly when end-to-end latency exceeds 300 ms, while current cellular networks exhibit substantial latency variance in urban environments -- imposing a fundamental constraint on real-time control modes.

### 4.2 Indirect Control

Addressing the limitations of direct steering control under high-latency conditions, the research community has proposed indirect control approaches. A study published in Springer's International Journal of Automotive Technology in 2025 explored waypoint-setting-based tele-operated driving assistance as an alternative to direct steering [36]. This method elevates the remote operator's role from low-level continuous control to high-level path planning decisions, effectively reducing sensitivity to communication latency.

### 4.3 Control Center Framework

The Institute of Automotive Technology (FTM) at the Technical University of Munich presented a Control Center Framework for teleoperation support of automated vehicles on public roads at the 2025 IEEE Intelligent Vehicles Symposium (IV) [37]. The framework proposes a modular control center architecture encompassing situation awareness, communication management, and task allocation modules, providing a reference baseline for the engineering realization of Remote Operations Centers.

### 4.4 Comprehensive Surveys

Lu et al. published a survey in IEEE in 2022 that systematically reviewed teleoperation technologies for enhancing the performance of connected and autonomous vehicles [38]. The survey covered communication architectures, human-machine interaction interfaces, and safety mechanisms across multiple dimensions, and remains one of the more highly cited foundational works in the field.

Current academic research exhibits notable gaps: strategies for remote operations during systemic failure scenarios remain understudied, theoretical models for operator-to-vehicle ratio optimization have yet to be established, and the quantitative impact of cross-border operations center latency on decision quality awaits empirical validation.

## 5 Accident Data Analysis

Accident data provides essential evidence for evaluating the effectiveness of remote operations. According to NHTSA data, Waymo reported 1,429 accidents between July 2021 and November 2025, involving 117 injuries and 2 fatalities [39]. Given its cumulative autonomous mileage exceeding 4 million miles, these figures require comparative analysis against human driver accident rates under equivalent operational conditions.

Following the October 2023 pedestrian dragging incident, Cruise implemented a full fleet recall and was assessed a $1.5 million fine by NHTSA [1]. The response delay and intervention decision-making process of the remote operator in this incident exposed critical deficiencies at the human-machine interaction level.

In China, Pony.ai experienced a vehicle fire incident in Beijing that resulted in a temporary service suspension [40]. Baidu Apollo's mass shutdown and pedestrian collision incidents in Wuhan further highlighted the vulnerability of remote operations under high-density deployment conditions [3].

These accident data reveal a common pattern: remote operations systems perform acceptably under routine conditions but exhibit inadequate emergency capacity when anomalous scenarios compound -- network failures, extreme weather, system software defects, and similar concurrent stressors. This is precisely the residual risk interval that demands the closest scrutiny in safety case argumentation.

## 6 Key Challenges and Research Gaps

Based on the regulatory, practical, and academic analysis presented above, this review identifies six key challenges and research gaps:

**First, the absence of systemic failure emergency response capability.** The March 2026 Apollo Go shutdown in Wuhan demonstrates that no current operator possesses an effective response plan for simultaneous multi-vehicle fleet failures. Existing emergency protocols are designed primarily for single-vehicle faults; scenarios in which software defects, network disruptions, or other common-cause failures render an entire fleet inoperative simultaneously lack systematic contingency architectures.

**Second, conceptual divergence between remote assistance and remote driving.** SAE J3016 deliberately avoids the term "teleoperation"; ISO 22737 defines the "Driverless Operation Dispatcher" role; and the Chinese GB standard employs the term "remote assistance" [yuancheng xiezhu]. In practice, Waymo operates an advisory model while Tesla permits direct control. This inconsistency in terminology and practice increases the complexity of cross-border regulatory harmonization and safety assessment.

**Third, the economic gap in operator-to-vehicle ratios.** Waymo's ratio of approximately 1:41 and China's regulatory maximum of 1:3 differ by more than an order of magnitude [9][26]. How to reduce manual intervention ratios through AI-assisted decision-making, automated event triage, and similar technological means while maintaining safety levels represents a critical challenge for commercial sustainability.

**Fourth, communication security and latency constraints.** Waymo's Philippines-based operations center exhibits a median latency of approximately 250 ms, substantially higher than the approximately 150 ms from domestic centers [26]. 5G and V2X deployment across Chinese cities remains uneven. Communication security (against hijacking and tampering) and deterministic end-to-end latency guarantees are foundational prerequisites for large-scale remote operations deployment.

**Fifth, ambiguity in legal liability allocation.** The UK's ASDE model represents the most clearly delineated liability framework in current global regulation, but China remains in a phase of exploratory local legislation without a formed national-level liability allocation framework. When a remote operator's command leads to an accident, whether liability attaches to the individual operator, the operating company, or the ADS developer remains unresolved in most jurisdictions.

**Sixth, the absence of naturalistic driving behavior baselines.** The residual risk criteria in the Chinese GB standard (collision rate below 10^-4/h, etc.) require human driver behavioral baseline data as a reference. However, credible large-scale naturalistic driving behavior datasets for specific Chinese urban traffic scenarios remain scarce, constraining the scientific rigor of residual risk assessment.

## 7 Future Outlook: From Remote Operations to "Robotaxi Rescue Insurance"

### 7.1 Structural Parallels with Traditional Auto Insurance

The current automotive insurance industry has established a mature roadside assistance model: after an accident, the driver calls the insurer, who dispatches an adjuster, arranges towing, coordinates repairs, and processes claims. The essence of this chain is **risk pooling and scalable emergency response** — no individual car owner can economically maintain a dedicated rescue team; insurers aggregate premiums from a large pool of policyholders to sustain a 24/7 response network.

L4 robotaxi remote operations face a structurally identical economic problem. Each operator currently builds independent remote operations centers in every city of deployment. However, as robotaxi services scale from pilot programs in a handful of cities to nationwide or global operations, the cost of maintaining dedicated remote operations teams in each city will become increasingly untenable. Just as car owners cannot afford their own repair crews, robotaxi operators maintaining city-by-city remote operations teams will face diminishing economic viability at scale.

### 7.2 A Three-Layer Service Architecture

Based on this analysis, future robotaxi remote operations may differentiate into three service layers:

**Layer 1: Remote Operations as a Service (ROaaS).** This is the core business model described by ROAM's reference architecture. A third-party platform provides 24/7 remote monitoring, AI-assisted decision-making, and anomaly resolution for multiple operators and OEMs, charged per vehicle-month or per incident. The commercial logic mirrors AAA roadside assistance or China's 12122 traffic rescue service — multi-brand vehicles sharing a common rescue infrastructure.

**Layer 2: Incident Response Insurance.** When remote intervention cannot resolve the situation (e.g., hardware failure, traffic accident, passenger injury), on-site teams are required. This segment directly overlaps with traditional auto insurance functions: loss assessment, towing, and claims processing. Insurance companies can serve as underwriters while remote operations platforms serve as execution partners, creating an "insurance + operations" synergy. Standardized coverage can be designed for passenger relocation, alternative transportation, and medical transfer.

**Layer 3: Data-Driven Risk Pricing.** This is where the true insurance logic emerges. As ROAM's incident database and scenario taxonomy accumulate sufficient scale, they can enable differentiated accident rate and risk probability calculations across operators, ADS systems, and urban environments. Specifically:

- **Exposure rate calculation**: Naturalistic driving data provides the denominator (normal driving miles/hours); accident data provides the numerator (incident frequency). Together, they yield scenario-specific accident exposure rates.
- **Preventability assessment**: Distinguishing "accidents that human drivers also could not avoid" (force majeure, lower premiums) from "accidents that ADS should have prevented but did not" (system deficiency, higher premiums), enabling differentiated pricing by accident type.
- **Operator rating**: Rating different operators' remote operations capability based on historical incident data, with ratings directly influencing premium levels.

### 7.3 Early Industry Practice

Globally, robotaxi insurance exploration has already begun. Waymo has partnered with Swiss Re to leverage autonomous driving operational data for insurance pricing model optimization [41]. The UK Automated Vehicles Act 2024 explicitly requires ASDEs to hold liability insurance [15]. In China, major insurers including Ping An and PICC are actively exploring intelligent connected vehicle insurance product design [42].

However, current efforts face a common challenge: **the absence of standardized incident data and risk assessment frameworks.** Accident reporting formats differ across operators, severity and preventability assessment criteria are undefined, and insurers cannot build comparable actuarial models.

### 7.4 ROAM's Position in the Insurance Ecosystem

ROAM's four modules correspond precisely to critical infrastructure needs in the robotaxi insurance ecosystem:

| ROAM Module | Role in Insurance Ecosystem |
|-------------|----------------------------|
| Incident Database | Claims case library and actuarial data source |
| Scenario Taxonomy | Risk classification and premium pricing framework |
| Reference Architecture | Technical standards for remote operations service providers (insurance execution partners) |
| Evaluation Benchmarks | Operator capability rating and premium differentiation metrics |

DRIVEResearch's aerial naturalistic driving dataset (750h+ flight hours, 10.5M+ trajectories) serves as the "healthy population baseline" in this ecosystem — just as health insurers need normal population health metrics to identify anomalies, robotaxi insurers need naturalistic driving behavior baselines to distinguish "reasonable residual risk" from "unreasonable system deficiency."

### 7.5 Timeline Outlook

The maturation of this ecosystem requires several prerequisites to fall into place:

- **Near-term (2026–2028)**: Remote operations systems across operators gradually standardize; GB standard safety case and residual risk criteria enter implementation; open-source projects like ROAM accumulate structured incident data.
- **Mid-term (2028–2030)**: Third-party remote operations service providers emerge; insurers launch robotaxi-specific insurance products; data-driven differentiated pricing becomes feasible.
- **Long-term (2030+)**: A three-party collaborative ecosystem forms among operators, remote operations service providers, and insurers. Remote operations platforms become critical nodes in the insurance claims chain, and data-driven risk management becomes industry standard practice.

## 8 ROAM Project Positioning

Based on the analysis presented above, the ROAM (RoboTaxi Operations Anomaly Management) project aims to address critical gaps in this domain. ROAM is positioned as an open-source reference architecture and analytical toolkit, with core contributions spanning four dimensions:

**Incident tracking baseline.** Establishing a structured recording and classification system for L4 robotaxi remote operations incidents, covering communication failures, system shutdowns, human-machine interaction breakdowns, and other representative event types. This provides the industry with a comparable incident analysis framework.

**Scenario taxonomy.** Drawing on the ISO 34502 scenario description methodology, ROAM constructs a scenario classification system (Scenario Taxonomy) for remote operations. This taxonomy maps regulatory requirements, industry practices, and accident data into a searchable scenario repository.

**Reference architecture.** Based on industry best practices and academic frontiers, ROAM proposes a modular reference architecture for Remote Operations Centers supporting flexible configuration across advisory and direct control modes.

**Insurance ecosystem infrastructure.** Through standardized incident records, scenario classification, and evaluation benchmarks, ROAM provides the data foundation and methodological support for future robotaxi insurance product actuarial pricing and claims execution.

DRIVEResearch's aerial-survey naturalistic driving dataset (750h+ flight hours, 10.5M+ trajectories) provides behavioral baseline data to support the above research. This dataset can be used to establish human driver behavioral benchmarks for Chinese urban traffic scenarios, creating alignment with the GB standard's residual risk criteria and supporting scenario analysis and known unsafe scenario identification under the SOTIF (ISO 21448) methodology.

The ROAM project will adhere to open-source collaboration principles, providing public knowledge infrastructure for L4 robotaxi remote operations safety management through standardized data formats, modular architecture design, and community-driven iterative development.

---

## References

[1] NHTSA, "Cruise LLC Consent Order and Civil Penalty," National Highway Traffic Safety Administration, 2024. [Link](https://www.nhtsa.gov/press-releases/consent-order-cruise-crash-reporting)

[2] TechCrunch, "Waymo explains why its robotaxis got stuck during the SF blackout," December 2025. [Link](https://techcrunch.com/2025/12/24/waymo-explains-why-its-robotaxis-got-stuck-during-the-sf-blackout/)

[3] Huxiu, "Apollo Go mass shutdown in Wuhan exposes Achilles' heel of robotaxi operations," April 2026. [Link](https://www.huxiu.com/article/4847431.html)

[4] Sina Auto, "Apollo Go Wuhan incident: vehicles restored, industry analysis," April 2026. [Link](https://auto.sina.cn/news/2026-04-01/detail-inhsyfuw2691947.d.html)

[5] UNECE, "ECE-TRANS-WP.29-GRVA-2026-02e: Draft Global Technical Regulation on Automated Driving Systems," United Nations Economic Commission for Europe, January 2026. [Link](https://unece.org/sites/default/files/2026-01/ECE-TRANS-WP.29-GRVA-2026-02e.pdf)

[6] Connected Automated Driving, "UNECE GRVA Adopts Draft Global Regulation on Automated Driving Systems," January 2026. [Link](https://www.connectedautomateddriving.eu/blog/unece-grva-adopts-draft-global-regulation-on-automated-driving-systems/)

[7] U.S. Federal Register, "Notice and Request for Comment; Proposal for a New United Nations Global Technical Regulation on Automated Driving Systems (ADS)," January 2026. [Link](https://www.federalregister.gov/documents/2026/01/23/2026-01274/notice-and-request-for-comment-proposal-for-a-new-united-nations-global-technical-regulation-on)

[8] Ministry of Industry and Information Technology of China, "GB XXXXX--XXXX Intelligent and Connected Vehicles -- Safety Requirements for Automated Driving Systems," Draft for Public Comment, February 2026. Including Appendix C.2 Remote Assistance Requirements and Appendix D Safety Case Requirements. [Link](https://carnewschina.com/2026/02/26/new-chinese-regulations-push-l3-autonomous-vehicles-closer-to-l4-capabilities-with-enhanced-safety-protocols/)

[9] Ministry of Transport of China, "Guidelines for Safe Transportation Services of Autonomous Vehicles (Trial)," December 2023. Remote safety operator-to-vehicle ratio requirement: maximum 1:3. [Link](https://xxgk.mot.gov.cn/2020/jigou/ysfws/202312/t20231205_3962490.html)

[10] Standing Committee of the Shenzhen Municipal People's Congress, "Shenzhen Special Economic Zone Regulations on the Management of Intelligent and Connected Vehicles," August 2022. [Link](https://www.gd.gov.cn/gdywdt/dsdt/content/post_3986167.html)

[11] Standing Committee of the Beijing Municipal People's Congress, "Beijing Autonomous Vehicle Regulations," Effective April 2025. [Link](https://www.beijing.gov.cn/zhengce/dfxfg/202501/t20250103_3980149.html)

[12] NHTSA, "Standing General Order on Crash Reporting for Automated Driving Systems," National Highway Traffic Safety Administration. [Link](https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting)

[13] Mayer Brown, "DOT and NHTSA Announce Autonomous Vehicle Framework," April 2025. [Link](https://www.mayerbrown.com/en/insights/publications/2025/04/dot-and-nhtsa-announce-autonomous-vehicle-framework)

[14] Foley & Lardner LLP, "Driving Into 2026: The State of NHTSA and the Future of Vehicle Safety Regulation," November 2025. [Link](https://www.foley.com/insights/publications/2025/11/driving-into-2026-the-state-of-nhtsa-and-the-future-of-vehicle-safety-regulation/)

[15] UK Parliament, "Automated Vehicles Act 2024," Royal Assent May 20, 2024. [Link](https://www.legislation.gov.uk/ukpga/2024/10)

[16] Hogan Lovells, "UK passes Automated Vehicles Act 2024," 2024. [Link](https://www.hoganlovells.com/en/publications/uk-passes-automated-vehicles-act-2024)

[17] Addleshaw Goddard, "The UK's Automated Vehicles Act 2024," 2024. [Link](https://www.addleshawgoddard.com/en/insights/insights-briefings/2024/transport/passing-self-driving-test-uks-automated-vehicles-act-2024/)

[18] Taylor Wessing, "Legal framework for automated and autonomous driving and teledriving in the EU and Germany," February 2026. [Link](https://www.taylorwessing.com/en/insights-and-events/insights/2026/02/legal-frameworks-for-autonomous-driving-and-teledriving)

[19] Bird & Bird, "Teleoperated Driving -- StVFernLV in force since December 2025," 2026. [Link](https://www.twobirds.com/en/insights/2026/germany/teleoperiertes-fahren-straenverkehr-fernlenk-verordnung-(stvfernlv)-seit-dezember-2025-in-kraft)

[20] Vay Technology, "Vay Welcomes Germany's Remote Driving Regulation," Press Release, 2025. [Link](https://vay.io/press-release/vay-welcomes-germanys-remote-driving-regulation-a-breakthrough-in-remote-driving-commercialization-at-scale/)

[21] SIP-adus (Cross-ministerial Strategic Innovation Promotion Program -- Automated Driving for Universal Services), Cabinet Office of Japan, launched 2014. [Link](https://en.sip-adus.go.jp/)

[22] SIP-adus, "An Update on Japanese Initiatives for Automated Driving," in *Automated Driving*, Springer, 2018. [Link](https://link.springer.com/chapter/10.1007/978-3-319-94896-6_2)

[23] SAE International, "J3016: Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles," May 2024 update (Joint with ISO). See also: MobilityEngTech analysis. [Link](https://www.mobilityengineeringtech.com/component/content/article/44792-sae-ma-06724)

[24] ISO, "ISO 22737:2021 -- Intelligent transport systems -- Low-speed automated driving (LSAD) systems for predefined routes," International Organization for Standardization, 2021. [Link](https://www.iso.org/standard/73767.html)

[25] Waymo Blog, "Fleet response: Lending a helpful hand to Waymo's autonomously driven vehicles," May 2024. [Link](https://waymo.com/blog/2024/05/fleet-response/)

[26] Remio AI, "Waymo Remote Assistance: The Reality of Autonomous Driving," 2025. See also: Futurism related analysis. [Link](https://www.remio.ai/post/waymo-remote-assistance-the-reality-of-autonomous-driving)

[27] Waymo Blog, "Independent Audits of Waymo's Safety Case and Remote Assistance Programs," November 2025. [Link](https://waymo.com/blog/2025/11/independent-audits/)

[28] TechCrunch, "Tesla appears to be building a teleoperations team for its robotaxi service," November 2024. See also: TechCrunch, "Tesla launches robotaxi rides in Austin," June 2025. [Link](https://techcrunch.com/2024/11/26/tesla-appears-to-be-building-a-teleoperations-team-for-its-robotaxi-service/)

[29] Futurism, "Tesla Workers Are Seizing Control of Robotaxis When They Get Stuck," 2025. [Link](https://futurism.com/advanced-transport/tesla-robotaxis-driven-remotely)

[30] Planetizen, "Tesla Reveals Remote Drivers Temporarily Control its Robotaxis," 2026. [Link](https://www.planetizen.com/news/2026/04/137261-tesla-reveals-remote-drivers-temporarily-control-its-robotaxis)

[31] Baidu Investor Relations, "Baidu Announces Fourth Quarter and Fiscal Year 2025 Results," February 2026. [Link](https://ir.baidu.com/news-releases/news-release-details/baidu-announces-fourth-quarter-and-fiscal-year-2025-results)

[32] Vay Technology, "Vay expands service area in Las Vegas," Press Release, 2025. See also: TechCrunch, "Vay expands driverless car-sharing fleet in Las Vegas," January 2025. [Link](https://vay.io/vay-expands-service-area-in-las-vegas/)

[33] StartUs Insights, "5 Top Emerging Teleoperation Startups," 2025. Covering Ottopia (AI-powered teleoperation platform) and GetUgo (end-to-end encrypted communication solution). [Link](https://www.startus-insights.com/innovators-guide/5-top-emerging-teleoperation-startups/)

[34] Tracxn, "Top Companies in Autonomous Vehicles Teleoperation," 2025. [Link](https://tracxn.com/d/trending-business-models/startups-in-autonomous-vehicles-teleoperation/__GS_MwTPd-ARbXrP9dRsdYOTXDe2wOGOsT2hPv2G8ty8/companies)

[35] Hofbauer, M. et al., "Network latency challenges in teleoperation of connected and automated vehicles: A systematic review," *Sensors*, vol. 24, no. 12, p. 3957, 2024. [Link](https://www.mdpi.com/1424-8220/24/12/3957)

[36] Kim, K. et al., "Development of Tele-operated Driving Assistance System for Autonomous Vehicles with an Open-Source Platform," *International Journal of Automotive Technology*, vol. 26, pp. 1379-1390, 2025. [Link](https://link.springer.com/article/10.1007/s12239-025-00218-8)

[37] Wolf, M.-M. et al., "Control center framework for teleoperation support of automated vehicles on public roads," in *Proc. IEEE Intelligent Vehicles Symposium (IV)*, 2025. [Link](https://ieeexplore.ieee.org/document/11097634/)

[38] Lu, S. et al., "Teleoperation technologies for enhancing connected and autonomous vehicles," in *Proc. IEEE 19th International Conference on Mobile Ad Hoc and Smart Systems (MASS)*, 2022. [Link](https://ieeexplore.ieee.org/document/9973618/)

[39] DAM Firm, "Waymo Accidents | NHTSA Crash Data," damfirm.com, 2025. [Link](https://www.damfirm.com/waymo-accident-statistics.html)

[40] EVreporter, "Pony.ai Beijing operations suspended after Robotaxi fire," 2025. [Link](https://evreporter.com/autonomous-driving-startup-pony-ai-beijing-operations-suspended-after-robotaxi-fire/)

[41] Swiss Re, "Waymo and Swiss Re partner on autonomous vehicle insurance," 2024. [Link](https://www.swissre.com/reinsurance/property-and-casualty/solutions/automotive-solutions.html)

[42] China Banking and Insurance News, "Intelligent connected vehicle insurance: from traditional auto insurance to data-driven risk management [智能网联汽车保险]," 2025. [Link](https://www.cbimc.cn/)

---

*This literature review serves as a foundational research document for the ROAM project and will be continuously revised as regulations evolve, industry practices advance, and new research findings are published.*
