# 六大技术支柱：L4 远程运营异常管理的技术体系

**Six Technology Pillars for L4 Remote Operations and Anomaly Management**

---

> 作者：Yuxin Zhang
> 日期：2026 年 4 月
> 版本：v1.0

---

## 引言

L4 自动驾驶远程运营与异常管理不是单一技术能够解决的问题，而是需要多个技术领域深度融合的系统工程。本文档将 L4 远程运营所依赖的技术体系归纳为 **六大支柱**，每个支柱包含核心能力、关键指标、代表性学术文献、国际/国内标准和行业最佳实践。

### 六大支柱的相互关系

```
     ┌──────────────────────────────────────────────────┐
     │              L4 远程运营异常管理系统               │
     └──────────────────────────────────────────────────┘
                           ▲
       ┌──────────┬────────┼────────┬──────────┐
       │          │        │        │          │
   ┌───┴───┐  ┌───┴───┐┌───┴───┐┌───┴───┐  ┌───┴───┐
   │支柱1  │  │支柱2  ││支柱3  ││支柱4  │  │支柱5  │
   │感知决策│  │远程遥控││无线通信││AI信任  │  │网安数据│
   └───────┘  └───────┘└───────┘└───────┘  └───────┘
                           ▲
                        ┌──┴──┐
                        │支柱6│
                        │人员运营│
                        └─────┘
```

**依赖关系**：**支柱 3（通信）** 是基础设施；**支柱 1（感知决策）** 决定异常被识别的能力；**支柱 2（远程遥控）+ 支柱 4（AI 信任）** 决定异常如何被处置；**支柱 5（网安数据）** 贯穿始终；**支柱 6（人员）** 是最终保障。

---

## 支柱一：自动驾驶感知与决策（Perception & Decision）

### 核心能力
- **异常自识别**：ADS 主动识别自身无法处置的场景
- **不确定性量化**：对感知和决策置信度的实时评估
- **边缘场景检测**：识别超出 ODD 边界的情况
- **SOTIF 触发条件监控**：在线监测已知和未知的触发条件

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| ODD 场景族覆盖率 | ≥ 95% | ISO 34502 |
| OOD 检测 AUROC | ≥ 0.95 | Waymo/Mobileye 公开披露 |
| 残余 SOTIF 风险 | ≤ 10⁻⁸/hour | Koopman L4 基准 |
| 异常检出率 | > 95% | 行业目标 |
| ODD 退出判断延迟 | < 200 ms | 行业目标 |

### 学术文献

1. **Peng, L., Li, B., Yu, W., Yang, K., Shao, W., & Wang, H. (2024).** "SOTIF Entropy: Online SOTIF Risk Quantification and Mitigation for Autonomous Driving." *IEEE Transactions on Intelligent Transportation Systems*, 25(2). — 基于熵的运行时 SOTIF 风险指标，桥接 ODD 监控与 MRC/远程接管触发。

2. **Shao, Y., Mohd Zulkefli, M. A., Sun, Z., & Huang, P. (2023).** "Evaluating connected and autonomous vehicles using a hardware-in-the-loop testbed and a living lab." *Transportation Research Part C*, 150. — HIL + living-lab SOTIF 验证方法学。

3. **Zhou, J., del Re, L., & Kiencke, U. (2023).** "Decomposition and Quantification of SOTIF Requirements for Perception Systems of Autonomous Vehicles." *arXiv:2501.10097*. — ODD 到需求的定量分解，对异常阈值设定至关重要。

4. **Hendrycks, D., Basart, S., Mazeika, M., et al. (2022).** "Scaling Out-of-Distribution Detection for Real-World Settings." *ICML 2022*. — AV 感知安全文献广泛引用的 OOD 基准。

5. **Feng, D., Harakeh, A., Waslander, S. L., & Dietmayer, K. (2022).** "A Review and Comparative Study on Probabilistic Object Detection in Autonomous Driving." *IEEE Transactions on Intelligent Transportation Systems*, 23(8), 9961-9980. DOI:10.1109/TITS.2021.3096854 — 感知不确定性量化的权威综述。

6. **Koopman, P., & Wagner, M. (2023).** "Positive Trust Balance for Self-Driving Car Deployment." *SAFECOMP 2023 Workshops, LNCS 14182*. — 论证运行时异常升级至人工的必要性。

