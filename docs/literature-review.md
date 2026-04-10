# L4级自动驾驶出租车远程运营与安全管理综述

**A Literature Review on Remote Operations, Teleoperation, and Safety Management for L4 Robotaxis**

---

> 作者：[Yuxin Zhang](https://www.linkedin.com/in/zhangyuxin/)
> 日期：2026年4月
> 文档版本：v1.0

---

## 摘要

L4级自动驾驶出租车（Robotaxi）的远程运营是实现大规模商业部署的关键支撑能力。近年来，随着Waymo、百度Apollo、Tesla等企业加速推进无人驾驶商业化，远程运营中心（Remote Operations Center, ROC）的架构设计、通信可靠性、人车配比经济性以及系统性故障应急等问题日益凸显。2023年10月Cruise行人拖拽事故、2025年12月Waymo旧金山断网事件、2026年3月百度萝卜快跑武汉大规模宕机等典型案例，暴露了当前远程运营体系在极端场景下的脆弱性。与此同时，联合国WP29/GRVA、中国国家标准、美国NHTSA、英国自动驾驶法案及德国远程驾驶法规等多条监管路线正在加速收敛。本文系统梳理国际法规进展、行业实践架构、学术研究前沿及事故数据，识别当前研究空白，并阐述ROAM项目的定位与展望。

---

## 1 引言

L4级自动驾驶系统（Automated Driving System, ADS）在设计运行域（Operational Design Domain, ODD）内无需人类驾驶员介入，但其大规模商业部署仍面临诸多现实挑战。远程运营作为连接自动驾驶车辆与人类监管者的桥梁，在异常场景处置、乘客服务、车队调度及紧急干预等方面承担着不可或缺的角色。

近年来的多起事故为该领域敲响了警钟。2023年10月，Cruise公司的自动驾驶车辆在旧金山撞击并拖拽一名行人，远程操作员未能及时有效干预，导致Cruise全面召回车队并被处以150万美元罚款[1]。2025年12月，Waymo在旧金山遭遇区域性网络故障，部分车辆陷入通信中断状态[2]。2026年3月31日，百度Apollo旗下萝卜快跑在武汉发生大规模系统宕机，暴露出其缺乏道路救援团队、远程干预手段失效、SOS按钮无响应、客服系统过载等系统性缺陷[3][4]。

上述事件表明：当前L4级Robotaxi的远程运营体系在系统韧性（System Resilience）、故障应急和人机协同方面仍存在显著不足。这构成了本文综述的核心问题域。

## 2 国际法规与标准进展

### 2.1 联合国WP29/GRVA框架

联合国世界车辆法规论坛（WP.29）下设的自动驾驶与网联车辆工作组（GRVA）是全球自动驾驶法规协调的核心平台。2026年1月，GRVA在第22次会议上通过了自动驾驶系统全球技术法规（Global Technical Regulation, GTR）草案[5]。该GTR的核心要求包括：ADS的表现应至少达到"有能力且谨慎的人类驾驶员"（competent and careful human driver）水平；部署方需提交安全论证（Safety Case），其中包含安全管理体系（Safety Management System, SMS）[6]。该GTR预计于2026年6月正式通过[7]。

这一框架对远程运营的隐含要求在于：安全论证中需覆盖远程运营相关的风险分析与缓解措施，安全管理体系需包含远程运营中心的运行规范。

### 2.2 中国标准体系

中国在自动驾驶法规层面的推进速度正在加快，形成了"国家标准+地方立法"的双层架构。

在国家标准层面，GB XXXXX--XXXX《智能网联汽车 自动驾驶系统安全要求》征求意见稿于2026年2月发布[8]。该标准附录C.2专门定义了L4级远程协助（Remote Assistance）要求，具有重要参考价值：

- **C.2.1.2**明确规定ADS不应依赖远程协助执行动态驾驶任务（DDT），即远程协助是辅助而非替代；
- **C.2.2**提出通信要求，包括信号强度、延迟、抖动检测等指标，并要求在通信失效时触发最小风险策略（Minimal Risk Maneuver, MRM）；
- **C.2.3**规定信息交换内容，涵盖车辆状态、ADS状态、环境信息及指令确认；
- **C.2.1.4**要求ADS基于驾驶环境安全性响应远程指令，而非盲目执行。

该标准附录D定义了安全档案（Safety Case）结构，包括危害分析与残余风险接受准则。残余风险目标值设定为：碰撞率低于10^-4/h，轻伤率低于10^-5/h，重伤率低于10^-6/h，致命率低于10^-7/h[8]。此外，标准要求L3/L4级车辆强制配备自动驾驶数据记录系统（Data Storage System for Automated Driving, DSSAD），该强制性国家安全标准将于2027年7月1日起实施[8]。

在远程运营人车比方面，当前中国法规要求不超过1:3（一名安全员最多监管3辆车）[9]。

在地方立法层面，深圳于2022年率先出台《深圳经济特区智能网联汽车管理条例》，成为中国首部智能网联汽车综合性立法[10]。北京市《自动驾驶汽车条例》于2025年4月正式生效，为自动驾驶车辆的道路测试和示范应用提供了法律框架[11]。

### 2.3 美国NHTSA

美国国家公路交通安全管理局（NHTSA）采用以数据驱动的监管思路。其常规通用命令（Standing General Order, SGO）要求涉及ADS激活状态下的碰撞事件须在30秒内上报[12]。2025年4月，NHTSA发布自动驾驶车辆框架，提出三项基本原则：保障安全、消除障碍、促进部署[13]。该框架简化了事故报告流程，在维持安全底线的同时为行业发展创造了更灵活的政策空间[14]。

### 2.4 英国自动驾驶法案

英国于2024年5月20日通过《自动驾驶车辆法案》（Automated Vehicles Act 2024），建立了相对完善的责任分配框架[15]。该法案创设了"授权自动驾驶实体"（Authorised Self-Driving Entity, ASDE）角色，明确区分"车内用户"（User-in-Charge, UIC）和"无车内用户"（No-User-in-Charge, NUIC）两种运营模式[16]。安全标准定义为"等于或高于谨慎且有能力的人类驾驶员"（equal to or higher than careful and competent human drivers）[15]。搭载付费乘客的商业试运行预计从2026年春季启动[17]。

英国法案的ASDE模式在当前全球法规中责任界定最为清晰，为远程运营的法律责任归属提供了重要参考。

### 2.5 德国远程驾驶法规

德国于2025年12月1日发布《自动驾驶远程驾驶条例》（Straßenverkehrs-Fernlenkungs-Verordnung, StVFernLV），成为欧洲首个远程驾驶（Teleoperated Driving）法规框架[18]。该条例允许远程控制车辆在批准区域内以不超过80 km/h的速度行驶，设定为期5年的试行阶段[19]。Vay公司计划在该框架下推出商业化无人驾驶共享用车服务[20]。

该法规的独特之处在于它明确覆盖了远程"直接驾驶"（Direct Control）模式，而非仅限于远程协助（Remote Assistance），这与其他国家的监管取向形成差异。

### 2.6 日本SIP-adus

日本的跨部门战略创新促进计划（SIP-adus）自2014年启动，将远程监控与控制纳入自动驾驶巴士的关键能力要求[21]。该计划通过路侧单元（Roadside Unit）与车载摄像头的协同，开展了系统性的现场测试[22]。日本的实践经验对低速自动驾驶场景下的远程运营具有参考价值。

### 2.7 SAE/ISO标准

SAE J3016标准于2024年5月更新（与ISO联合发布），增加了远程支持（Remote Support）相关术语定义[23]。值得注意的是，该标准刻意避免使用"远程操作"（Teleoperation）一词，原因在于该术语在不同语境下的含义存在显著差异[23]。

ISO 22737:2021定义了低速自动驾驶系统在预定路线上的运行要求，最高速度限制为32 km/h，并引入了"无人驾驶运营调度员"（Driverless Operation Dispatcher）角色[24]。该标准为低速封闭/半封闭场景下的远程运营提供了规范基础。

### 2.8 美国国会调查：Markey远程协助操作员报告

2026年3月31日，美国马萨诸塞州民主党参议员Edward J. Markey发布了《远程协助操作员：揭示自动驾驶行业对人类远程协助操作员的依赖》（Remote Back Seat Operators）报告——这是美国国会首次对自动驾驶公司使用远程协助操作员（Remote Assistance Operators, RAOs）进行系统性调查[50]。Markey办公室于2026年2月向七家头部自动驾驶公司（Aurora、May Mobility、Motional、Nuro、特斯拉、Waymo、Zoox）发出质询函，要求披露远程协助运营的详细信息[50]。

调查得出五项关键发现，对ROAM具有直接参考价值：

**第一，七家公司均拒绝披露RAO干预频率。** 所有公司以"商业机密"为由拒绝公开其无人车需要远程协助的频率[50][51]。这一发现构成了迄今为止最有力的证据，表明行业的"自动驾驶"叙事建立在一个未被披露的人工支撑体系之上——这正是ROAM开放事件数据库旨在填补的透明度空白。

**第二，Waymo是唯一使用海外RAO的公司。** 约半数Waymo远程协助人员驻扎在菲律宾，带来了额外的延迟、网络安全和文化语境风险[50]。其他六家受调查公司均未采用离岸RAO。

**第三，Waymo海外RAO不持有美国驾照。** 菲律宾RAO仅持有当地驾照而非美国驾照[50]。鉴于RAO指令直接影响在美国道路上行驶的自动驾驶车辆行为，这引发了关于其对美国交通规则和惯例熟悉程度的安全关切。

**第四，各公司延迟差异显著。** 调查揭示了平均单向延迟的巨大差异：May Mobility 100-140ms（最差500ms）、Waymo本土150ms、Nuro 200ms、Waymo海外250ms、Motional 80-300ms（方向相关）、Zoox最差333ms[50]。Aurora和特斯拉拒绝提供延迟数据。由于缺乏任何联邦层面的RAO允许延迟标准，各公司实际上各自设定安全阈值。

**第五，ADS可能无法可靠拒绝危险的RAO指令。** 尽管所有公司声称其ADS会忽略不安全的RAO建议，但NTSB调查发现，一辆Waymo车辆执行了错误的RAO指令，非法驶过一辆正在展开停车标志的校车[50][51]。

Markey随后致函NHTSA，要求对自动驾驶公司的远程协助实践进行深入调查，并宣布将提出立法为RAO运营建立联邦标准[51]。这一监管态势表明，强制性的RAO透明度要求可能即将到来——进一步验证了ROAM项目建立开放、循证的远程运营基准的时效性和必要性。

## 3 行业实践：远程运营架构对比

### 3.1 Waymo Fleet Response

Waymo的远程运营采用咨询模式（Advisory Model），其核心原则是ADS始终保持完整的车辆控制权，远程人员仅提供上下文信息辅助决策，类似于"打电话问朋友"（phone-a-friend）的模式[25]。

截至2025年底，Waymo运营车辆超过3,000辆，远程值班人员约70名，人车比约为1:41[26]。其远程运营中心分布于亚利桑那州、密歇根州及菲律宾的两个站点[25]。运营规模方面，Waymo每周完成超过40万次付费出行，累计自动驾驶里程超过400万英里[26]。2025年11月，Waymo发布了独立审计报告[27]。

在通信延迟方面，美国本土运营中心的中位延迟约为150ms，菲律宾中心约为250ms[26]。跨国运营中心的延迟差异是否影响决策质量，值得进一步研究。

### 3.2 Tesla Teleops

Tesla于2025年6月在奥斯汀启动远程操作服务，2026年1月起开始无人监管车辆运营[28]。与Waymo的咨询模式不同，Tesla的远程操作员在极端情况下可对车辆实施完全控制（Full Control），限速10 mph以下[29]。Tesla正在开发定制化远程操作系统，并计划2026年上半年扩展至7个城市[30]。

Tesla的技术路线选择反映了"直接控制"与"咨询协助"两种模式的根本分歧。在直接控制模式下，通信延迟和带宽对安全性的影响更为关键。

### 3.3 百度Apollo萝卜快跑

百度Apollo旗下萝卜快跑在2025年第四季度完成超过340万单[31]。然而，2026年3月31日武汉大规模宕机事件暴露了其远程运营的系统性缺陷：缺乏专业道路救援团队，远程干预手段实质无效，最终依赖交通警察进行现场处置[3]。乘客端SOS按钮无法正常工作，客服系统严重过载[4]。

该事件具有典型的系统性故障（Systemic Failure）特征：非单一车辆的孤立故障，而是整个车队同时失效。这类场景在当前任何运营商的应急预案中均未得到充分覆盖，构成了远程运营领域最严峻的研究挑战之一。

### 3.4 远程运营创业公司

远程运营技术正在催生专业化的创业生态。Vay Technology于2025年2月在拉斯维加斯部署30辆租赁车，至2025年7月完成超过17,000次出行[32]。Ottopia开发了基于AI的远程操作平台，支持人机协作式远程干预[33]。GetUgo则聚焦于通信安全，提供端到端加密的远程操作通信方案[33]。据统计，全球自动驾驶远程操作领域约有13家专业企业[34]。

这些创业公司的技术路线差异反映了远程运营尚未形成统一的行业标准和最佳实践。

## 4 学术研究前沿

### 4.1 网络延迟与通信

通信延迟是远程操作的核心技术瓶颈。2024年发表于MDPI Sensors的系统综述对网联自动驾驶车辆远程操作中的网络延迟挑战进行了全面分析，梳理了延迟缓解（Latency Mitigation）与补偿策略（Compensation Strategies）[35]。该研究指出，当端到端延迟超过300ms时，远程操作员的驾驶表现显著下降，而当前蜂窝网络在城市环境中的延迟波动范围较大，这对实时控制模式构成了本质性约束。

### 4.2 间接控制模式

针对直接转向控制在高延迟环境下的局限性，学术界提出了间接控制（Indirect Control）方案。2025年Springer IJAT发表的研究探索了基于路径点设置（Waypoint-Setting）而非直接操舵的远程辅助驾驶模式[36]。该方法将远程操作员从低层级的连续控制任务中解放出来，转为高层级的路径规划决策，有效降低了对通信延迟的敏感度。

### 4.3 控制中心框架

慕尼黑工业大学车辆技术研究所（FTM）在2025年IEEE智能车辆大会（IV）上发表了公共道路自动驾驶车辆远程操作支持的控制中心框架（Control Center Framework）[37]。该框架提出了模块化的控制中心架构设计，涵盖态势感知、通信管理、任务分配等核心功能模块，为远程运营中心的工程化实现提供了参考基线。

### 4.4 综合综述

Lu等人于2022年在IEEE发表的综述系统梳理了提升网联与自动驾驶车辆性能的远程操作技术[38]。该综述覆盖了通信架构、人机交互界面、安全机制等多个维度，是该领域引用率较高的基础性文献。

### 4.5 AI决策信任校准

随着AI辅助和AI自主决策成为远程运营的核心（ROAM第1层和第2层），何时信任AI输出、何时进行人工介入成为关键问题。Cui等人提出了C-TRAIL框架，这是一种基于常识世界模型的轨迹规划方法，引入了双重信任机制：常识信任（Commonsense Trust，评估AI输出是否符合交通常识）和运动学信任（Kinematic Trust，验证物理可行性）[43]。该框架采用自适应信任校准（Adaptive Trust Calibration）机制，基于指数移动平均（EMA）更新和奖励自适应衰减：当AI决策产生高奖励（正确结果）时，信任水平保持；当决策产生低奖励（错误或近似未遂事件）时，信任以加速速率衰减。这一信任衰减机制对远程运营具有直接启示：在ROAM的第1层（AI自主响应）中，类似方法可动态调整自主行动的置信度阈值——当对AI决策质量的累积信任降至安全阈值以下时，自动升级至第2层（人工确认）。

### 4.6 人类角色分类框架

Koopman于2026年4月提出了自动驾驶及具身AI系统中人类角色的系统性分类框架，对当前行业"assistant vs driver"的二分法提出了根本性质疑[44]。该框架识别出六类人类角色，每类又分为"现场"（On-Site）和"远程"（Remote）两种形式，共构成12种角色组合：

| 角色 | 职责 | 对应ROAM层级 |
|------|------|------------|
| **Operator（操作员）** | 执行至少一个持续控制回路（如方向盘、制动） | Layer 3 远程遥控 |
| **Supervisor（监督员）** | 主动监控自动化运行，必要时介入 | （未覆盖，增强方向） |
| **Decider（决策者）** | 响应AI请求，提供情景判断或方案批准 | Layer 2 AI辅助+人工确认 |
| **Responder（响应者）** | 处理异常事件（脱困、事故、乘客问题） | Layer 3 线下派人 |
| **Standby（待命者）** | 按需切换至其他角色 | 运营中心调度 |
| **Maintainer（维护者）** | 诊断、维修、运营就绪管理 | （未覆盖，车队管理域） |

该框架有三个对ROAM具有直接价值的洞察：

**第一，澄清"远程协助"的安全责任边界。** Koopman批判了Automated Vehicle Safety Consortium（AVSC-I-04-2023）的立场——该标准声称远程协助（Remote Assistance）不承担DDT安全责任，因此可由海外人员承担、无需像驾驶员那样接受监管[44]。Koopman反驳：远程决策者对"交通信号灯颜色识别"或"道路障碍物性质判断"等任务的回应直接影响ADS行为，这些任务本就是DDT的组成部分，否认其安全责任等同于"责任洗白"（accountability laundering）。

**第二，与SAE自动化等级正交。** Koopman明确指出，这12种人类角色与SAE J3016的L0-L5等级划分是两个独立维度：SAE等级描述的是DDT在人-机之间的分配，而角色框架描述的是为使自动化系统在真实世界可运行所需的人类工作类型[44]。一个标称L4的系统仍可能同时需要Operator（测试阶段）、Remote Decider（日常运营）、Remote/On-Scene Responder（事故响应）等多类人员。

**第三，问责制原则。** 该框架主张：无论人员处于哪个角色，其决策若影响系统行为，就应当承担与其职责范围相称的安全责任；受害者不应被迫在复杂的人-机责任界定中承担举证负担。

**ROAM参考架构的扩展方向：** 当前ROAM三层架构主要围绕"AI自主/人工确认/人工接管"的决策升级逻辑展开，而Koopman框架补充了人员组织层面的视角。未来可在ROAM参考架构中增加"Roles & Responsibilities"模块，将Koopman的12角色体系与ROAM三层决策模型进行正式对齐，明确每层决策所涉及的人员角色、所需资质、响应时间要求及法律责任分配。

### 4.7 无人机远程运营的跨域经验

Cummings于2026年发表研究，系统性地将美军35年无人机（UAV）远程运营经验迁移至自动驾驶出租车领域[45]。该研究识别出五项可直接应用于Robotaxi远程运营的关键教训：延迟约束、人因工作站设计、操作员工作负荷管理、系统化操作员训练、以及健壮的应急预案。

延迟约束的物理边界。Cummings明确指出人类神经肌肉反应延迟为200-500ms[45]。早期美军在拉斯维加斯远程起降中东战区无人机，2秒延迟导致事故率极高，最终被本地视距操作取代，进而演进至全自动起降。这一教训对Robotaxi远程遥控的意义在于：任何要求远程操作员在200ms内响应的场景在物理上不可行，必须通过AI预处理、操作员辅助决策等方式重构任务分配。Waymo在旧金山2025年断电事件中，由于将远程运营中心迁至菲律宾导致端到端延迟显著增加，成为事件恶化的关键因素之一。

工作站设计决定成败。Cummings的数据揭示：美军Shadow无人机80%事故归因于界面设计缺陷，而自动化程度高、界面设计优良的Global Hawk仅因人因问题损失1架[45]。自动驾驶行业大量使用Xbox/PS5游戏手柄作为低速接驳车的远程控制设备存在严重隐患：无力反馈导致误触、游戏习惯到严肃运营的负迁移、控制位姿不稳定等。军方早在40年前就在数字控制中引入力反馈以防止误操作。

操作员工作负荷的数量级差距。美军经过数亿美元研发投入、历经20多年，仍无法实现1名操作员监管多架中大型无人机的目标。Waymo当前1:29的人车比在Cummings分析的2024-2025数据中表现出显著的性能瓶颈——阻塞与冻结事件的平均响应时间分别为21.5分钟和20.3分钟，统计上无显著改善（t=-0.217, p=0.82）[45]，表明该配比已达能力天花板。

DJI的产品化方案提供了平行参考系。与军方经验互补的是，DJI在消费级与工业级无人机远程运营上积累了30年产品化经验，将Cummings所列的五项教训工程化为可规模化部署的方案[46-49]：

- OcuSync/O4图传系统：通过物理层直连消除TCP/IP握手延迟，端到端延迟低至15ms，FCC标准下传输距离达15km，自适应跳频覆盖5.170-5.250 GHz与5.725-5.850 GHz双频段[46]。这一工程成就证明延迟问题在专用链路设计下可被大幅压缩。
- FlightHub 2 Virtual Cockpit：模块化的远程操作员工作站，三段式界面布局（地图/设备信息/操控），鼠标键盘为主要输入（替代游戏手柄），配备音频提示与FPV窗口[47]。
- Dock 2自动化基座：IP55防护等级、双RTK天线、独立电池、通信失联自动返航等工程特性[48]，代表了"本地自主+远程监督"混合架构的成熟形态。
- UTC训练认证体系：全球200+ DJI无人机培训中心，超过40,000名认证飞手，12小时在线+2天实训+飞行考核的标准化认证流程[49]。

这一对比揭示了Robotaxi远程运营的一个独特机会：中国部分具备无人机技术传承的Robotaxi运营主体（如承袭DJI技术栈的卓驭科技）在低延迟专用传输链路、操作员工作站设计、飞手级认证体系等维度具备其他纯自动驾驶背景公司难以复制的原生优势。这一优势的系统性挖掘与对外分享，构成ROAM项目的一项重要差异化贡献方向。相关技术细节与映射分析见 [uav-lessons-learned.md](./uav-lessons-learned.md)。

当前学术研究仍存在明显的领域空白：系统性故障场景下的远程运营策略缺乏研究，人车比优化的理论模型尚未建立，跨国运营中心的延迟对决策质量的量化影响尚待验证。

## 5 事故数据分析

事故数据是评估远程运营有效性的关键依据。根据NHTSA数据，2021年7月至2025年11月期间，Waymo共报告1,429起事故，涉及117人受伤和2人死亡[39]。考虑到其超过400万英里的自动驾驶里程，这一数据需要与人类驾驶员在相同运行环境下的事故率进行对比分析。

Cruise在2023年10月行人拖拽事故后实施车队召回，被NHTSA处以150万美元罚款[1]。该事件中远程操作员的响应延迟和干预决策过程暴露了人机交互层面的关键缺陷。

在中国，小马智行（Pony.ai）在北京发生过车辆起火事件，导致服务临时暂停[40]。百度Apollo在武汉的大规模宕机事件以及行人碰撞事故，进一步凸显了远程运营在高密度部署场景下的脆弱性[3]。

这些事故数据揭示了一个共同模式：远程运营系统在常态运行中表现尚可，但在异常场景叠加（网络故障、极端天气、系统软件缺陷等）时，其应急能力不足。这恰恰是安全论证中最需关注的残余风险区间。

## 6 关键挑战与研究空白

基于上述法规、实践和学术研究的梳理，本文识别出以下六项关键挑战和研究空白：

**第一，系统性故障应急能力缺失。** 2026年3月萝卜快跑武汉宕机事件表明，当前无任何运营商具备应对批量车辆同时故障的有效方案。现有应急预案主要面向单车故障设计，对于软件缺陷、网络中断等可能导致整个车队同时失效的场景，缺乏系统性的应急架构。

**第二，远程协助与远程驾驶的概念分歧。** SAE J3016刻意回避"Teleoperation"一词，ISO 22737定义了"Driverless Operation Dispatcher"角色，中国GB标准使用"远程协助"表述。在实践中，Waymo采用咨询模式（Advisory），Tesla允许直接控制（Direct Control）。术语和实践的不统一增加了跨国法规协调和安全评估的复杂度。

**第三，人车比经济性的巨大差距。** Waymo的人车比约为1:41，而中国法规要求最高为1:3，两者之间存在一个数量级以上的差距[9][26]。如何通过AI辅助决策、自动化事件分流等技术手段降低人工干预比例，同时维持安全水平，是实现商业可持续的关键课题。

**第四，通信安全与延迟约束。** Waymo菲律宾运营中心的中位延迟约为250ms，远高于本土的150ms[26]。5G和V2X技术在中国城市的部署仍不均匀。通信安全（防劫持、防篡改）和端到端延迟的确定性保障是远程运营大规模部署的基础前提。

**第五，法律责任界定不清晰。** 英国ASDE模式在全球法规中责任界定最为明确，但中国目前仍处于地方立法探索阶段，国家层面的责任分配框架尚未成型。当远程操作员的指令导致事故时，责任归属于操作员个人、运营企业还是ADS开发商，在大多数法域中仍无定论。

**第六，自然驾驶行为基准缺失。** 中国GB标准中的残余风险准则（碰撞率低于10^-4/h等）需要人类驾驶员的行为基线数据作为参照。然而，在具体的中国城市交通场景中，可信的大规模自然驾驶行为数据集仍然稀缺，这制约了残余风险评估的科学性。

## 7 未来展望：从远程运维到"无人驾驶出租车救援保险"

### 7.1 与传统汽车保险救援的结构性类比

当前汽车保险行业的道路救援服务已形成成熟的运营模式：事故发生后，驾驶员拨打保险公司电话，保险公司调度查勘员到场评估、安排拖车、协调维修、完成理赔。这一链条的本质是**风险分摊与规模化应急响应**——单个车主无力维持专属救援团队，保险公司通过汇聚大量投保人的保费来支撑24小时救援网络的运营成本。

L4级Robotaxi的远程运营面临着高度类似的经济学问题。当前各运营商（Waymo、百度Apollo、小马智行等）均在各自的运营城市建设独立的远程运维中心。然而，随着Robotaxi从少数城市试点扩展至全国乃至全球范围的规模化运营，每家运营商在每个城市独立建设和维护远程运维团队的模式将面临越来越大的经济压力。

这一矛盾与汽车保险行业的演化路径高度一致：正如车主不会自己养修车队一样，Robotaxi运营商在每个城市建独立的远程运维团队，在规模化阶段同样不经济。

### 7.2 三层服务架构展望

基于上述分析，未来Robotaxi远程运营有可能分化出三个层次的服务形态：

**第一层：远程运维即服务（Remote Operations as a Service, ROaaS）**。这是ROAM参考架构所描述的核心业务形态。第三方服务平台为多家运营商和OEM提供7×24小时的远程监控、AI辅助决策和异常处置服务，按车·月或按次收费。其商业逻辑类似于当前的AAA道路救援或中国的12122交通救援服务——多品牌车辆共享同一套救援基础设施。

**第二层：事故响应保险服务**。当远程处置无法解决问题时（如车辆硬件故障、交通事故、乘客受伤），需要线下团队到场处理。这一环节与传统汽车保险的查勘定损、拖车救援高度重合。保险公司可作为承保方，远程运维平台作为执行方，形成"保险+运维"的协同模式。对于乘客安置、替代交通安排、医疗转运等增值服务，保险产品可提供标准化的保障方案。

**第三层：数据驱动的风险定价**。这是真正体现保险本质的层面。当ROAM的事件数据库和场景分类体系积累到足够规模后，可以为不同运营商、不同ADS系统、不同城市环境计算差异化的事故率和风险概率。这些数据即为保险精算的核心输入。具体而言：

- **暴露率计算**：自然驾驶行为数据提供"分母"（正常行驶里程/时间），事故数据提供"分子"（事故频次），由此计算特定场景下的事故暴露率；
- **可预防性判断**：区分"人类驾驶员也无法避免"的事故（不可抗力，保费较低）和"ADS应当避免但未能避免"的事故（系统缺陷，保费较高），对不同类型事故进行差异化定价；
- **运营商评级**：基于历史事件数据对不同运营商的远程运维能力进行评级，评级结果直接影响保费水平。

### 7.3 行业先行实践

全球范围内，Robotaxi保险的探索已经开始。Waymo与瑞士再保险（Swiss Re）合作，利用自动驾驶运营数据优化保险定价模型[41]。英国《自动驾驶车辆法案2024》明确规定了ASDE（授权自动驾驶实体）的保险责任，要求ADS运营方必须持有责任保险[15]。中国平安、人保等保险公司也在积极探索智能网联汽车保险产品的设计[42]。

然而，当前的尝试普遍面临一个共性挑战：**缺乏标准化的事件数据和风险评估框架**。各运营商的事故报告格式不统一，严重度和可预防性的判断标准缺失，导致保险公司无法建立可比较的精算模型。

### 7.4 ROAM在保险生态中的定位

ROAM项目的四个模块恰好对应了Robotaxi保险生态中的关键基础设施需求：

| ROAM模块 | 保险生态中的角色 |
|----------|----------------|
| 事件数据库 | 保险理赔的案例库和精算数据源 |
| 场景分类体系 | 风险分类和保费定价的分类框架 |
| 参考架构 | 远程运维服务商（保险执行方）的技术标准 |
| 评价基准 | 运营商能力评级和保费差异化的指标体系 |

驭研科技的航测自然驾驶数据（750h+飞行时数、10.5M+轨迹）在此生态中承担着"正常人群健康基线"的角色——正如健康保险需要知道正常人群的体检指标才能判断异常，Robotaxi保险需要自然驾驶行为基线来区分"合理的残余风险"与"不合理的系统缺陷"。

### 7.5 展望时间线

这一生态的成熟需要多个前置条件的逐步到位：

- **近期（2026-2028）**：各运营商的远程运维体系逐步标准化，GB标准的安全档案和残余风险准则落地实施，ROAM等开源项目积累结构化事件数据；
- **中期（2028-2030）**：第三方远程运维服务商出现，保险公司推出Robotaxi专项保险产品，基于运营数据的差异化定价成为可能；
- **远期（2030+）**：形成"运营商+远程运维服务商+保险公司"的三方协同生态，远程运维平台成为保险理赔链条的关键节点，数据驱动的风险管理成为行业常态。

## 8 ROAM项目定位

基于上述分析，ROAM（RoboTaxi Operations Anomaly Management）项目旨在填补该领域的关键空白。ROAM定位为开源的参考架构与分析工具集，核心贡献包括三个层面：

**事件追踪基线。** 建立L4级Robotaxi远程运营事件的结构化记录与分类体系，覆盖通信故障、系统宕机、人机交互失效等典型事件类型，为行业提供可比较的事件分析框架。

**场景分类法。** 参照ISO 34502的场景描述方法论，构建远程运营相关的场景分类体系（Scenario Taxonomy），将法规要求、行业实践和事故数据映射为可检索的场景库。

**参考架构。** 基于行业最佳实践和学术前沿，提出远程运营中心的模块化参考架构，支持咨询模式和直接控制模式的灵活配置。

**保险生态基础设施。** 通过标准化的事件记录、场景分类和评价基准，为未来Robotaxi保险产品的精算定价和理赔执行提供数据基础和方法论支撑。

驭研科技（DRIVEResearch）积累的航测自然驾驶数据（750h+飞行时数、10.5M+轨迹）为上述研究提供了行为基线数据支撑。该数据集可用于建立中国城市交通场景下的人类驾驶员行为基准，与GB标准的残余风险准则形成对接，并支撑SOTIF（ISO 21448）方法论中的场景分析与已知不安全场景识别。

ROAM项目将秉持开源协作的理念，通过标准化数据格式、模块化架构设计和社区驱动的迭代模式，为L4级Robotaxi远程运营的安全管理提供公共知识基础设施。

---

## 参考文献

[1] NHTSA, "Cruise LLC Consent Order and Civil Penalty," National Highway Traffic Safety Administration, 2024. [Link](https://www.nhtsa.gov/press-releases/consent-order-cruise-crash-reporting)

[2] TechCrunch, "Waymo explains why its robotaxis got stuck during the SF blackout," 2025年12月. [Link](https://techcrunch.com/2025/12/24/waymo-explains-why-its-robotaxis-got-stuck-during-the-sf-blackout/)

[3] 虎嗅网, "萝卜快跑瘫痪事故暴露的'阿喀琉斯之踵'," 2026年4月. [Link](https://www.huxiu.com/article/4847431.html)

[4] 新浪汽车, "武汉'萝卜快跑'车辆停滞已恢复，业内人士分析," 2026年4月. [Link](https://auto.sina.cn/news/2026-04-01/detail-inhsyfuw2691947.d.html)

[5] UNECE, "ECE-TRANS-WP.29-GRVA-2026-02e: Draft Global Technical Regulation on Automated Driving Systems," United Nations Economic Commission for Europe, 2026年1月. [Link](https://unece.org/sites/default/files/2026-01/ECE-TRANS-WP.29-GRVA-2026-02e.pdf)

[6] Connected Automated Driving, "UNECE GRVA Adopts Draft Global Regulation on Automated Driving Systems," 2026年1月. [Link](https://www.connectedautomateddriving.eu/blog/unece-grva-adopts-draft-global-regulation-on-automated-driving-systems/)

[7] U.S. Federal Register, "Notice and Request for Comment; Proposal for a New United Nations Global Technical Regulation on Automated Driving Systems (ADS)," 2026年1月. [Link](https://www.federalregister.gov/documents/2026/01/23/2026-01274/notice-and-request-for-comment-proposal-for-a-new-united-nations-global-technical-regulation-on)

[8] 中华人民共和国工业和信息化部, "GB XXXXX--XXXX《智能网联汽车 自动驾驶系统安全要求》征求意见稿," 2026年2月. 含附录C.2远程协助要求、附录D安全档案要求. [Link](https://carnewschina.com/2026/02/26/new-chinese-regulations-push-l3-autonomous-vehicles-closer-to-l4-capabilities-with-enhanced-safety-protocols/)

[9] 交通运输部, "自动驾驶汽车运输安全服务指南（试行）," 2023年12月. 远程安全员人车比要求最高1:3. [Link](https://xxgk.mot.gov.cn/2020/jigou/ysfws/202312/t20231205_3962490.html)

[10] 深圳市人民代表大会常务委员会, "深圳经济特区智能网联汽车管理条例," 2022年8月. [Link](https://www.gd.gov.cn/gdywdt/dsdt/content/post_3986167.html)

[11] 北京市人民代表大会常务委员会, "北京市自动驾驶汽车条例," 2025年4月生效. [Link](https://www.beijing.gov.cn/zhengce/dfxfg/202501/t20250103_3980149.html)

[12] NHTSA, "Standing General Order 2021-01: Incident Reporting for Automated Driving Systems," National Highway Traffic Safety Administration. [Link](https://www.nhtsa.gov/laws-regulations/standing-general-order-crash-reporting)

[13] Mayer Brown, "DOT and NHTSA Announce Autonomous Vehicle Framework," 2025年4月. [Link](https://www.mayerbrown.com/en/insights/publications/2025/04/dot-and-nhtsa-announce-autonomous-vehicle-framework)

[14] Foley & Lardner LLP, "Driving Into 2026: The State of NHTSA and the Future of Vehicle Safety Regulation," 2025年11月. [Link](https://www.foley.com/insights/publications/2025/11/driving-into-2026-the-state-of-nhtsa-and-the-future-of-vehicle-safety-regulation/)

[15] UK Parliament, "Automated Vehicles Act 2024," Royal Assent 2024年5月20日. [Link](https://www.legislation.gov.uk/ukpga/2024/10)

[16] Hogan Lovells, "UK passes Automated Vehicles Act 2024," 2024. [Link](https://www.hoganlovells.com/en/publications/uk-passes-automated-vehicles-act-2024)

[17] Addleshaw Goddard, "The UK's Automated Vehicles Act 2024," 2024. [Link](https://www.addleshawgoddard.com/en/insights/insights-briefings/2024/transport/passing-self-driving-test-uks-automated-vehicles-act-2024/)

[18] Taylor Wessing, "Legal framework for automated and autonomous driving and teledriving in the EU and Germany," 2026年2月. [Link](https://www.taylorwessing.com/en/insights-and-events/insights/2026/02/legal-frameworks-for-autonomous-driving-and-teledriving)

[19] Bird & Bird, "Teleoperiertes Fahren -- StVFernLV seit Dezember 2025 in Kraft," 2026. [Link](https://www.twobirds.com/en/insights/2026/germany/teleoperiertes-fahren-straenverkehr-fernlenk-verordnung-(stvfernlv)-seit-dezember-2025-in-kraft)

[20] Vay Technology, "Vay Welcomes Germany's Remote Driving Regulation," Press Release, 2025. [Link](https://vay.io/press-release/vay-welcomes-germanys-remote-driving-regulation-a-breakthrough-in-remote-driving-commercialization-at-scale/)

[21] SIP-adus (Cross-ministerial Strategic Innovation Promotion Program -- Automated Driving for Universal Services), 日本内阁府, 2014年启动. [Link](https://en.sip-adus.go.jp/)

[22] SIP-adus, "An Update on Japanese Initiatives for Automated Driving," in *Automated Driving*, Springer, 2018. [Link](https://link.springer.com/chapter/10.1007/978-3-319-94896-6_2)

[23] SAE International, "J3016: Taxonomy and Definitions for Terms Related to Driving Automation Systems for On-Road Motor Vehicles," 2024年5月更新 (Joint with ISO). 另见：MobilityEngTech分析. [Link](https://www.mobilityengineeringtech.com/component/content/article/44792-sae-ma-06724)

[24] ISO, "ISO 22737:2021 -- Intelligent transport systems -- Low-speed automated driving (LSAD) systems for predefined routes," International Organization for Standardization, 2021. [Link](https://www.iso.org/standard/73767.html)

[25] Waymo Blog, "Fleet response: Lending a helpful hand to Waymo's autonomously driven vehicles," 2024年5月. [Link](https://waymo.com/blog/2024/05/fleet-response/)

[26] Remio AI, "Waymo Remote Assistance: The Reality of Autonomous Driving," 2025. 另见：Futurism相关分析报道. [Link](https://www.remio.ai/post/waymo-remote-assistance-the-reality-of-autonomous-driving)

[27] Waymo Blog, "Independent Audits of Waymo's Safety Case and Remote Assistance Programs," 2025年11月. [Link](https://waymo.com/blog/2025/11/independent-audits/)

[28] TechCrunch, "Tesla appears to be building a teleoperations team for its robotaxi service," 2024年11月. 另见：TechCrunch, "Tesla launches robotaxi rides in Austin," 2025年6月. [Link](https://techcrunch.com/2024/11/26/tesla-appears-to-be-building-a-teleoperations-team-for-its-robotaxi-service/)

[29] Futurism, "Tesla Workers Are Seizing Control of Robotaxis When They Get Stuck," 2025. [Link](https://futurism.com/advanced-transport/tesla-robotaxis-driven-remotely)

[30] Planetizen, "Tesla Reveals Remote Drivers Temporarily Control its Robotaxis," 2026. [Link](https://www.planetizen.com/news/2026/04/137261-tesla-reveals-remote-drivers-temporarily-control-its-robotaxis)

[31] 百度投资者关系, "Baidu Announces Fourth Quarter and Fiscal Year 2025 Results," 2026年2月. [Link](https://ir.baidu.com/news-releases/news-release-details/baidu-announces-fourth-quarter-and-fiscal-year-2025-results)

[32] Vay Technology, "Vay expands service area in Las Vegas," Press Release, 2025. 另见：TechCrunch, "Vay expands driverless car-sharing fleet in Las Vegas," 2025年1月. [Link](https://vay.io/vay-expands-service-area-in-las-vegas/)

[33] StartUs Insights, "5 Top Emerging Teleoperation Startups," 2025. 涵盖Ottopia (AI辅助远程操作平台) 和 GetUgo (端到端加密通信方案). [Link](https://www.startus-insights.com/innovators-guide/5-top-emerging-teleoperation-startups/)

[34] Tracxn, "Top Companies in Autonomous Vehicles Teleoperation," 2025. [Link](https://tracxn.com/d/trending-business-models/startups-in-autonomous-vehicles-teleoperation/__GS_MwTPd-ARbXrP9dRsdYOTXDe2wOGOsT2hPv2G8ty8/companies)

[35] Hofbauer, M. et al., "Network latency challenges in teleoperation of connected and automated vehicles: A systematic review," *Sensors*, vol. 24, no. 12, p. 3957, 2024. [Link](https://www.mdpi.com/1424-8220/24/12/3957)

[36] Kim, K. et al., "Development of Tele-operated Driving Assistance System for Autonomous Vehicles with an Open-Source Platform," *International Journal of Automotive Technology*, vol. 26, pp. 1379-1390, 2025. [Link](https://link.springer.com/article/10.1007/s12239-025-00218-8)

[37] Wolf, M.-M. et al., "Control center framework for teleoperation support of automated vehicles on public roads," in *Proc. IEEE Intelligent Vehicles Symposium (IV)*, 2025. [Link](https://ieeexplore.ieee.org/document/11097634/)

[38] Lu, S. et al., "Teleoperation technologies for enhancing connected and autonomous vehicles," in *Proc. IEEE 19th International Conference on Mobile Ad Hoc and Smart Systems (MASS)*, 2022. [Link](https://ieeexplore.ieee.org/document/9973618/)

[39] DAM Firm, "Waymo Accidents | NHTSA Crash Data," damfirm.com, 2025. [Link](https://www.damfirm.com/waymo-accident-statistics.html)

[40] EVreporter, "Pony.ai Beijing operations suspended after Robotaxi fire," 2025. [Link](https://evreporter.com/autonomous-driving-startup-pony-ai-beijing-operations-suspended-after-robotaxi-fire/)

[41] Swiss Re, "Waymo and Swiss Re partner on autonomous vehicle insurance," 2024. [Link](https://www.swissre.com/reinsurance/property-and-casualty/solutions/automotive-solutions.html)

[42] 中国银行保险报, "智能网联汽车保险：从传统车险到数据驱动的风险管理," 2025. [Link](https://www.cbimc.cn/)

[43] Cui, Z. et al., "C-TRAIL: A Commonsense World Framework for Trajectory Planning in Autonomous Driving," *IEEE Transactions on Vehicular Technology*, 2026. GitHub: [https://github.com/ZhihongCui/CTRAIL](https://github.com/ZhihongCui/CTRAIL)

[44] Koopman, P., "Human Roles in AVs and Embodied AI Systems," *Phil & Junko on AV Safety*, Substack, April 4, 2026. 提出6角色×2位置=12种角色组合的框架，挑战"assistant vs driver"二分法，论证远程决策者对系统安全承担实质责任。[Link](https://philkoopman.substack.com/p/embodied-ai-accountability-for-remote)

[45] Cummings, M., "What self-driving companies should learn from drone remote operations," College of Engineering & Computing, George Mason University, 2026. 基于美军35年UAV远程运营经验，提炼延迟、工作站设计、操作员负荷、训练、应急预案五项教训，指出Waymo当前1:29人车比已达能力天花板。

[46] DJI Enterprise, "OcuSync/O4 Video Transmission Technology: 15ms latency, 15km range with adaptive frequency hopping," 2024. [Link](https://enterprise.dji.com/)

[47] DJI Enterprise Insights, "DJI FlightHub 2: Virtual Cockpit Now Available," 2024. 三段式远程操作员工作站界面：地图+设备信息+操控面板，鼠标键盘输入。[Link](https://enterprise-insights.dji.com/blog/dji-flighthub-2-virtual-cockpit-now-available)

[48] DJI Enterprise, "DJI Dock 2 Elevates Automated Drone Operations," 2024. IP55防护、双RTK天线、独立电池、通信失联自动返航。[Link](https://enterprise.dji.com/news/detail/dji-dock-2-release)

[49] DJI Enterprise, "DJI UTC (Unmanned Aerial System Training Centers) Program," 200+全球培训中心，40,000+认证飞手。[Link](https://enterprise-insights.dji.com/learning-center)

[50] Office of Senator Edward J. Markey, "Remote Back Seat Operators: Revealing the Autonomous Vehicle Industry's Reliance on Human Remote Assistance Operators," 2026年3月31日. 美国国会首次对自动驾驶远程协助操作的系统性调查，覆盖七家公司（Aurora、May Mobility、Motional、Nuro、Tesla、Waymo、Zoox）。[Link](https://www.markey.senate.gov/news/press-releases/senator-markey-releases-groundbreaking-report-on-autonomous-vehicle-industrys-use-of-remote-human-operators) [PDF](docs/Markey-Remote-Back-Seat-Operators-Report-2026.pdf)

[51] 智车科技, "Waymo拒交安全数据：七家自动驾驶巨头集体沉默," 2026年4月9日. 对Markey RAOS报告的中文深度分析，提供了行业透明度挑战的额外背景。

---

*本文献综述为ROAM项目研究基础文档，将随着法规更新、行业实践演进和新研究成果的发表持续修订。*
