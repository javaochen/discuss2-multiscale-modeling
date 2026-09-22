# 术语、符号、软件与 benchmark 清单

> 本文是三份用途合一的参考页：
> （1）术语表——避免同一概念在汇报中被叫成不同名字；
> （2）符号表——本项目全部文档 中所有数学符号的统一定义；
> （3）工具与数据清单——第二次讨论“确定数据 + benchmark”时可直接使用。
>
> **用法**：作为术语与符号的查阅页，也可作为第二次讨论“确定数据与 benchmark”的清单。

---

## 1. 术语表

| 中文 | 英文 / 缩写 | 定义（本报告口径） |
|---|---|---|
| 电磁暂态 | Electromagnetic Transient, EMT | 直接求解三相瞬时 $v(t),i(t)$、保留全部 $L,C$ 微分的模型，含开关 |
| 机电暂态 | Electromechanical Transient | 保留转子角/转速/慢控制动态，网络用相量代数的模型，即 RMS |
| 相量 | Phasor | 把窄带正弦的幅值与相位打包成复数；成立前提是包络慢变 |
| 准稳态 | Quasi-Steady-State | 令相量包络的导数 $=0$ 得到的近似 |
| 潮流 | Power Flow, PF | 稳态节点功率平衡方程（代数） |
| 准稳态时序 | Quasi-Static Time-Series, QSTS | 逐时点解潮流，用于承载力/调压设备动作统计 |
| 承载力 | Hosting Capacity, HC | 在全部约束下可接入的 DER 最大容量 |
| 慢流形 | Slow Manifold | 令 $\varepsilon\to0$ 后快变量被约束到的曲面 $\bm z=\bm h(\bm x)$ |
| 边界层 | Boundary Layer | 初值到慢流形之间的 $O(\varepsilon)$ 快过渡段 |
| 刚度比 | Stiffness Ratio | 系统特征值最大与最小模之比 |
| 接口母线 | Interface Bus | 混合仿真中 EMT 与 RMS 子系统的边界节点 |
| 滑动 DFT | Sliding DFT | 用一个工频窗口从瞬时波形提取基频相量的算法 |
| 序参量 | Order Parameter | Kuramoto 中度量同步程度的 $r\in[0,1]$ |
| 临界耦合 | Critical Coupling | 出现同步相变的最小耦合强度 $K_c$ |
| 构网型 / 跟网型 | GFM / GFL | 变流器控制的两类基本模式（电压源型 / 电流源型） |
| 下垂控制 | Droop Control | $P$–$f$、$Q$–$V$ 线性关系实现无通信功率分配 |

---

## 2. 符号表

### 2.1 网络与潮流

| 符号 | 含义 | 单位/备注 |
|---|---|---|
| $n$ | 节点数 | — |
| $V_i,\theta_i$ | 节点 $i$ 电压幅值、相角 | pu / rad |
| $P_i,Q_i$ | 节点注入有功、无功 | pu |
| $G_{ik},B_{ik}$ | 节点导纳矩阵的实部、虚部 | pu |
| $R_{ik},X_{ik}$ | 支路电阻、电抗 | pu |
| $S_i=P_i+\jmath Q_i$ | 复功率 | pu |
| $\bm Y,\bm G,\bm B$ | 节点导纳矩阵及其实虚部 | — |
| $\bm J$ | 牛顿法雅可比矩阵 | — |
| $\theta_{ik}$ | $\theta_i-\theta_k$ | rad |

### 2.2 动态与 EMT

| 符号 | 含义 | 单位/备注 |
|---|---|---|
| $\bm x,\bm y$ | 状态变量、代数量 | — |
| $\bm f,\bm g$ | 微分方程、代数约束 | — |
| $\bm z$ | 快变量（EMT/电磁） | — |
| $\varepsilon$ | 快慢时间常数比 | — |
| $\Delta t_e,\Delta t_r$ | EMT、RMS 步长 | s |
| $N$ | 步长比 $\Delta t_r/\Delta t_e$ | — |
| $L,C,R$ | 电感、电容、电阻 | H, F, Ω |
| $Z_c,\tau$ | 波阻抗、行波时间 | Ω, s |
| $\lambda_i$ | 特征值 | rad/s |
| $\kappa$ | 刚度比 | — |
| $\omega_s$ | 同步角频率 $2\pi\cdot50$ | rad/s |

### 2.3 相量与接口

