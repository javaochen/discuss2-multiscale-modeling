"""fig04: 相量(准稳态)解 vs 含暂态的 EMT 精确解 —— RL 合闸。

电路: L di/dt + R i = Vm cos(wt+phi), i(0)=0。
精确解 (EMT):  i(t) = (Vm/|Z|)[cos(wt+phi-phi_z) - cos(phi-phi_z) e^{-t/tau}]
相量解 (RMS/PF 准稳态):  i_ph(t) = (Vm/|Z|) cos(wt+phi-phi_z)
其中 |Z|=sqrt(R^2+(wL)^2), phi_z=atan(wL/R), tau=L/R。
差值严格等于 -(Vm/|Z|)cos(phi-phi_z)e^{-t/tau}, 即"相量法忽略的暂态"。
"""
import numpy as np

from common import C_EMT, C_GREY, C_KUR, C_PF, C_RMS, plt, save

f, w = 50.0, 2 * np.pi * 50.0
Vm, R, L = 1.0, 1.0, 0.02
Z = np.hypot(R, w * L)
phiz = np.arctan2(w * L, R)
tau = L / R
print(f"|Z|={Z:.4f} ohm, phi_z={np.degrees(phiz):.2f} deg, tau={tau*1e3:.1f} ms, Q=wL/R={w*L/R:.2f}")

t = np.linspace(0, 0.12, 20000)
v = Vm * np.cos(w * t)


def i_exact(phi):
    return (Vm / Z) * (np.cos(w * t + phi - phiz) - np.cos(phi - phiz) * np.exp(-t / tau))


def i_ph(phi):
    return (Vm / Z) * np.cos(w * t + phi - phiz)


fig, axs = plt.subplots(1, 2, figsize=(11.0, 4.0))

ax = axs[0]
phi = phiz  # 最坏合闸角
ax.plot(t * 1e3, v, color="#95a5a6", lw=1.0, label="$v(t)/V_m$")
ax.plot(t * 1e3, i_exact(phi) * Z / Vm, color=C_EMT, lw=1.6, label="EMT 精确解 (含暂态)")
ax.plot(t * 1e3, i_ph(phi) * Z / Vm, color=C_RMS, lw=1.6, ls="--", label="相量解 (稳态)")
ax.axhline(1, color=C_GREY, lw=0.8, ls=":")
ax.axhline(-1, color=C_GREY, lw=0.8, ls=":")
ax.annotate("", xy=(tau * 1e3, -1.05), xytext=(0, -1.05),
            arrowprops=dict(arrowstyle="<->", color=C_KUR, lw=1.1))
ax.text(tau * 1e3 / 2, -1.35, r"$\tau=L/R$", color=C_KUR, ha="center", fontsize=9)
ax.set_ylim(-1.7, 1.6)
ax.set_title("(a) 最坏合闸相角 $\\phi=\\phi_z$: 相量法缺失的暂态与稳态同量级")
ax.set_xlabel("时间 / ms"); ax.set_ylabel("归一化电流  $i\\,|Z|/V_m$")
ax.legend(loc="upper right", fontsize=8, frameon=False)

ax = axs[1]
for phi_d, c in [(phiz, C_EMT), (0.0, C_RMS), (np.pi / 2 - phiz, C_PF)]:
    err = np.abs(i_exact(phi_d) - i_ph(phi_d)) * Z / Vm
    ax.semilogy(t * 1e3, np.maximum(err, 1e-12), color=c, lw=1.6,
                label=f"$\\phi={np.degrees(phi_d):.0f}^\\circ$")
ax.semilogy(t * 1e3, np.exp(-t / tau), color="k", lw=1.0, ls=":",
            label=r"$e^{-t/\tau}$ (理论上界)")
ax.set_ylim(1e-3, 2.0)
ax.set_title("(b) 误差严格按 $e^{-t/\\tau}$ 衰减, $\\tau=L/R$")
ax.set_xlabel("时间 / ms"); ax.set_ylabel("$|i_{EMT}-i_{ph}|\\,|Z|/V_m$")
ax.legend(loc="lower left", fontsize=8, frameon=False)

save(fig, "fig04_phasor_vs_waveform")