### 标准

- **ISO 21448:2022** *Road vehicles — Safety of the Intended Functionality (SOTIF)*
- **ISO 34502:2022** *Road vehicles — Test scenarios for automated driving systems*
- **ISO/PAS 8800:2024** *Road vehicles — Safety and artificial intelligence*
- **ISO 26262:2018** *Road vehicles — Functional safety*
- **GB/T 41798-2022** 《智能网联汽车 自动驾驶功能场地试验方法及要求》
- **GB/T 44721-2024** 《智能网联汽车 预期功能安全 场景要素》（中国 SOTIF 场景标准）

### 行业最佳实践

- **Waymo Safety Framework v2 (2023)** — 公开的"残余风险接受准则"与 readiness determination，定义异常触发的远程支持升级流程
- **Mobileye RSS + True-Redundancy** — 形式化验证边缘场景响应（Shalev-Shwartz et al. 的 IEEE 系列论文）
- **Baidu Apollo Scenario Engine** — 大规模场景挖掘与 SOTIF 触发条件管理

### ROAM 层级映射
- **L1 AI 自主响应**：依赖强异常自识别能力
- **L2 AI 辅助人工确认**：不确定性量化是升级判断的依据
- **L3 远程驾驶**：ODD 退出是触发 L3 的前提

---

## 支柱二：远程遥控与人机交互（Teleoperation & HMI）

### 核心能力
- **低延迟远程驾驶**：直接控制模式下的实时操纵
- **间接路径规划**：Waypoint/轨迹/交互式规划模式
- **操作员情境感知**：多路视频、地图、车辆状态综合展示
- **HMI 优化**：降低操作员认知负荷

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| 玻璃到玻璃延迟（摄像头→显示） | < 200 ms（商用目标）/ < 150 ms（研究目标） | Ottopia / 学术研究 |
| 指令到动作延迟 | < 300 ms（直接驾驶） | 5GAA 要求 |
| 操作员监管车辆数（间接模式） | 1:3 ~ 1:10 | Motional/Waymo 披露 |
| 情境感知恢复时间 | < 10 s | Mutzenich 2021 基准 |
| NASA-TLX 工作负荷 | < 60/100 | 行业目标 |

### 学术文献

1. **Majstorović, D., Hoffmann, S., Pfab, F., et al. (2022).** "Survey on Teleoperation Concepts for Automated Vehicles." *IEEE SMC 2022*. arXiv:2206.04239 — 被引用最多的直接/间接（waypoint/轨迹/交互式规划）远程操作分类。

2. **Zhang, T. (2024).** "Network Latency in Teleoperation of Connected and Autonomous Vehicles: A Review of Trends, Challenges, and Mitigation Strategies." *Sensors*, 24(12), 3957. DOI:10.3390/s24123957 — 最新综合综述。

3. **Graf, G., & Hussmann, H. (2020, 2023 更新).** "User Requirements for Remote Teleoperation-Based Interfaces." *AutomotiveUI Adjunct Proceedings*. — 远程操作员工作站的实证 HMI 需求研究。

4. **Schimpe, A., Feiler, J., Hoffmann, S., Majstorović, D., & Diermeyer, F. (2022).** "Open Source Software for Teleoperated Driving." *IEEE ICCVE 2022*. — TUM 的开源远程操作栈，基准参考。

5. **Kang, L., Zhao, W., Qi, B., & Banerjee, S. (2018).** "Augmenting Self-Driving with Remote Control: Challenges and Directions." *HotMobile 2018*. — 被引用最多的基础论文，论证间接控制对 L4 的必要性。

6. **Neumeier, S., Wintersberger, P., Frison, A.-K., Becher, A., Facchi, C., & Riener, A. (2019).** "Teleoperation: The Holy Grail to Solve Problems of Automated Driving? Sure, but Latency Matters." *AutomotiveUI 2019*. — AV 远程操作最被引用的实证工作负荷研究。

7. **Tener, F., & Lanir, J. (2022).** "Driving from a Distance: Challenges and Guidelines for Autonomous Vehicle Teleoperation Interfaces." *CHI 2022*. DOI:10.1145/3491102.3501827 — ACM CHI 的人因设计指南。

### 标准