| 符号 | 含义 | 单位/备注 |
|---|---|---|
| $\underline V,\underline I$ | 电压、电流相量 | pu |
| $V(t),I(t)$ | 复包络 | pu |
| $Z(\jmath\omega_s)=R+\jmath\omega_sL$ | 阻抗 | Ω |
| $\phi_z$ | 阻抗角 $\arctan(\omega_sL/R)$ | rad |
| $\Omega$ | 包络带宽 | rad/s |
| $m$ | 包络调制深度 | — |
| $\underline V(t)$（滑动 DFT） | 提取的相量 | pu |
| $\tau_d$ | 接口延迟 | s |
| $Y_n,I_n$ | 接口诺顿导纳、电流源 | pu |
| $E_{th},Z_{th}$ | 接口戴维南等值 | pu |

### 2.4 Kuramoto

| 符号 | 含义 | 电网对应 |
|---|---|---|
| $\theta_i$ | 振子相位 | 相角 / 转子角 $\delta_i$ |
| $\omega_i$ | 自然频率 | 有功不平衡 |
| $K,K_{ij}$ | 耦合强度 | $V_iV_jB_{ij}$ |
| $r,\psi$ | 序参量、平均相位 | 同步程度 |
| $g(\omega)$ | 自然频率分布 | 不平衡的分布 |
| $K_c$ | 临界耦合 | 维持同步的最小耦合 |
| $\gamma$ | Lorentzian 分布宽度 | 不平衡离散度 |
| $M,D$ | 惯性常数、阻尼系数 | s, pu |
| $P_{m},P_{e}$ | 机械、电磁功率 | pu |

---

## 3. 软件清单

### 3.1 潮流 / QSTS / 优化
- **MATPOWER**（MATLAB）：潮流、OPF、连续潮流，教学与算法原型首选；
- **pandapower / PYPOWER**（Python）：易与数据管线集成；
- **OpenDSS**：三相不平衡配电网潮流与 QSTS，支持 DER 与调压器模型；
- **PSS®E / DIgSILENT PowerFactory**：工业级，含动态与 EMT 模块；
- **GridLAB-D**：配电系统时序仿真，含住宅负荷模型。

### 3.2 RMS（机电暂态）
- PSS®E、PowerFactory、Dynaωo（开源，研究常用）、
  ANDES（Python，现代开源）、PSAT、OpenModelica。

### 3.3 EMT（电磁暂态）
- PSCAD/EMTDC、EMTP-RV、ATP-EMTP、PowerFactory（EMT）、
  MATLAB/Simulink Simscape Electrical、OpenModelica；
  研究型：MATEMTP、Dynaωo EMT 扩展。

### 3.4 混合仿真框架
- HELICS（co-simulation 调度）、GridPACK（HPC 相量）、
  GridLAB-D（三相配电）、以及 T&D co-simulation 研究平台。

---

## 4. benchmark 清单（第二次讨论可直接采用）

### 4.1 输电网
| 系统 | 节点数 | 用途 |
|---|---|---|
| IEEE 9（WSCC 3 机） | 9 | EMT/RMS/潮流三方对照，本项目 fig12 已用 |
| IEEE 14 / 30 / 57 | 14/30/57 | 潮流与无功优化 |
| New England IEEE 39 | 39 | 机电暂态与振荡研究 |
| IEEE 118 / 300 | 118/300 | 大规模算法性能 |

### 4.2 配电网
| 系统 | 特点 | 用途 |
|---|---|---|
| IEEE 13 节点 | 三相不平衡、单相支路 | 三相潮流、DER 接入 |
| IEEE 34 节点 | 长馈线、调压器 | 电压越限、QSTS |
| IEEE 123 节点 | 大规模不平衡 | 承载力、优化 |
| CIGRE MV/LV | 欧洲典型网络 | 光伏高渗透场景 |
| EPRI 电路 | 含谐波源 | 电能质量 |

### 4.3 变流器 / 直流
- CIGRE B4 直流基准；WECC 第二基准（含 IBR）；
- 变流器 LCL 滤波器算例、弱电网短路比算例。

---

## 5. 数据来源建议

| 数据 | 来源 |
|---|---|
| 网络拓扑/参数 | MATPOWER 算例、IEEE PES 测试馈线文档 |
| 光伏出力 | NREL PVWatts、DOE 数据集 |
| 负荷曲线 | IEEE 测试馈线负荷、OpenEI |
| EV 充电 | 充电站数据集、ACN/Eluminocity 等公开数据 |
| 风速/风电 | NREL WIND Toolkit |
| 电价/市场 | 公开市场出清数据（可选） |

**注意**：DER 时序的时间分辨率必须与模型匹配——
QSTS 需要 1–15 min 分辨率，EMT 需要 μs 级波形，二者不可混用。

---

## 6. 使用说明

- §1 术语表用于统一汇报口径，避免同一概念被叫成不同名字；
- §2 符号表覆盖本项目文档中的全部数学符号；
- §3--5 可作为第二次讨论“确定数据与 benchmark”的清单。
