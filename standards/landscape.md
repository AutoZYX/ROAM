# L4 远程运营与异常管理 标准现状扫描

**Standards Landscape Survey for L4 Remote Operations & Anomaly Management**

---

> 作者：Yuxin Zhang
> 日期：2026 年 4 月
> 版本：v1.0
> 数据源：Web Search 多次交叉验证

---

## 执行摘要

1. **国际标准层面空白显著**：ISO / SAE / UNECE 均无一部专门针对 L4 远程运营与运营异常管理的综合性参考框架标准
2. **欧洲已走在前面，但仅覆盖"远程驾驶"单一模式**：德国 StVFernLV（2025-12-01 生效）、英国 AV Act 2024 均为**法规**而非技术标准
3. **中国标准体系已有多点布局但彼此割裂**：通信口、汽车口、交通口、网安口四套体系并行，缺乏统一的参考架构
4. **最大的结构性缺口**：现有所有标准都是"要求型"（requirements-oriented），无一是"参考架构型"（reference architecture）
5. **可直接切入的机会**：CSAE 体系中**没有**专门的远程驾驶/运营团体标准（重要更正：T/CSAE 200-2021 实为《汽车用铝合金直锻工艺轮毂技术条件》，与远程驾驶无关）
6. **2026-04 重大监管转向**：武汉萝卜快跑事件后 14 天内，国家三部门召开全国安全监管会议，超 10 城同步收紧准入。监管逻辑从"包容审慎"转向"安全底线刚性化、全链条责任闭环化"，要求从单车安全扩展至"云-网-边-车"系统性安全全链条监管，这一转向为 ROAM 框架的标准化提案提供了强有力的产业需求论据

---

## A. 中国标准体系

### A.1 中国团体标准（团标）

| 标准号 | 名称 | 发布 | 范围 | 远程运营相关度 |
|-------|------|-----|------|--------------|
| T/CSAE 286.1/286.2-2022 | 功能型无人车 术语 / 技术要求 | 2022 | 低速功能型无人车，含远程接管的笼统要求 | 中 |
| T/CSAE 382-2024 | 智能网联汽车 自动驾驶系统要求及测试方法 高速公路及城市快速路 | 2024 | 高快速路 L3/L4 场景 | 低 |
| T/CSAE 309-2023 | 城市道路场景无人化测试 场地试验方法 | 2023 | 测试场景 | 低 |
| T/CITSA 48-2024 | 城市道路基础设施辅助自动驾驶车辆 能力分级规范 | 2024 | 路侧能力分级 | 低 |
| T/CSAE 247-2022 | 智能网联汽车道路试验监管系统技术要求 | 2022 | 测试监管平台 | 中（可借鉴） |

**核心结论**：T/CSAE 和 T/CITSA 体系**没有**一部专门的"L4 远程运营 / 异常管理"团体标准。T/CSAE 247-2022 是最接近的相邻标准，但它针对"道路试验监管"而非商业化运营。**这是 ROAM 切入 T/CSAE 或 T/CAICV 的直接机会。**

> ⚠️ **重要更正**：此前曾有资料引用 T/CSAE 200-2021 为《智能网联汽车 远程驾驶系统技术要求》，经核实该编号实际对应《汽车用铝合金直锻工艺轮毂技术条件》，与远程驾驶无关。

### A.2 中国行业标准（YD/T、JT 等）

| 标准号 | 名称 | 主管 | 状态 | 相关度 |
|-------|------|-----|------|------|
| **YD/T 4778-2024** | **基于 5G 的远程遥控驾驶信息交互系统 总体技术要求** | CCSA TC5 / 工信部 | **2024-10-01 实施** | **高** |
| **YD/T 4779-2024** | **城市运营车紧急接管技术要求** | CCSA | **2024** | **高** |
| **YD/T 4780-2024** | **自动驾驶出租车云端控制技术要求** | CCSA | **2024** | **高** |
| YD/T 4781-2024 | 高速车队远控技术要求 | CCSA | 2024 | 中 |
| YD/T 4783-2024 | 音视频传输技术要求 | CCSA | 2024 | 中 |