- **SAE J3016_202104** — 定义远程驾驶员、远程协助、远程应急角色
- **ISO/TR 4804:2020** → **ISO/PAS 5112** *Road vehicles — Safety and cybersecurity for ADS*
- **BSI PAS 1881:2022** *Assuring the operational safety of automated vehicles*（英国）
- **UNECE GRVA WP.29 R157** — DDT fallback/MRM 引用
- **YD/T 4778-2024** 《基于 5G 的远程遥控驾驶信息交互系统 总体技术要求》（CCSA，2024-10-01 实施）—— 系统总体架构与通用功能要求
- **YD/T 4779-2024** 《城市运营车紧急接管技术要求》—— 对应 ROAM M7/M8 公共交通模式
- **YD/T 4780-2024** 《自动驾驶出租车云端控制技术要求》—— 百度牵头，对应 ROAM M1/M2 Robotaxi 模式
- **YD/T 4782-2024** 《物流车遥控驾驶技术要求》—— 对应 ROAM M9/M10 专用环境模式
- **YD/T 4783-2024** 《音视频传输技术要求》—— 远程遥控驾驶全链路的音视频编码、传输协议与时延质量要求，是整个系列的共性支撑标准
- *注：YD/T 系列覆盖了通信管道层的技术要求，但不涉及运营治理层（场景分类、处置流程、责任分工、KPI 体系）。ROAM 与 YD/T 属于不同层面的互补关系 —— 详见 [`standards/`](../standards/) 目录。*

### 行业最佳实践

- **Ottopia + Motional (2021-)** — "Indirect Control" 与 "Tele-Assist" 在 L4 Robotaxi 的商用部署；混合 AI 路径绘制界面是最广泛引用的 L4 远程操作参考架构，同时服务 DENSO 和 BMW
- **Vay Technology (Hamburg/Las Vegas, 2023-)** — 首个公路商用远程驾驶共享用车服务；直接控制 + 冗余 LTE 绑定链路，累计 >1000 次付费出行无安全事故
- **DJI FlightHub 2 Virtual Cockpit** — 三段式操作员界面（地图 + 设备信息 + 控制面板）+ 力反馈控制器

### ROAM 层级映射
- **L2 AI 辅助人工确认**：主要依赖间接控制能力（waypoint、approval）
- **L3 远程驾驶**：依赖直接控制能力（低延迟、高可靠）

---

## 支柱三：无线通信网络（Wireless Communication Networks）

### 核心能力
- **5G URLLC**：1 ms 空口延迟，99.999% 可靠性
- **确定性网络切片**：为 L4 远程运营保留专用带宽
- **V2X (C-V2X)**：车路协同，补充视距外感知
- **5G-Advanced (5.5G)**：进一步提升容量和可靠性
- **LEO 卫星备份**：地面网络中断时的冗余
- **多路径聚合**：多运营商、多技术冗余提升可用性

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| 端到端延迟（上行视频） | ≤ 50 ms（3GPP），≤ 20 ms（5G-A 拉伸目标） | 3GPP TS 22.186 |
| 可靠性 | 99.999% 包在延迟预算内 | 3GPP URLLC |
| 上行吞吐量（多摄像头） | ≥ 25 Mbps/车 | 3GPP |
| 抖动（ToD 直接控制） | ≤ 5 ms | 3GPP |
| 年可用性 | > 99.99% | 行业目标 |

### 学术文献

1. **Rahman, A., et al. (2023).** "A Comprehensive Survey on 5G-and-Beyond Networks with UAVs." *IEEE Journal on Selected Areas in Communications*, 41(1). — 全面的 URLLC 综述，适用于地面 AV 远程操作。

2. **Saad, W., Bennis, M., & Chen, M. (2022).** "A Vision of 6G Wireless Systems." *IEEE Network*. DOI:10.1109/MNET.001.1900287 — 定义了远程操作所需的 beyond-URLLC 服务类。

3. **Ansari, R. I., et al. (2024).** "5G and beyond for autonomous vehicles: A survey of V2X, edge computing and network slicing." *IEEE Access*. — 连接网络切片与 AV 用例的最新综述。

4. **Garcia, M. H. C., Molina-Galan, A., Boban, M., et al. (2021).** "A Tutorial on 5G NR V2X Communications." *IEEE Communications Surveys & Tutorials*, 23(3), 1972-2026. DOI:10.1109/COMST.2021.3057017 — 任何 5G V2X 论文必引的权威 tutorial。

