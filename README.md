# 电网多尺度建模（子任务 3）：EMT 简介与 PF/RMS/EMT 连接

本目录是第一次讨论分工中**第 3 项任务**的产出：EMT 简介 $+$ 多尺度建模（重点）。

## 结构

```
.
├── main.tex                  # 主汇报稿（xelatex，问题驱动，约 24 页）
├── sections/                 # 主稿各章
│   ├── 01_intro.tex          # 任务、问题、定义、索引
│   ├── 02_q1_emt.tex         # Q1: EMT 是什么
│   ├── 03_q2_models.tex      # Q2: 三类模型对照
│   ├── 04_q3_multiscale.tex  # Q3: 潮流与 RMS 如何连接（核心）
│   ├── 05_q4_kuramoto.tex    # Q4: Kuramoto 与电网
│   └── 07_summary.tex        # 小结、对应项目书、建议
├── refs.bib                  # 参考文献（已联网核实）
├── md/                       # 基础性长文（步骤完整、可独立阅读）+ 讲稿
│   ├── 00_最小讲稿卡.md      # 6 句话版（只背这些）
│   ├── 07_明日组会讲稿.md    # 四层结构 + 三根锚点（忘词时往回找）
│   ├── 08_讲稿自测题库.md    # 18 题自测（汇报级 / 追问级 / 实战）
│   ├── 09_现场速讲卡.md      # ★ 上台只看这份：页码、翻页顺序、追问速答
│   ├── 01_电磁暂态与数值积分.md
│   ├── 02_从电路到潮流.md
│   ├── 03_多尺度与奇异摄动.md
│   ├── 04_混合仿真接口.md
│   ├── 05_Kuramoto与电网同步.md
│   └── 06_术语符号与软件benchmark.md
├── python/                   # 一图一脚本，可复现
├── figures/                  # fig01–fig13 的 pdf（矢量，供 tex）与 png（供 md）
├── data/                     # 关键数值数据（npz）
└── build/                    # 编译中间产物与 main.pdf
```

## 编译主稿

```bash
cd "电网多尺度建模"
xelatex -interaction=nonstopmode -output-directory=build main.tex
BIBINPUTS=".:build:" bibtex build/main
xelatex -interaction=nonstopmode -output-directory=build main.tex
xelatex -interaction=nonstopmode -output-directory=build main.tex
# 结果: build/main.pdf
```

依赖：`xelatex` + `ctex` + `enumitem` + `caption`（TinyTeX 可用 `tlmgr install` 补装）。

## 复现全部图

```bash
cd python
python3 fig01_timescales.py
python3 fig02_assumptions.py
python3 fig03_park.py
python3 fig04_phasor.py
python3 fig05_quasistatic.py
python3 fig06_singular.py
python3 fig07_spectrum.py
python3 fig08_hybrid.py
python3 fig09_interface.py
python3 fig10_swing_kuramoto.py
python3 fig11_kuramoto_transition.py
python3 fig12_kuramoto_grid.py
python3 fig13_model_chain.py
```

依赖：`numpy`、`scipy`、`matplotlib`、`networkx`。
中文字体：`Noto Sans CJK SC`（缺失时 `common.py` 会回退）。

## 学习路径（逐步理解）

推荐顺序（每步读完先做该 md 末尾的自测题，再看下一步）：

| 步 | 内容 | 目标 |
|---|---|---|
| 0 | 主稿 `build/main.pdf` 的目录 + 表 1 | 知道全局有 4 个问题、13 张图 |
| 1 | `md/02_从电路到潮流.md` §1–§5 | 建立“相量 → 节点方程 → 潮流 → 牛顿法”的直觉 |
| 2 | `md/01_电磁暂态与数值积分.md` §0–§4 | 建立“瞬时域每步在解什么”的直觉 |
| 3 | 主稿图 1 + 表 2 | 理解“三类模型 = 保留不同时间导数” |
| 4 | `md/03_多尺度与奇异摄动.md` §2–§5 | 理解“忽略快动态”的数学（慢流形、Tikhonov 误差界） |
| 5 | 主稿图 3 → 4 → 5 → 6 → 7 | 每张图对应 `md/03` 的一节，读完能自己推出准稳态误差式 |
| 6 | `md/04_混合仿真接口.md` §2–§7 | 理解接口变量、延迟误差 $\omega\tau\cot\theta$ 与 Nyquist |
| 7 | `md/05_Kuramoto与电网同步.md` §2–§4 | 理解 swing → Kuramoto 的退化与相变 $K_c$ |
| 8 | 回到主稿逐章的“小问题” | 自测；不会的回到对应 md 与图 |

## 十三个结论速览

| 图 | 一句话结论 |
|---|---|
| fig01 | 同一电网现象跨越 15 个数量级，三类模型各覆盖一段 |
| fig02 | 三模型对每个物理过程的保留/近似/忽略清单 |
| fig03 | 平衡正序时 dq 为直流，不平衡时出现 $2\omega$ 纹波（相量法失效） |
| fig04 | 相量法丢掉的暂态按 $e^{-t/\tau}$ 衰减，最坏合闸时与稳态同量级 |
| fig05 | 准稳态误差 $\approx m(\Omega/\omega)\sin\phi_z$，数值验证斜率一致 |
| fig06 | RMS 是 EMT 在 $\varepsilon\to0$ 的慢流形极限 |
| fig07 | 线性化系统特征值分两团，刚度比 $\sim5\times10^4$ |
| fig08 | 混合仿真接口交换“瞬时波形 $\leftrightarrow$ 基频相量” |
| fig09 | 接口两条硬约束：Nyquist 混叠与 $\omega\tau\cot\theta$ 延迟误差 |
| fig10 | $R=0$ 时 swing 与 Kuramoto 完全重合；偏差 $\propto R/X$ |
| fig11 | 同步相变，$K_c=2\gamma$（全连接 + Lorentzian） |
| fig12 | 稀疏网络同步更难，且从网络中心扩散 |
| fig13 | 完整 DAE $\to$ RMS $\to$ PF $\to$ Kuramoto 的降阶链条与信息损失 |

## 备注

- 主稿每个结论都标注了可回溯的图/公式/脚本；每章末尾有“小问题”就地答疑。
- 图的 pdf 供 LaTeX 引用（矢量），png 供 md 内嵌（Markdown 不能显示 pdf）。
- 文献均经联网核实（DOI/卷期），见 `refs.bib`。
- fig02 在主稿中以彩色表格（表 2）呈现，图文件仍保留供 md 版使用；
  其余 12 张图在主稿中以插图呈现，宽度统一为 `0.99\textwidth`。
