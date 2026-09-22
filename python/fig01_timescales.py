"""fig01: 电网物理现象与三类模型的时间尺度谱。

一张图回答: "三类模型各自研究哪个时间尺度, 覆盖哪些物理现象"。
横轴为对数时间尺度 (秒)。上半部分是物理现象区间, 下半部分是
EMT / RMS / PF-QSTS 三类模型的动态分辨率与典型步长。
"""
from common import (C_EMT, C_GREY, C_KUR, C_ORANGE, C_PF, C_RMS, band, plt,
                    save)

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(10.0, 6.6), sharex=True,
    gridspec_kw={"height_ratios": [3.0, 2.0], "hspace": 0.10}
)
XMIN, XMAX = 1e-6, 3e10

# ---------------- 上: 物理现象 ----------------
phenomena = [
    ("电力电子开关暂态 / PWM", 1e-6, 1e-4, C_ORANGE),
    ("线路行波 / 雷电冲击", 1e-6, 1e-3, "#e67e22"),
    ("逆变器内环控制 / PLL", 1e-4, 1e-1, "#f1c40f"),
    ("谐波 / 次同步振荡 (SSO)", 1e-2, 1e1, "#27ae60"),
    ("机电振荡 (0.1–2 Hz)", 1e-1, 1e1, C_RMS),
    ("一次调频 / AGC", 1e1, 1e3, "#2980b9"),
    ("机组组合 / 经济调度", 1e3, 1e5, C_KUR),
    ("输配电扩展规划", 1e7, 1e9, C_GREY),
]
for i, (name, x0, x1, c) in enumerate(phenomena):
    y = len(phenomena) - i
    ax1.plot([x0, x1], [y, y], color=c, lw=7, solid_capstyle="butt", zorder=2)
    ax1.text(x1 * 1.45, y, name, va="center", ha="left", fontsize=10.5, color="#2c3e50")

ax1.set_xlim(XMIN, XMAX)
ax1.set_ylim(0.4, len(phenomena) + 0.7)
ax1.set_yticks([])
ax1.set_title("同一套电网: 不同时间尺度上的物理现象 (研究对象的尺度跨度约 15 个数量级)", pad=6)
ax1.grid(axis="y", visible=False)

# 50 Hz 载波周期: EMT 与 RMS 的分界依据
ax1.axvline(0.02, color="k", ls=":", lw=1.0, zorder=1)
ax2.axvline(0.02, color="k", ls=":", lw=1.0, zorder=1)

# 频段标注 (放在左侧空白区)
ax1.text(2.5e-6, 6.0, "电磁暂态\n$\\mu$s–ms", fontsize=10.5, color=C_EMT,
         ha="left", va="center")
ax1.text(2.5e-6, 4.5, "机电暂态\n0.1–10 s", fontsize=10.5, color=C_RMS,
         ha="left", va="center")
ax1.text(2.5e-6, 2.5, "准稳态 / 规划\nmin–year", fontsize=10.5, color=C_PF,
         ha="left", va="center")

# ---------------- 下: 三类模型 ----------------
models = [
    ("EMT", 1e-6, 1e-2, C_EMT, r"$\Delta t=1\text{–}50\,\mu$s"),
    ("RMS", 1e-1, 1e3, C_RMS, r"$\Delta t=1\text{–}10\,$ms"),
    ("PF / QSTS", 6e1, 3e8, C_PF, r"$\Delta t=1\,$min–1 h"),
]
for i, (name, x0, x1, c, dt) in enumerate(models):
    y = len(models) - i
    band(ax2, y, x0, x1, c, text=name, height=0.55)
    ax2.text(x1 * 1.5, y, dt, va="center", ha="left", fontsize=10.5, color=c)

ax2.set_ylim(0.28, 3.75)
ax2.set_yticks([])
ax2.set_xscale("log")
ax2.set_xlim(XMIN, XMAX)
ax2.set_xlabel("时间尺度 / s  (对数轴)")
ax2.set_title("三类主流模型: 可解析的动态范围与典型积分步长", pad=6)
ax2.grid(axis="y", visible=False)
ax2.text(0.021, 3.68, "50 Hz 载波周期 20 ms: EMT 逐点求解, RMS 只保留其包络",
         fontsize=7.8, color="k", ha="left", va="top")

ticks = [1e-6, 1e-3, 1e0, 1e3, 1e6, 1e9]
ax2.set_xticks(ticks)
ax2.set_xticklabels([r"$1\,\mu$s", "1 ms", "1 s", r"$10^3$ s", r"$10^6$ s", r"$10^9$ s"])

# 各模型动态分辨率的分界
ax2.annotate("", xy=(1e-1, 0.40), xytext=(1e-6, 0.40),
             arrowprops=dict(arrowstyle="<->", color=C_GREY, lw=1.0))
ax2.text(3e-4, 0.55, "只有 EMT 能分辨", fontsize=10.0, color=C_GREY, ha="center")
ax2.annotate("", xy=(6e1, 0.40), xytext=(1e-1, 0.40),
             arrowprops=dict(arrowstyle="<->", color=C_GREY, lw=1.0))
ax2.text(2.5e0, 0.55, "RMS 主力区间", fontsize=10.0, color=C_GREY, ha="center")
ax2.annotate("", xy=(3e8, 0.40), xytext=(6e1, 0.40),
             arrowprops=dict(arrowstyle="<->", color=C_GREY, lw=1.0))
ax2.text(1e5, 0.55, "潮流 / QSTS / 规划", fontsize=10.0, color=C_GREY, ha="center")

save(fig, "fig01_model_timescales")