5. **Liu, Y., et al. (2024).** "5G-Advanced: Expanding the Frontiers of 5G." *IEEE Communications Standards Magazine*. — Release 18 (5G-A/5.5G) 对远程操作的相关特性。

### 标准

- **3GPP TS 22.186 v17** *Service requirements for enhanced V2X scenarios* — 定义"远程驾驶"服务类：5 ms E2E 延迟、99.999% 可靠性、25 Mbps 上行
- **3GPP TR 22.886** — V2X 用例研究包含远程操作
- **3GPP Release 17（URLLC 增强）** 和 **Release 18（5G-Advanced）**
- **IEEE 802.11bd-2023** *Next Generation V2X*
- **ITU-T Y.3106** *QoS requirements for low-latency services over IMT-2020*
- **GB/T 41998-2022** 《智能网联汽车 数据通用要求》
- **YD/T 3977-2021** 《基于 LTE 的车联网无线通信技术 直连通信系统总体技术要求》（C-V2X）
- **YD/T 4778-2024** 《基于 5G 的远程遥控驾驶信息交互系统 总体技术要求》—— 3GPP TS 22.186 "Remote Driving" 场景在中国的行业实施标准
- **YD/T 4783-2024** 《音视频传输技术要求》—— 远程遥控驾驶全链路音视频编码与传输协议，是通信支柱的关键共性标准

### 行业最佳实践

- **5GAA 白皮书 "Tele-operated Driving (ToD): System Requirements Analysis and Architecture" (2021, 2023 更新)** — 5G 远程操作的事实产业规范；定义延迟预算、回退行为、QoS 映射
- **China IMT-2020 Promotion Group "5G V2X Phase 3 Test Specification"** — 对齐 3GPP R17 与中国 C-V2X 部署的国家测试框架
- **5G-MOBIX（EU，2018-2022）** — 跨境 5G V2X 走廊示范
- **T-Mobile × Aurora** — 美国商用 5G 用于重卡远程操作

### ROAM 层级映射
- **所有三层**都依赖可靠通信
- **L3 直接控制**对通信质量要求最高
- **L1 AI 自主**在通信失联时作为降级兜底（MRM）

---

## 支柱四：AI 辅助决策与信任校准（AI Decision Support & Trust Calibration）

### 核心能力
- **决策置信度量化**：AI 决策的可信度实时评估
- **自动升级机制**：基于信任度动态切换 L1/L2/L3
- **可信 AI**：符合 NIST AI RMF、EU AI Act 的高风险 AI 治理要求
- **LLM 增强决策**：利用大语言模型提升复杂场景的解释和判断

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| LLM 辅助决策准确率 vs 延迟 | > 95%（与人类专家一致），< 2 s 响应 | 研究目标 |
| 信任校准误差（过度+不足） | < 15% | NIST AI RMF |
| 不确定性覆盖（ECE） | < 5% | NIST AI RMF Measure 功能 |
| 从 L1 升级到 L2 的判断延迟 | < 500 ms | 行业目标 |

### 学术文献

1. **Cui, C., Ma, Y., Cao, X., Ye, W., Wang, Z., et al. (2024).** "A Survey on Multimodal Large Language Models for Autonomous Driving." *IEEE/CVF WACV 2024 Workshop LLVM-AD*. — 映射 LLM/VLM 在 AD 中角色的最全面早期综述。

2. **Wang, Y., Jiao, R., Zhan, S. S., et al. (2024).** "LLM4AD: Large Language Models for Autonomous Driving — Concept, Review, Benchmark, Experiments, and Future Trends." *arXiv:2410.15281*. — 识别"信任、透明度、延迟"为部署的关键阻碍。

3. **Sha, H., Mu, Y., Jiang, Y., et al. (2023).** "LanguageMPC: Large Language Models as Decision Makers for Autonomous Driving." *arXiv:2310.03026 / ICRA 2024*. — 基于链式思考的 LLM 决策框架。

4. **Lee, J. D., & See, K. A. (2004).** "Trust in Automation: Designing for Appropriate Reliance." *Human Factors*, 46(1), 50-80. — 任何信任校准论证的必引经典，NIST AI RMF 引用。

5. **Hoffman, R. R., Mueller, S. T., Klein, G., & Litman, J. (2023).** "Measures for Explainable AI." *Frontiers in Computer Science*, 5. DOI:10.3389/fcomp.2023.1096257 — 将 XAI 辅助决策的信任度量化。

