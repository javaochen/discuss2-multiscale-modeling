"""fig05: 准稳态(相量)近似的误差判据 —— 误差 ~ (包络带宽/载波频率)。

设 v(t)=A(t)cos(wt), A(t)=1+m sin(Wt)。
线性系统 H(w)=1/(R+jwL) 的精确稳态解含 w, w+W, w-W 三个频率分量;
相量法只保留 w 分量并把 A(t) 当作瞬时幅值。对 W/w 做一阶展开给出

    eps / |I_w|  =  m * (W/w) * (wL/|Z|)  =  m*(W/w)*sin(phi_z)

(推导: 边带幅值 |H(w±W)| 与相位各展开到 O(W), 两式相减后得到
 cos(Wt)*[a sin(...) + c cos(...)], 其幅度为 m*|H|*(W/w)*sin(phi_z);
 注意系数是 m 而不是 m/2 —— 早期草稿的 m/2 已废弃。)
即相量法成立的尺度: 包络带宽 W << 载波频率 w (在 wL/R 不小时)。
本图用解析精确解数值验证该斜率与量级。数值自检 (与 data/*.npz 对照):
  Omega/w <= 0.25 时 num/theory = 1.000--1.040 (偏差 <5%);
  Omega/w -> 1 时边带触及 DC 与 2w, 一阶展开失效, 右端偏离属预期。
"""
import numpy as np

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save, save_data

f, w = 50.0, 2 * np.pi * 50.0
m = 0.30
ratios = np.logspace(np.log10(0.02), np.log10(1.0), 15)
qs = [0.2, 1.0, 5.0]
colors = [C_PF, C_RMS, C_EMT]

rel_err = np.zeros((len(qs), len(ratios)))
for iq, q in enumerate(qs):
    R = 1.0
    L = q * R / w
    for ir, ratio in enumerate(ratios):
        W = ratio * w
        tmax = max(5 * 2 * np.pi / W, 0.4)
        t = np.linspace(0, tmax, int(tmax * 8000) + 1)

        def H(wx):
            return 1.0 / (R + 1j * wx * L)

        # 精确稳态 (三个频率分量; 注意 (w-W) 边带来自 sin((W-w)t) 故为负号)
        Hw, Hp, Hm = H(w), H(w + W), H(w - W)
        i_ex = (np.abs(Hw) * np.cos(w * t + np.angle(Hw))
                + (m / 2) * np.abs(Hp) * np.sin((w + W) * t + np.angle(Hp))
                - (m / 2) * np.abs(Hm) * np.sin((w - W) * t + np.angle(Hm)))
        # 相量/准稳态解
        A = 1 + m * np.sin(W * t)
        i_ph = A * np.abs(Hw) * np.cos(w * t + np.angle(Hw))
        rel_err[iq, ir] = np.max(np.abs(i_ex - i_ph)) / np.abs(Hw)

fig, ax = plt.subplots(figsize=(7.2, 5.0))
for iq, (q, c) in enumerate(zip(qs, colors)):
    sin_phi = q / np.hypot(1.0, q)
    theory = m * ratios * sin_phi
    ax.loglog(ratios, rel_err[iq], "o-", color=c, ms=4.5, lw=1.5,
              label=f"数值: $\\omega L/R={q}$")
    ax.loglog(ratios, theory, "--", color=c, lw=1.0, alpha=0.8,
              label=f"理论: $m(\\Omega/\\omega)\\sin\\phi_z, \\ \\sin\\phi_z={sin_phi:.2f}$")

ax.axhline(0.01, color=C_KUR, ls=":", lw=1.2)
ax.text(0.022, 0.011, "1% 误差容限", color=C_KUR, fontsize=8.5)
ax.set_xlabel("包络带宽比  $\\Omega/\\omega$   (包络频率 / 载波频率)")
ax.set_ylabel("最大相对误差  $\\max|i_{exact}-i_{ph}|/|I_\\omega|$")
ax.set_title("准稳态(相量)法的误差判据: 误差 ∝ 包络带宽 / 载波频率\n"
             f"($m={m}$, $\\omega=2\\pi\\cdot 50$ rad/s, 解析精确解验证)")
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8, loc="upper left", frameon=False)
save_data("fig05_quasistatic_error", ratios=ratios, qs=np.array(qs), rel_err=rel_err, m=m)
save(fig, "fig05_quasistatic_error")
