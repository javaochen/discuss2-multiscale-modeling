# -*- coding: utf-8 -*-
"""给主稿中 7 个推导块加显式边界标记（不删改任何内容）。"""
import io

BLOCKS = [
    ('sections/03_q2_models.tex',
     r'\paragraph{推导：从 KCL 到功率平衡方程。}',
     r'\noindent\textbf{【推导块 1】}起点：KCL $\bm I=\bm Y\bm V$ $\Rightarrow$ 目标：节点功率平衡方程（3 步）$\Rightarrow$ 结论：潮流方程不含时间导数 $\Rightarrow$ 支撑：Q3 的工作点层连接。'),
    ('sections/04_q3_multiscale.tex',
     '\\subsubsection{Park 变换：为什么它能“消掉”载波}',
     r'\noindent\textbf{【推导块 2】}起点：三相正序 $+$ 变换矩阵 $\Rightarrow$ 目标：证明 $v_d=V,\,v_q=0$（2 步）$\Rightarrow$ 结论：载波在 $dq$ 中变直流 $\Rightarrow$ 支撑：准稳态判据。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsubsection{RL 支路的 $dq$ 方程：交叉耦合项从哪来}',
     r'\noindent\textbf{【推导块 3】}起点：$abc$ 域 $RL$ 方程 $\Rightarrow$ 目标：$dq$ 形式与交叉项来源（2 步）$\Rightarrow$ 结论：$\omega L$ 来自坐标旋转、非电磁暂态 $\Rightarrow$ 支撑：EMT/RMS 的分界。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsubsection{准稳态（相量）近似与误差判据}',
     r'\noindent\textbf{【推导块 4】}起点：复包络 $v=\Real\{Ve^{\jj\omega_s t}\}$ $\Rightarrow$ 目标：误差公式（3 步）$\Rightarrow$ 结论：$\varepsilon=m(\Omega/\omega_s)\sin\phi_z$ $\Rightarrow$ 支撑：QSTS 是否可用的判据。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsection{第三层：时间尺度分离与奇异摄动（数学本质）}',
     r'\noindent\textbf{【推导块 5】}起点：$\varepsilon\dot{\bm z}=\bm g(\bm x,\bm z)$ $\Rightarrow$ 目标：慢流形与降阶（3 步）$\Rightarrow$ 结论：RMS $=$ EMT 在 $\varepsilon\to0$ 的降阶 $\Rightarrow$ 支撑：前两层连接的合法性。'),
    ('sections/05_q4_kuramoto.tex',
     r'\subsection{为什么电网能用 Kuramoto：从 swing 方程推导}',
     r'\noindent\textbf{【推导块 6】}起点：swing 方程 $+$ 网络功率 $\Rightarrow$ 目标：三假设下的退化（3 步）$\Rightarrow$ 结论：Kuramoto 是 swing 的严格退化 $\Rightarrow$ 支撑：Q4“为什么能用”。'),
    ('sections/05_q4_kuramoto.tex',
     r'\subsection{同步相变：Kuramoto 给出的可解析结论}',
     r'\noindent\textbf{【推导块 7】}起点：序参量 $+$ 平均场 $\Rightarrow$ 目标：临界耦合（4 步）$\Rightarrow$ 结论：$K_c=2/(\pi g(0))$ $\Rightarrow$ 支撑：承载力宏观指标。'),
]

from collections import defaultdict
byfile = defaultdict(list)
for f, anchor, info in BLOCKS:
    byfile[f].append((anchor, info))

for f, items in byfile.items():
    lines = io.open(f, encoding='utf-8').read().split('\n')
    for anchor, info in items:
        hits = [i for i, L in enumerate(lines) if L.strip() == anchor]
        assert len(hits) == 1, (f, anchor, len(hits))
        i = hits[0]
        block = ['', r'\begin{center}\rule{0.45\textwidth}{0.4pt}\end{center}', info,
                 r'\begin{center}\rule{0.45\textwidth}{0.4pt}\end{center}', '']
        lines[i+1:i+1] = block
    io.open(f, 'w', encoding='utf-8').write('\n'.join(lines))
    print('marked', f, len(items), 'blocks')
print('done')