6. **Cui, Z., et al. (2026).** "C-TRAIL: A Commonsense World Framework for Trajectory Planning in Autonomous Driving." *IEEE Transactions on Vehicular Technology*. — 引入双重信任（常识+运动学）和自适应信任校准机制。

### 标准/框架

- **NIST AI RMF 1.0 (2023 年 1 月)** + **Generative AI Profile (2024 年 7 月)** — Govern/Map/Measure/Manage 四大核心功能
- **EU AI Act (Regulation 2024/1689, 2024 年 8 月生效)** — Annex III 将"道路车辆中的安全组件"列为高风险 AI
- **ISO/IEC 42001:2023** *AI Management System* — 首个可认证的 AIMS 标准
- **ISO/IEC TR 5469:2024** *Functional safety and AI systems* — 桥接 26262/21448 与 AI
- **IEEE 7000-2021** *Model Process for Addressing Ethical Concerns during System Design*
- **GB/T 42755-2023** 《人工智能 机器学习系统风险管理要求》

### 行业最佳实践

- **Google/Waymo "Safety Case for Fully Autonomous Operations" (2023)** — 包含 AI 置信度门限与远程协助升级策略
- **MIT AgeLab / Toyota CSRC "C-TRAIL"** — 操作员信任校准研究框架
- **NVIDIA DriveOS** — 硬件隔离的安全 AI 计算架构

### ROAM 层级映射
- **L1 AI 自主**：信任校准决定 L1 占比的理论上限
- **L2 AI 辅助**：AI 置信度是人工介入的判断依据
- **跨层升级**：信任度下降是自动升级的触发条件

---

## 支柱五：网络安全与数据保护（Cybersecurity & Data Protection）

### 核心能力
- **整车网络安全**：从制造到运营全生命周期管理
- **软件更新安全**：OTA 推送的防篡改、防回滚
- **数据主权**：符合各国数据跨境传输法律
- **隐私保护**：乘客、车主、操作员的个人信息保护
- **远程控制通道安全**：防劫持、防重放、防中间人攻击

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| 补丁延迟（严重 CVE → OTA 交付） | < 30 天 | Auto-ISAC 基准 |
| 漏洞 SLA（CVSS ≥ 9.0） | 修复 < 90 天 | CISA ICS 指南 |
| 数据本地化（中国） | 100% 重要数据在岸 | 中国《汽车数据安全管理若干规定》 |
| 远程控制会话加密 | AES-256 + TLS 1.3 | 行业最佳实践 |

### 学术文献

1. **Checkoway, S., McCoy, D., Kantor, B., et al.** "Comprehensive Experimental Analyses of Automotive Attack Surfaces." *USENIX Security 2011*. — 汽车网络安全的起源论文，必引。

2. **Ring, M., et al. (2023).** "A Survey on Automotive Cybersecurity based on ISO/SAE 21434 and UN R155." *IEEE Access*, 11. — 标准到实践的最新综合。

3. **Sommer, F., Dürrwang, J., & Kriesten, R. (2022).** "Survey and Classification of Automotive Security Attacks." *Information*, 13(5), 238 (MDPI). — 对齐 21434 TARA 的更新攻击分类。

4. **Kim, S., & Shrestha, R. (2023).** "Automotive Cyber Security: Introduction, Challenges, and Standardization." Springer. ISBN 978-981-19-8052-4 — 标准链的教科书级参考。

5. **Li, Z., et al. (2024).** "Protection of Personal Information in the Era of Autonomous Vehicles: China's Dilemma and Legal System Reactions." *World Electric Vehicle Journal*, 17(2), 60 (MDPI). — 专门讨论 PIPL + 汽车数据规则。

### 标准

- **ISO/SAE 21434:2021** *Road vehicles — Cybersecurity engineering*
- **UN Regulation No. 155 (CSMS)** — 欧盟新车型自 2022 年 7 月起强制，所有新车自 2024 年 7 月起强制
- **UN Regulation No. 156 (SUMS/OTA)**
- **ISO 24089:2023** *Road vehicles — Software update engineering*
- **ISO/IEC 27001:2022** — 信息安全管理（车辆后端复用）
- **GB 44495-2024** 《汽车整车信息安全技术要求》（强制性，2026-01-01 生效）
- **GB 44496-2024** 《汽车软件升级通用技术要求》（强制性 OTA，2026-01-01 生效）
- **GB/T 41871-2022** 《信息安全技术 汽车数据处理安全要求》
- **中国 PIPL (2021) + DSL (2021) + 网信办《汽车数据安全管理若干规定》(2021 年 10 月)**
- **EU GDPR + EDPB Guidelines 01/2020 on connected vehicles**

