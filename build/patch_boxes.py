# -*- coding: utf-8 -*-
"""把 7 个推导块改为 tcolorbox 盒子；图（浮动体）留在盒外。可重复运行（幂等）。"""
import io
from collections import defaultdict

FIG = r'\begin{figure}'

BLOCKS = [
    ('sections/03_q2_models.tex',
     r'\paragraph{推导：从 KCL 到功率平衡方程。}',
     r'\paragraph{关键观察。}',
     '推导块 1：从 KCL 到潮流方程',
     r'\textbf{起点}：KCL $\bm I=\bm Y\bm V$；\textbf{目标}：节点功率平衡方程（3 步）；\textbf{结论}：潮流方程不含时间导数；\textbf{支撑}：Q3 的工作点层连接。'),
    ('sections/04_q3_multiscale.tex',
     '\\subsubsection{Park 变换：为什么它能“消掉”载波}',
     FIG,
     '推导块 2：Park 变换——载波变直流',
     r'\textbf{起点}：三相正序 $+$ 变换矩阵；\textbf{目标}：证明 $v_d=V,\,v_q=0$（2 步）；\textbf{结论}：载波在 $dq$ 中变直流；\textbf{支撑}：准稳态判据。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsubsection{RL 支路的 $dq$ 方程：交叉耦合项从哪来}',
     r'\subsubsection{准稳态（相量）近似与误差判据}',
     '推导块 3：RL 支路的 dq 方程',
     r'\textbf{起点}：$abc$ 域 $RL$ 方程；\textbf{目标}：$dq$ 形式与交叉项来源（2 步）；\textbf{结论}：$\omega L$ 来自坐标旋转、非电磁暂态；\textbf{支撑}：EMT/RMS 的分界。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsubsection{准稳态（相量）近似与误差判据}',
     FIG,
     '推导块 4：准稳态误差判据',
     r'\textbf{起点}：复包络；\textbf{目标}：误差公式（3 步）；\textbf{结论}：$\varepsilon=m(\Omega/\omega_s)\sin\phi_z$；\textbf{支撑}：QSTS 是否可用的判据。'),
    ('sections/04_q3_multiscale.tex',
     r'\subsection{第三层：时间尺度分离与奇异摄动（数学本质）}',
     FIG,
     '推导块 5：奇异摄动与慢流形',
     r'\textbf{起点}：$\varepsilon\dot{\bm z}=\bm g(\bm x,\bm z)$；\textbf{目标}：慢流形与降阶（3 步）；\textbf{结论}：RMS $=$ EMT 在 $\varepsilon\to0$ 的降阶；\textbf{支撑}：前两层连接的合法性。'),
    ('sections/05_q4_kuramoto.tex',
     r'\subsection{为什么电网能用 Kuramoto：从 swing 方程推导}',
     FIG,
     '推导块 6：从 swing 方程到 Kuramoto',
     r'\textbf{起点}：swing 方程 $+$ 网络功率；\textbf{目标}：三假设下的退化（3 步）；\textbf{结论}：Kuramoto 是 swing 的严格退化；\textbf{支撑}：Q4“为什么能用”。'),
    ('sections/05_q4_kuramoto.tex',
     r'\subsection{同步相变：Kuramoto 给出的可解析结论}',
     FIG,
     '推导块 7：自洽方程与临界耦合',
     r'\textbf{起点}：序参量 $+$ 平均场；\textbf{目标}：临界耦合（4 步）；\textbf{结论}：$K_c=2/(\pi g(0))$；\textbf{支撑}：承载力宏观指标。'),
]

files = sorted({b[0] for b in BLOCKS})

def strip_boxes(lines):
    out, skip = [], False
    for L in lines:
        if skip:
            skip = False
            continue
        s = L.strip()
        if s.startswith(r'\begin{derivblock}'):
            skip = True
            continue
        if s == r'\end{derivblock}':
            continue
        if 'rule{0.45\\textwidth}' in L or s.startswith(r'\noindent\textbf{【推导块'):
            continue
        out.append(L)
    return out

# 阶段 0：清除旧的盒子与标记（幂等）
for f in files:
    lines = io.open(f, encoding='utf-8').read().split('\n')
    io.open(f, 'w', encoding='utf-8').write('\n'.join(strip_boxes(lines)))

# 阶段 1：定位并插入
ops = defaultdict(list)
for f, anchor, endanchor, title, info in BLOCKS:
    lines = io.open(f, encoding='utf-8').read().split('\n')
    s_hits = [i for i, L in enumerate(lines) if L.strip() == anchor]
    assert len(s_hits) == 1, ('start', f, anchor, len(s_hits))
    s = s_hits[0]
    e = None
    for i in range(s + 1, len(lines)):
        if lines[i].strip().startswith(endanchor):
            e = i
            break
    assert e is not None, ('end', f, endanchor)
    ops[f].append((s + 1, '\\begin{derivblock}{' + title + '}\n' + info))
    ops[f].append((e, '\\end{derivblock}\n'))

for f, items in ops.items():
    lines = io.open(f, encoding='utf-8').read().split('\n')
    for idx, text in sorted(items, key=lambda x: -x[0]):
        lines.insert(idx, text)
    io.open(f, 'w', encoding='utf-8').write('\n'.join(lines))
    print('boxed', f, len(items) // 2, 'blocks')
print('done')