**重要性**：YD/T 4778-4783 系列是目前**最完整的远程遥控驾驶系列标准**，由信通院主导、工信部通信口归口。但侧重于 **5G 信道、技术接口、信息交互**，不涉及运营参考架构、场景分类、KPI 基准。

### A.3 中国国家标准（GB/T、GB）

| 标准号 | 名称 | 主管 | 状态 | 相关度 |
|-------|------|-----|------|------|
| GB/T 40429-2021 | 汽车驾驶自动化分级 | TC114 | 已发布 | 基础术语 |
| GB/T 41798-2022 | 智能网联汽车 自动驾驶功能场地试验方法及要求 | TC114 | 已发布 | 中 |
| GB/T 44721-2024 | 智能网联汽车 自动驾驶系统通用技术要求 | TC114 | 已发布 | 中 |
| GB/T 45312-2025 | 智能网联汽车 自动驾驶系统设计运行条件 | TC114 | 已发布 | 中 |
| GB 44495-2024 | 汽车整车信息安全技术要求 | TC114 | 2026-01-01 强制 | 网安 |
| GB 44496-2024 | 汽车软件升级通用技术要求 | TC114 | 2026-01-01 强制 | OTA |
| GB 44497-2024 | 智能网联汽车 自动驾驶数据记录系统（DSSAD） | TC114 | 2026-01-01 强制 | 中 |
| **强制性 GB 草案** | **智能网联汽车 自动驾驶系统安全要求**（含附录 C.2 远程协助） | **TC114/SC34** | **征求意见截止 2026-04-13，计划 2027-07-01 实施** | **高** |
| **GB/T 在研** | **自动驾驶营运车辆安全员技能要求与培训考核规范 第 2 部分：远程安全员**（计划号 20242301-T-348，主起草单位含萝卜运力） | **TC521 / 交通部** | **2024 立项，周期 18 个月** | **高** |
| 交通运输部规范性文件 | 自动驾驶汽车运输安全服务指南（试行） | 交通部 | 2023-11 | 规定安全员 1:3 比例 |

**中国体系的特征**：**行业维度割裂明显** —— 通信口 CCSA（5G / 信道）、汽车口 TC114（车辆功能安全）、交通口 TC521（人员 / 运营规范）、网安口（GB 44495 信息安全）**四套体系并行，但没有一个整合性的"运营中心参考架构"标准**。

---

## B. 国际标准与法规

### B.1 SAE 标准

| 标准号 | 名称 | 发布 | 与远程运营相关度 |
|-------|------|-----|----------------|
| SAE J3016_202104 | Taxonomy and Definitions for Terms Related to Driving Automation | 2021 | **明确拒绝**定义 teleoperation |
| SAE J3018_202012 | Safety-Relevant Guidance for On-Road Testing of Prototype ADS | 2020 | 仅车内安全员 |
| SAE J3216_202107 | Taxonomy for Cooperative Driving Automation | 2021 | V2X 协同非远程运营 |
| SAE J3131 | 自动驾驶架构定义 | — | 未覆盖远程运营 |

### B.2 ISO 标准

| 标准号 | 名称 | 发布 | 与远程运营相关度 |
|-------|------|-----|----------------|
| ISO 22737:2021 | ITS — Low-speed automated driving (LSAD) systems for predefined routes | 2021 | 仅低速封闭场景 |
| ISO 34501:2022 | Road vehicles — Test scenarios for ADS — Vocabulary | 2022 | 场景库非运营 |
| ISO 34502:2022 | Road vehicles — Test scenarios for ADS — Scenario based safety evaluation framework | 2022 | 场景库非运营 |
| ISO 21448:2022 | Road vehicles — Safety of the intended functionality (SOTIF) | 2022 | 概念层，未涉运营 |
| ISO/TR 4804:2020 | Road vehicles — Safety and cybersecurity for ADS | 2020 | 技术报告，非运营 |
| ISO 23793-1:2024 | Minimal risk manoeuvre (MRM) for automated driving — Framework | 2024 | 车端策略，非远程 |
| ISO/SAE 21434:2021 | Road vehicles — Cybersecurity engineering | 2021 | 网安 |