### 行业最佳实践

- **Auto-ISAC "Automotive Cybersecurity Best Practices" (2022 更新)** — 对齐 21434 的行业共识手册
- **BSI TR-03165（德国）/ ENISA "Good Practices for Security of Smart Cars" (2023)** — 欧洲监管认可的最佳实践
- **Tesla Cybersecurity Team** — bug bounty 最高 $1M，公开 responsible disclosure
- **Mercedes-Benz VSOC** — 整车厂级别的 Vehicle Security Operations Center

### ROAM 层级映射
- **所有层级**都依赖安全可信的通信通道
- **L2/L3**涉及操作员远程指令，安全性要求更高
- **数据所有权**（M4/M5 模式）是新的挑战

---

## 支柱六：运营组织与人因（Operations Organization & Human Factors）

### 核心能力
- **操作员资质认证**：类比飞行员驾照的认证体系
- **持续训练**：应对新场景和系统升级的培训
- **工作负荷管理**：排班、休息、疲劳监控
- **跨时区协同**：全球化 ROC 的协调机制
- **应急响应组织**：大规模事件的协调处置

### 关键指标
| 指标 | 目标值 | 来源 |
|------|-------|------|
| 最大连续监管班次 | ≤ 2 小时 | UAV 运营 + Waymo 披露 |
| 操作员-车辆比 | 1:1（直接驾驶）/ 1:5-10（远程协助） | Motional/Ottopia 披露 |
| 初始训练时长 | ≥ 120 h + 年度 ≥ 20 h | CA DMV + UAV 类比 |
| 情境感知恢复时间 | < 10 s | Mutzenich 2021 基准 |

### 学术文献

1. **Cummings, M. L., & Ryan, J. (2014).** "Who is in Charge? The Promises and Pitfalls of Driverless Cars." *TR News*, 292. — 从 UAV 到 AV 教训迁移的经典文献。

2. **Cummings, M. L., Mastracchio, C., Thornburg, K. M., & Mkrtchyan, A. (2013).** "Boredom and Distraction in Multiple Unmanned Vehicle Supervisory Control." *Interacting with Computers*, 25(1), 34-47. — 多车监管中警觉性衰减的开创性工作——直接适用于 L4 远程操作员的监管范围。

3. **Mutzenich, C., Durant, S., Helman, S., & Dalton, P. (2021).** "Updating our understanding of situation awareness in relation to remote operators of autonomous vehicles." *Cognitive Research: Principles and Implications*, 6(1), 9. DOI:10.1186/s41235-021-00271-8 — 明确为 AV 远程操作员重构 SA 理论。

4. **Kettwich, C., Schrank, A., & Oehl, M. (2021).** "Teleoperation of Highly Automated Vehicles in Public Transport." *Multimodal Technologies and Interaction*, 5(5), 26 (MDPI). — DLR 发表的带工作负荷度量的 HMI 评估。

5. **Neumeier, S., et al. (2019).** "Teleoperation: The Holy Grail to Solve Problems of Automated Driving? Sure, but Latency Matters." *AutomotiveUI 2019*. — AV 远程操作被引用最多的实证工作负荷研究。

6. **Tener, F., & Lanir, J. (2022).** "Driving from a Distance: Challenges and Guidelines for Autonomous Vehicle Teleoperation Interfaces." *CHI 2022*. DOI:10.1145/3491102.3501827 — ACM CHI 的人因设计指南。

7. **Cummings, M. L. (2026).** "What Self-Driving Companies Should Learn from Drone Remote Operations." *George Mason University College of Engineering*. — 美军 UAV 35 年经验的跨域教训。

### 标准/资质

