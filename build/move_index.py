# -*- coding: utf-8 -*-
"""把 §1.4 图表与脚本索引移到文末（08_index.tex），并把阅读路线改成有信息量的三处定位。"""
import io

src = 'sections/01_intro.tex'
lines = io.open(src, encoding='utf-8').read().split('\n')

i1 = next(i for i, L in enumerate(lines) if L.startswith(r'\subsection{图表与脚本索引}'))
i2 = next(i for i, L in enumerate(lines) if L.startswith(r'\subsection{阅读路线}'))

block = lines[i1:i2]
rest = lines[:i1] + lines[i2:]

io.open('sections/08_index.tex', 'w', encoding='utf-8').write(
    '\n'.join(block).rstrip() + '\n')

out, skip = [], False
for L in rest:
    if L.startswith(r'\subsection{阅读路线}'):
        out += [L, '',
                r'若时间有限，只读三处即可覆盖全部结论：表~\ref{tab:retention}（三模型保留矩阵）、'
                r'图~\ref{fig:chain}（由 EMT 到 Kuramoto 的降阶链）、'
                r'表~\ref{tab:assumptions}（每条结论的假设与失效条件）。',
                r'被追问时，按每章的推导块（【推导块 1--7】）定位到具体步骤与公式。', '']
        skip = True
        continue
    if skip:
        if L.startswith(r'\section{') or L.startswith(r'\subsection{'):
            skip = False
        else:
            continue
    out.append(L)

io.open(src, 'w', encoding='utf-8').write('\n'.join(out))
print('moved index section ->', i2 - i1, 'lines; 01_intro now', len(out), 'lines')
