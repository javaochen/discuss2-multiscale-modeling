# -*- coding: utf-8 -*-
"""把推导块 2..7 重编号为 1..6，并修正全部分块引用。"""
import io
import re

FILES = ['sections/01_intro.tex', 'sections/04_q3_multiscale.tex',
         'sections/05_q4_kuramoto.tex', 'sections/09_appendix.tex',
         'md/07_明日组会讲稿.md', 'md/08_讲稿自测题库.md']

def repl(m):
    n = int(m.group(2))
    return m.group(1) + ' ' + str(n - 1)

pat = re.compile(r'(推导块|块)\s*([2-7])')

for f in FILES:
    try:
        s = io.open(f, encoding='utf-8').read()
    except FileNotFoundError:
        continue
    n0 = len(pat.findall(s))
    s = pat.sub(repl, s)
    s = s.replace('推导块 1--7', '推导块 1--6').replace('推导块 1..7', '推导块 1..6')
    s = s.replace('块 1--7', '块 1--6')
    io.open(f, 'w', encoding='utf-8').write(s)
    print('renumbered', f, n0, 'references')
