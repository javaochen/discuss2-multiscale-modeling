"""fig09: 混合仿真接口的两个定量限制。

(a) 相量提取的混叠: EMT 侧的开关/谐波纹波被 RMS 侧以大步长采样时会混叠到
    低频, 污染基波相量。信号 v=cos(wt)+0.15cos(1250*2pi t+0.7), 在 RMS 网格上
    做基波最小二乘(等价整周期 DFT), 误差随步长出现台阶, 台阶位置由 Nyquist 决定:
        f_h < f_s/2 = 1/(2*dt_r)  =>  dt_r < 1/(2 f_h) = 0.4 ms.
(b) 接口延迟的代价: 延迟 tau 使接口相角滞后 w*tau, 对 P=(V1V2/X)sin(theta) 的
    相对误差 ≈ (w tau) cot(theta) (小角)。50 Hz 下 tau=5 ms 即 90 度相移, 误差不可接受,
    故混合仿真必须做延迟补偿/接口等值。
"""
import numpy as np

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save, save_data

w, f_h = 2 * np.pi * 50.0, 1250.0
fig, axs = plt.subplots(1, 2, figsize=(11.4, 4.3), layout="constrained")

# ---------- (a) 混叠误差 ----------
ax = axs[0]
dts = np.logspace(np.log10(5e-5), np.log10(5e-3), 120)
err = np.zeros_like(dts)
T = 1 / 50.0
for i, dt in enumerate(dts):
    n = max(int(round(T / dt)), 4)
    tt = np.arange(n) * dt
    v = np.cos(w * tt) + 0.15 * np.cos(f_h * 2 * np.pi * tt + 0.7)
    A = np.column_stack([np.cos(w * tt), np.sin(w * tt), np.ones(n)])
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    V_est = coef[0] + 1j * coef[1]
    err[i] = np.abs(V_est - 1.0)
err = np.maximum(err, 1e-7)

ax.loglog(dts * 1e3, err, "o-", color=C_EMT, ms=3, lw=1.3, label="基波相量提取误差")
ax.axvline(1 / (2 * f_h) * 1e3, color=C_KUR, ls="--", lw=1.3)
ax.text(1 / (2 * f_h) * 1e3 * 1.06, 2e-5,
        "Nyquist 临界\n$\\Delta t_r=1/(2f_h)=0.4$ ms", color=C_KUR, fontsize=8.5)
ax.axvspan(1 / (2 * f_h) * 1e3, 5, color=C_KUR, alpha=0.07)
ax.set_ylim(1e-7, 1.0)
ax.set_xlabel("RMS 侧采样步长 $\\Delta t_r$ / ms")
ax.set_ylabel("$|\\hat{V}-V|$ / pu")
ax.set_title("(a) 谐波混叠: EMT 侧 1250 Hz 纹波污染 RMS 基波相量\n"
             "(临界步长之下误差为数值零, 之上跳升)")
ax.legend(fontsize=8.5, frameon=False)


# ---------- (b) 延迟误差 ----------
ax = axs[1]
taus = np.logspace(np.log10(1e-4), np.log10(1.5e-2), 250)
for th_deg, c in zip([20, 30, 45], [C_PF, C_RMS, C_EMT]):
    th = np.radians(th_deg)
    exact = np.abs(np.sin(th - w * taus) - np.sin(th)) / np.sin(th)
    approx = w * taus / np.tan(th)
    ax.loglog(taus * 1e3, exact, color=c, lw=1.8, label=f"$\\theta={th_deg}^\\circ$ 精确")
    ax.loglog(taus * 1e3, approx, color=c, lw=0.9, ls=":", alpha=0.9)
ax.loglog([], [], color="k", lw=0.9, ls=":", label="虚线: $\\omega\\tau\\cot\\theta$")
ax.axvline(5.0, color=C_KUR, ls="--", lw=1.3)
ax.text(5.3, 1e-4, "50 Hz 下 $\\tau=5$ ms\n即 90$^\\circ$ 相移", color=C_KUR, fontsize=8.5)
ax.axhline(0.05, color="#7f8c8d", ls=":", lw=1.0)
ax.text(1.1e-1, 0.06, "5% 功率误差", color="#7f8c8d", fontsize=8.5)
ax.set_ylim(1e-5, 2e1)
ax.set_xlabel("接口延迟 $\\tau$ / ms")
ax.set_ylabel("功率相对误差  $|\\Delta P|/P$")
ax.set_title("(b) 接口延迟导致的功率误差: 小延迟下 $\\approx\\omega\\tau\\cot\\theta$\n"
             "(注: $\\tau=20$ ms 的整周期延迟对单一频率反而无误差)")
ax.legend(fontsize=7.5, frameon=False, ncol=2)

save_data("fig09_interface_error", dts=dts, err=err, taus=taus, w=w, f_h=f_h)
save(fig, "fig09_interface_error")
