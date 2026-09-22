"""fig08: EMT-RMS 混合仿真的接口结构与时步协调。

(a) 接口拓扑与交换变量: EMT 侧送瞬时波形, 经相量提取(滑动 DFT)进入 RMS 侧;
    RMS 侧解出的基频相量经受控源(Norton/Thevenin 等值)回注 EMT 侧。
(b) 多速率时步: 一个 RMS 大步 = N 个 EMT 小步, 接口处需要插值/外推,
    并存在一个交换延迟 (通常半个 RMS 步)。
"""
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

from common import C_EMT, C_GREY, C_KUR, C_PF, C_RMS, plt, save

fig, axs = plt.subplots(2, 1, figsize=(10.2, 6.6), height_ratios=[1.35, 1.0],
                        layout="constrained")

# ---------------- (a) 拓扑 ----------------
ax = axs[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.add_patch(Rectangle((0.25, 0.6), 4.1, 4.5, fc="#fdecea", ec=C_EMT, lw=1.6, zorder=1))
ax.add_patch(Rectangle((5.65, 0.6), 4.1, 4.5, fc="#eaf2f8", ec=C_RMS, lw=1.6, zorder=1))
ax.add_patch(Rectangle((4.70, 0.6), 0.60, 4.5, fc="#f2f3f4", ec="#bdc3c7", lw=1.0, zorder=1))
ax.text(5.0, 5.32, "接口母线 (边界节点)", ha="center", fontsize=12.0, fontweight="bold")
ax.text(2.3, 4.85, "EMT 区域: 详细瞬时模型", ha="center", color=C_EMT, fontsize=13.5, fontweight="bold")
ax.text(2.3, 4.50, r"$\Delta t_e=1\text{–}50\,\mu$s, 含开关/PWM", ha="center", color=C_EMT, fontsize=11.0)
ax.text(7.7, 4.85, "RMS 区域: 相量 / DAE 模型", ha="center", color=C_RMS, fontsize=13.5, fontweight="bold")
ax.text(7.7, 4.50, r"$\Delta t_r=1\text{–}10$ ms, 基频相量", ha="center", color=C_RMS, fontsize=11.0)

for x in [1.15, 2.3, 3.45]:
    ax.add_patch(FancyBboxPatch((x - 0.38, 1.5), 0.76, 1.7, boxstyle="round,pad=0.05",
                                fc="white", ec=C_EMT, lw=1.3, zorder=2))
    ax.text(x, 2.35, "IBR", ha="center", va="center", fontsize=10.5, color=C_EMT)
    ax.plot([x, x], [3.2, 4.0], color=C_EMT, lw=1.0, zorder=2)
ax.plot([1.15, 3.45], [4.0, 4.0], color=C_EMT, lw=1.0, zorder=2)

for x, lbl in [(6.55, "SG"), (7.75, "DER$_A$"), (8.85, "load")]:
    ax.add_patch(FancyBboxPatch((x - 0.48, 1.55), 0.96, 1.6, boxstyle="round,pad=0.05",
                                fc="white", ec=C_RMS, lw=1.3, zorder=2))
    ax.text(x, 2.35, lbl, ha="center", va="center", fontsize=10.5, color=C_RMS)
    ax.plot([x, x], [3.15, 4.0], color=C_RMS, lw=1.0, zorder=2)
ax.plot([6.55, 8.85], [4.0, 4.0], color=C_RMS, lw=1.0, zorder=2)

# 上行: EMT -> RMS
ax.annotate("", xy=(5.55, 3.45), xytext=(4.45, 3.45),
            arrowprops=dict(arrowstyle="-|>", color=C_EMT, lw=2.4), zorder=4)
ax.text(2.3, 3.78, r"$v_{abc}(t),\,i_{abc}(t)$", ha="center", va="center",
        fontsize=12.0, color=C_EMT, zorder=5)
ax.text(7.7, 3.78, r"$V\angle\theta,\ I\angle\theta$", ha="center", va="center",
        fontsize=12.0, color=C_EMT, zorder=5)
ax.text(5.0, 3.98, "滑动 DFT", ha="center", fontsize=10.0, color=C_EMT, zorder=5)

# 下行: RMS -> EMT
ax.annotate("", xy=(4.45, 2.35), xytext=(5.55, 2.35),
            arrowprops=dict(arrowstyle="-|>", color=C_RMS, lw=2.4), zorder=4)
ax.text(7.7, 1.30, r"$V\angle\theta$", ha="center", va="center",
        fontsize=12.0, color=C_RMS, zorder=5)
ax.text(2.3, 1.30, r"$v_{abc}(t)$（受控源）", ha="center", va="center",
        fontsize=12.0, color=C_RMS, zorder=5)
ax.text(5.0, 2.58, "相量合成", ha="center", fontsize=10.0, color=C_RMS, zorder=5)

ax.text(5.0, 0.32, "接口等值电路: Norton / Thevenin;  接口延迟 $\\tau_d$ 与阻尼不足是主要难点",
        ha="center", va="center", fontsize=11.0, color=C_KUR, zorder=5)

# ---------------- (b) 时步协调 ----------------
ax = axs[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 3.6); ax.axis("off")
N = 5
te = np.arange(0, 10.01, 0.5)
tr = np.arange(0, 10.01, 2.5)
ax.vlines(te, 2.55, 3.0, color=C_EMT, lw=1.0)
ax.plot([0, 10], [2.55, 2.55], color=C_EMT, lw=1.2)
ax.text(-0.18, 2.78, "EMT\n$\\Delta t_e$", ha="right", va="center", fontsize=11.0, color=C_EMT)
ax.vlines(tr, 1.05, 1.5, color=C_RMS, lw=2.4)
ax.plot([0, 10], [1.05, 1.05], color=C_RMS, lw=1.2)
ax.text(-0.18, 1.28, "RMS\n$\\Delta t_r$", ha="right", va="center", fontsize=11.0, color=C_RMS)

for t0 in tr[:-1]:
    ax.annotate("", xy=(t0 + 2.5, 2.0), xytext=(t0, 2.0),
                arrowprops=dict(arrowstyle="<->", color=C_GREY, lw=1.0))
    ax.text(t0 + 1.25, 2.08, f"$N={N}$", ha="center", fontsize=10.5, color=C_GREY)

for t0 in tr:
    ax.plot([t0, t0], [1.5, 2.55], color=C_GREY, ls=":", lw=0.9)
    ax.plot(t0, 2.55, "o", color=C_RMS, ms=4, zorder=4)

ax.annotate("", xy=(2.5, 0.60), xytext=(0.0, 0.60),
            arrowprops=dict(arrowstyle="<->", color=C_KUR, lw=1.4))
ax.text(1.25, 0.35, "接口延迟 $\\tau_d\\sim\\Delta t_r/2$", ha="center", fontsize=11.0, color=C_KUR)
ax.text(6.6, 0.60, "接口处需插值 / 外推: 引入延迟与数值误差, 可能使混合仿真失稳",
        ha="center", va="center", fontsize=11.0, color="#2c3e50")

save(fig, "fig08_hybrid_interface")
