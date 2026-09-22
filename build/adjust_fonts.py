# -*- coding: utf-8 -*-
"""放大文本型图（fig01/fig08/fig13）的图内字号，一次映射、不重复替换。"""
import io
import re

MAP = {8.0: 10.0, 8.2: 10.2, 8.4: 10.6, 8.5: 10.5, 8.8: 11.0,
       9.0: 11.0, 9.5: 12.0, 10.5: 13.5, 11.0: 13.5}

FILES = ['python/fig01_timescales.py', 'python/fig08_hybrid.py', 'python/fig13_model_chain.py']

def mapper(m):
    v = float(m.group(1))
    return 'fontsize=' + str(MAP.get(v, v))

for f in FILES:
    s = io.open(f, encoding='utf-8').read()
    n = len(re.findall(r'fontsize=([\d.]+)', s))
    s2 = re.sub(r'fontsize=([\d.]+)', mapper, s)
    io.open(f, 'w', encoding='utf-8').write(s2)
    print('adjusted', f, n, 'fontsize settings')
