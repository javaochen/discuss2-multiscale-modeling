"""fig02: 三类模型对物理过程的"保留 / 近似 / 忽略"矩阵。

行是物理过程或动态, 列是 PF-QSTS / RMS / EMT。
0 = 忽略 (或退化为代数约束), 1 = 近似保留 (准稳态/平均/参数化), 2 = 完整保留。
"""
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from common import C_EMT, C_PF, C_RMS, plt, save

procs = [
    "网络 KCL / KVL (瞬时)",
    "网络 L,C 电磁暂态  dv/dt, di/dt",
    "分布参数 / 行波传播",
    "同步机定子磁链动态 (快)",
    "转子摇摆动态 (慢)",
    "调速器 / 原动机动态",
    "励磁 / AVR 动态",
    "变流器 PWM 开关过程",
    "逆变器内环电流控制",
    "PLL / 外环控制",
    "三相不平衡与负序/零序",
    "非额定频率下的偏离",
    "全阶微分方程 (未降阶)",
]
# 0 = 忽略, 1 = 近似, 2 = 完整
M = np.array([
    [1, 1, 2],   # KCL/KVL
    [0, 0, 2],   # 网络电磁暂态
    [0, 0, 2],   # 行波
    [0, 0, 2],   # 定子磁链
    [0, 2, 2],   # 转子摇摆
    [0, 1, 2],   # 调速器
    [0, 1, 2],   # AVR
    [0, 0, 2],   # PWM
    [0, 1, 2],   # 内环
    [0, 1, 2],   # PLL/外环
    [1, 1, 2],   # 不平衡
    [0, 1, 2],   # 非额定频率
    [0, 1, 2],   # 全阶微分
])

symbols = {0: "×", 1: "≈", 2: "√"}
cmap = ListedColormap(["#f5b7b1", "#fdebd0", "#a9dfbf"])
textcolor = {0: "#922b21", 1: "#7d6608", 2: "#145a32"}

fig, ax = plt.subplots(figsize=(6.6, 6.2))
ax.imshow(M, cmap=cmap, vmin=-0.5, vmax=2.5, aspect="auto")

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, symbols[M[i, j]], ha="center", va="center",
                fontsize=15, color=textcolor[M[i, j]], fontweight="bold")

ax.set_xticks(range(3))
ax.set_xticklabels(["PF / QSTS", "RMS", "EMT"], fontsize=11)
ax.set_yticks(range(len(procs)))
ax.set_yticklabels(procs, fontsize=8.8)
ax.set_xticks(np.arange(-0.5, 3, 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(procs), 1), minor=True)
ax.grid(which="minor", color="white", lw=1.2)
ax.grid(which="major", visible=False)
ax.tick_params(which="minor", length=0)

for x, c in zip([0, 1, 2], [C_PF, C_RMS, C_EMT]):
    ax.get_xticklabels()[x].set_color(c)

ax.set_title("三类模型对物理过程的保留程度\n(√ 完整保留,  ≈ 准稳态/平均/参数化,  × 忽略或退化为代数约束)",
             fontsize=10.5)
ax.legend(handles=[
    Patch(facecolor="#a9dfbf", label="完整保留"),
    Patch(facecolor="#fdebd0", label="近似保留 (准稳态/平均)"),
    Patch(facecolor="#f5b7b1", label="忽略 / 代数化"),
], loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8.5, frameon=False)

save(fig, "fig02_assumption_matrix")
