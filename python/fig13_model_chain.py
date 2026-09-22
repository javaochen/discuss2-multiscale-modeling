"""fig13: 模型之间的简化关系（分叉结构，而非一条直线链）。

EMT --忽略网络电磁暂态--> RMS
RMS --令所有导数=0--> PF/QSTS      (静态化：丢掉时间维度)
RMS --恒幅值+无损纯感--> Kuramoto  (相角化：保留时间，消去网络与电压)
即：PF 与 Kuramoto 是 RMS 的两个并列简化，Kuramoto 不是“潮流的进一步简化”。
"""
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save

fig, ax = plt.subplots(figsize=(11.8, 8.6))
ax.set_xlim(0, 13.0)
ax.set_ylim(0, 11.6)
ax.axis("off")

BW, BH = 4.2, 2.0
box_kw = dict(boxstyle="round,pad=0.12", lw=2.0, fc="white")


def node(cx, cy, color, title, body, tsize=13.5, bsize=10.8):
    ax.add_patch(FancyBboxPatch((cx - BW / 2, cy - BH / 2), BW, BH,
                                ec=color, **box_kw))
    ax.text(cx, cy + 0.45, title, ha="center", va="center", color=color,
            fontsize=tsize, fontweight="bold")
    ax.text(cx, cy - 0.42, body, ha="center", va="center", fontsize=bsize,
            color="#2c3e50")


# 上：EMT
node(6.5, 10.2, C_EMT, "完整 EMT DAE",
     "变量 $v_{abc}(t),\\,i_{abc}(t)$（瞬时）\n步长 $1$–$50\\,\\mu$s｜含开关 / 行波")
# 中：RMS
node(6.5, 6.6, C_RMS, "RMS DAE",
     "状态 $\\delta,\\omega,E_q'$；代数 $V\\angle\\theta$\n步长 $1$–$10$ ms｜网络代数化")
# 左下：PF
node(2.6, 2.95, C_PF, "PF / QSTS（静态）",
     "变量 $V,\\theta$（无状态）\n代数方程｜QSTS 逐点求解")
# 右下：Kuramoto
node(10.4, 2.95, C_KUR, "Kuramoto（仅相角）",
     "变量仅 $\\delta_i$\n仍是微分方程｜恒幅值、无损纯感")

# 箭头：EMT -> RMS
ax.add_patch(FancyArrowPatch((6.5, 9.2), (6.5, 7.6),
                             arrowstyle="-|>", mutation_scale=20, lw=2.2, color=C_EMT))
ax.text(6.75, 8.4, "忽略网络电磁暂态 / 平均开关", fontsize=10.6, color=C_EMT,
        va="center", ha="left")

# 箭头：RMS -> PF
ax.add_patch(FancyArrowPatch((5.5, 5.6), (3.3, 3.95),
                             arrowstyle="-|>", mutation_scale=20, lw=2.2, color=C_PF))
ax.text(3.5, 4.85, "令所有导数 $=0$\n（静态化）", fontsize=10.6, color=C_PF,
        ha="center", va="center")

# 箭头：RMS -> Kuramoto
ax.add_patch(FancyArrowPatch((7.5, 5.6), (9.7, 3.95),
                             arrowstyle="-|>", mutation_scale=20, lw=2.2, color=C_KUR))
ax.text(9.5, 4.85, "恒幅值 + 无损纯感\n（相角化，消去网络）", fontsize=10.6, color=C_KUR,
        ha="center", va="center")

ax.text(6.5, 1.25,
        "PF 与 Kuramoto 是 RMS 的两个并列简化：PF 丢掉时间维度；Kuramoto 保留时间、只留相角",
        ha="center", fontsize=11.6, color="#2c3e50")
ax.text(6.5, 0.55,
        "（因此 Kuramoto 不是“潮流的进一步简化”，它比 PF 多保留了转子摇摆动态）",
        ha="center", fontsize=11.0, color=C_KUR)

save(fig, "fig13_model_chain")