### B.3 法规与政府文件

| 法规 | 发布机构 | 状态 | 与远程运营相关度 |
|------|---------|------|----------------|
| UN GTR on ADS | UNECE WP.29 GRVA | **2024-06 启动，2026 中期交付草案** | 草案阶段 |
| Germany StVFernLV | 德国联邦 | **2025-12-01 生效** | 法规，仅覆盖远程驾驶 |
| UK Automated Vehicles Act 2024 | 英国议会 | **2024-05 通过** | 法规，NUiC operator 许可 |
| California CPUC AV Reporting 2024 | 加州公用事业委 | 2024 | 事故 / 停摆 / 脱离报告 |

**国际层面结论**：目前国际上**没有任何一部 ISO/SAE/IEC 标准**以"L4 远程运营与异常管理"为专门对象。德国 StVFernLV 和英国 AVA 是法规不是技术标准；UN GTR on ADS 仍在 2026 年草案阶段。

---

## C. 六大覆盖缺口

基于上述扫描，ROAM 项目的六个维度均无现有标准形成完整覆盖：

### 缺口 1：事故 / 异常分级与报告
- 仅加州 CPUC 有 trip-level 事故与停摆报告要求
- 中国**无统一事故分级体系**
- Wuhan Apollo Go 2026-03 批量停摆、Waymo SF 2025-12 电网停电、Cruise 2023-10 拖行行人等事件暴露了缺乏统一的严重度分级框架

### 缺口 2：运营异常场景分类法
- ISO 34501/34502 聚焦**车辆感知测试场景**
- **没有一部标准定义"运营阶段异常场景"**（如通信中断、红绿灯瘫痪、施工改道、群体停摆）

### 缺口 3：远程运营参考架构
- 所有现有标准都是"功能要求型"
- **没有一部**以 UML / 系统视图描述"AI 自主处置 + AI 辅助+人在环 + 人工远程驾驶"三层架构的参考模型

### 缺口 4：KPI 基准
- MTTR、AI 自主解决率、误升级率、干预延迟等 KPI 没有任何标准给出基准或测量方法

### 缺口 5：十类运营模式矩阵
- Robotaxi / OEM 直营 / 个人+OEM 订阅 / 共享 / 公共交通 / 无人配送 / 专用车辆等场景下的远程运营责任分配**无标准覆盖**
- 交通部 2023 试行指南仅给出 Robotaxi 1:3 安全员比例

### 缺口 6：多方责任矩阵
- 运营商 / OEM / 消费者 / 平台 / 保险方五方责任分配**无标准**
- UK AVA 提出了 ASDE 和 NUiC operator 两个角色，但未覆盖保险与平台

---

## D. 术语碎片化

不同标准中"远程协助"和"远程驾驶"经常混用或未定义：

| 术语 | SAE J3016 | ISO | YD/T 4778 | UK AVA | StVFernLV | 中国 GB 草案 |
|------|-----------|-----|-----------|--------|-----------|------------|
| Remote assistance | 未定义 | 未定义 | 未明确 | 未明确 | 未涉 | 远程协助（附录） |
| Remote driving / teleoperation | **明确拒绝** | 未定义 | 远程遥控驾驶 | NUiC operator | 远程操控 | 远程驾驶 |
| Remote monitoring | 未定义 | 未定义 | 云端监控 | 未明确 | 未涉 | 未涉 |
| Remote safety officer | 未涉 | 未涉 | 未涉 | 未涉 | 未涉 | 远程安全员（TC521） |