- **FAA Part 107 Remote Pilot Certificate (14 CFR Part 107)** — AV 远程操作员认证的模板（知识测试 + 复训）
- **ICAO Doc 10019 — Manual on Remotely Piloted Aircraft Systems** — RPAS 操作员资格的国际框架
- **EASA Easy Access Rules for Unmanned Aircraft Systems (2022)** — 欧盟 RPAS 操作员能力框架
- **ISO 9241-210:2019** *Ergonomics of human-system interaction — Human-centred design*
- **ISO/TS 5255-1:2022** *Ergonomic aspects of remote operation*
- **SAE J3114 (Human Factors)** 和 **SAE J3016** — 远程操作员角色定义
- **CA DMV AV Deployment Permit Requirements** — 远程操作员资格条款
- **GB/T 40429-2021** 《汽车驾驶自动化分级》（中国 L0-L5 分级，引用远程回退）
- **中国民用无人驾驶航空器操作员管理规定（2023）** — 国内无人机操作员管理，可供 AV 参考

### 行业最佳实践

- **California DMV AV Deployment Regulations (Art. 3.8)** — 首个对训练有素的远程操作员提出监管要求；Waymo/Cruise 披露文件记录训练时长、班次限制、操作员-车辆比
- **DJI UTC + AOPA China UAV Certification** — 截至 2024 年已有 150 万+ 认证远程飞手；经过验证的大规模操作员资格流水线，直接可迁移至 AV 远程运营中心
- **Zoox Safety Report / Waymo "Safety Approach to the Remote Assistance Team" (2023)** — 公开描述疲劳限制、操作员训练课程（通常 4-8 周初训 + 复训）

### ROAM 层级映射
- **L2 AI 辅助**：操作员资质和训练是核心
- **L3 远程驾驶**：要求更高级别的认证（类比 CDL + 特种作业）
- **组织维度**：跨层协调、排班管理是组织能力

---

## 中国标准与国际标准的双语桥接

为支持中国学术期刊和国际会议的双向引用，以下是关键的双语标准对应关系：

| 国际标准 | 对应中国标准 | 领域 |
|---------|-------------|------|
| ISO 21448 | GB/T 44721 | SOTIF 预期功能安全 |
| ISO/SAE 21434 | GB 44495 | 汽车网络安全 |
| UN R156 | GB 44496 | OTA 软件升级 |
| SAE J3016 | GB/T 40429 | 自动驾驶分级 |
| 3GPP TS 22.186 | YD/T 3977 | C-V2X 通信 |
| 3GPP TS 22.186 Remote Driving | YD/T 4778—4783 | 5G 远程遥控驾驶（"1+4+1"系列） |
| ISO 34502 | GB/T 41798 | 场景测试 |

这些配对使中国研究者可以在双语语境下论证"中国标准与国际标准对接"，同时也为国际读者提供中国标准的对应查阅点。

---

## 技术支柱与 ROAM 模块的映射

| ROAM 模块 | 涉及的主要技术支柱 |
|----------|------------------|
| **模块 1：事件数据库** | 支柱 5（数据安全）、支柱 6（数据治理） |
| **模块 2：场景分类** | 支柱 1（感知决策） |
| **模块 3：参考架构** | **六大支柱全部** |
| **模块 4：评价基准** | 支柱 2（延迟）、支柱 3（通信）、支柱 6（人员） |

---

## 关键挑战与研究空白

基于六大支柱的梳理，本文识别出以下跨支柱的研究空白：

1. **支柱 1 × 支柱 4 融合**：AI 感知不确定性与决策信任校准的联合优化
2. **支柱 2 × 支柱 3 融合**：间接控制模式下的通信延迟补偿
3. **支柱 5 × 支柱 6 融合**：跨境 ROC 的数据合规与人员认证
4. **支柱 1 × 支柱 6 融合**：自动异常检测与操作员升级判断的协同
5. **六支柱 × ROAM 运营模式**：不同模式下支柱重要性的量化评估

这些跨支柱研究空白将构成 ROAM 平台和相关学术研究的下一步重点方向。

---

## 版本历史

- **v1.0** (2026-04): 初始发布，包含 50+ 学术文献、20+ 标准、15+ 行业最佳实践

---

*本文档是 ROAM 开源框架的核心组成部分。欢迎通过 GitHub Issues 提交修订建议和补充参考文献。*

**说明**：部分 DOI 需要在论文正式发表前核实。arXiv 条目（LLM4AD, LanguageMPC, Majstorović survey, Zhou SOTIF）为预印本，会议最终版可能略有差异。