**术语不一致**是目前最大的基础性障碍。ROAM 的第一要务应是**锁定一套跨行业可通用的术语表**。

---

## E. 小结：ROAM 的战略空白

| 维度 | 现有标准覆盖 | ROAM 填补 |
|------|------------|----------|
| **分级定义**（What level） | SAE J3016 · GB/T 40429 | — |
| **SOTIF 安全论证**（Is it safe） | ISO 21448 · GB/T 44721 | — |
| **场景测试方法**（How to test） | ISO 34502 · GB/T 41798 | — |
| **网络安全**（Is it secure） | ISO/SAE 21434 · GB 44495 | — |
| **通信要求**（How fast） | 3GPP TS 22.186 · YD/T 4778-4783 | — |
| **事件分类体系** | — | 🆕 ROAM |
| **场景-处置映射** | — | 🆕 ROAM |
| **参考架构**（Who does what） | — | 🆕 ROAM |
| **KPI 基准** | — | 🆕 ROAM |
| **运营模式责任矩阵** | — | 🆕 ROAM |

---

## 参考

1. YD/T 4778-2024 - [国家数字标准馆](https://ndls.org.cn/standard/detail/952cf56990a5ec6f67cfba667f5704d3)
2. YD/T 4779-2024 - [国家数字标准馆](https://www.ndls.org.cn/standard/detail/6eaefd1bf79e3c0e286b2ad12c0e6073)
3. YD/T 4780-2024 - [国家数字标准馆](https://ndls.org.cn/standard/detail/6504dc066ff2498d578ffcfbdbf43e6e)
4. GB/T 44721-2024 - [国家标准全文公开系统](https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8AA1E95193C35E2BFF390DBE5B986DE8)
5. GB/T 45312-2025 - [国家数字标准馆](https://ndls.org.cn/standard/detail/a50a240964017ce8dd96f14e0f50dbef)
6. 强制性 GB 草案《智能网联汽车 自动驾驶系统安全要求》(2026-02 征求意见) - [CATARC](https://www.catarc.ac.cn/mobile/detail/0913d68668f44f689ee0c7128fcbf5ff)
7. TC521 GB/T 计划号 20242301-T-348 - [国家标准化管理委员会](https://std.samr.gov.cn/gb/search/gbDetailed?id=15C95F63A0DC0771E06397BE0A0A99EC)
8. 交通运输部《自动驾驶汽车运输安全服务指南（试行）》- [交通部政府信息公开](https://xxgk.mot.gov.cn/2020/jigou/ysfws/202312/t20231205_3962490.html)
9. SAE J3016_202104 - [SAE](https://www.sae.org/standards/content/j3016_202104/)
10. ISO 22737:2021 - [ISO](https://www.iso.org/standard/73767.html)
11. ISO 34501:2022 / 34502:2022 - [ISO TC22/SC33/WG9](https://standards.iteh.ai/catalog/tc/iso/ef4f9218-476b-4f71-a387-3251edc25b3e/iso-tc-22-sc-33-wg-9)
12. ISO 23793-1:2024 - [ISO](https://www.iso.org/standard/81711.html)
13. Germany StVFernLV - [Bird & Bird 法律解读](https://www.twobirds.com/en/insights/2026/germany/teleoperiertes-fahren-straenverkehr-fernlenk-verordnung-(stvfernlv)-seit-dezember-2025-in-kraft)
14. UK Automated Vehicles Act 2024 - [legislation.gov.uk](https://www.legislation.gov.uk/ukpga/2024/10)
15. California CPUC AV Reporting - [CPUC](https://www.cpuc.ca.gov/news-and-updates/all-news/cpuc-enhances-autonomous-vehicle-reporting-requirements-to-boost-safety-standards)

---

*本扫描结果将随着新标准的发布持续更新。欢迎通过 GitHub Issues 提交补充和修订建议。*
