"""fig07: 线性化系统的特征值谱 —— 多尺度的"刚度比"从哪来。

算例: 无穷大母线(节点1) - RL 线路1 - 节点2(C2) - RL 线路2 - 节点3(C3, 负荷)
      节点3 接入一台同步机(2 阶经典模型, 经暂态电抗 X'd)。
在同步旋转 dq 坐标系中写 10 阶状态方程, 先数值求平衡点, 再数值线性化求特征值。

结果: 特征值分成两团
  * 电磁团  ~ 1/(sqrt(L C)) 量级 (网络/电缆/滤波器), 极快;
  * 机电团  ~ D/M 量级 (转子摇摆), 很慢。
两者之比即刚度比, 决定了"直接积分完整 EMT 需要极小步长、却要仿真很长时间"。
"""
import numpy as np
from scipy.optimize import fsolve

from common import C_EMT, C_GREY, C_KUR, C_RMS, plt, save, save_data

w = 1.0
R1, L1 = 0.02, 0.08
R2, L2 = 0.03, 0.10
C2, C3 = 1e-4, 1e-4
GL = 0.3
Efd, Xdp = 1.10, 0.30
M, D = 6.0, 1.5
v1d, v1q = 1.0, 0.0


def machine_current(delta, v3d, v3q):
    ed, eq = Efd * np.cos(delta), Efd * np.sin(delta)
    return (eq - v3q) / Xdp, -(ed - v3d) / Xdp


def deriv(x, Pm):
    i1d, i1q, v2d, v2q, i2d, i2q, v3d, v3q, delta, dw = x
    igd, igq = machine_current(delta, v3d, v3q)
    return np.array([
        (v1d - v2d - R1 * i1d + w * L1 * i1q) / L1,
        (v1q - v2q - R1 * i1q - w * L1 * i1d) / L1,
        (i1d - i2d + w * C2 * v2q) / C2,
        (i1q - i2q - w * C2 * v2d) / C2,
        (v2d - v3d - R2 * i2d + w * L2 * i2q) / L2,
        (v2q - v3q - R2 * i2q - w * L2 * i2d) / L2,
        (i2d - GL * v3d + igd + w * C3 * v3q) / C3,
        (i2q - GL * v3q + igq - w * C3 * v3d) / C3,
        dw,
        (Pm - (v3d * igd + v3q * igq) - D * dw) / M,
    ])


# ---- 平衡点: 设 delta0, 解网络 8 个代数方程 ----
delta0 = 0.30
guess = np.array([0.8, -0.2, 0.99, -0.05, 0.7, -0.2, 0.97, -0.15])


def net_eqs(y):
    x = np.array([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], delta0, 0.0])
    d = deriv(x, 0.0)
    return d[:8]


sol = fsolve(net_eqs, guess, xtol=1e-12, full_output=True)
y = sol[0]
x0 = np.array([y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], delta0, 0.0])
igd, igq = machine_current(delta0, x0[6], x0[7])
Pe0 = x0[6] * igd + x0[7] * igq
Pm = Pe0
print("平衡点收敛:", sol[2], " Pm=Pe0=%.4f" % Pe0)
print("v2=%.4f%+.4fj  v3=%.4f%+.4fj" % (x0[2], x0[3], x0[6], x0[7]))
d0 = deriv(x0, Pm)
print("平衡点残差 max=%.2e" % np.max(np.abs(d0)))

# ---- 数值 Jacobian ----
n = len(x0)
J = np.zeros((n, n))
h = 1e-7
for j in range(n):
    xp, xm = x0.copy(), x0.copy()
    xp[j] += h
    xm[j] -= h
    J[:, j] = (deriv(xp, Pm) - deriv(xm, Pm)) / (2 * h)

lam = np.linalg.eigvals(J)
lam = lam[np.argsort(-np.abs(lam))]
fast = lam[np.abs(lam) > 100]
slow = lam[np.abs(lam) <= 100]
print("\n特征值 (rad/s):")
for l in lam:
    print(f"  {l.real:+10.4f} {l.imag:+10.4f}j   |lambda|={abs(l):10.4f}")
if len(fast) and len(slow):
    print(f"\n刚度比 |lambda|max/|lambda|min = {np.abs(lam).max()/np.abs(lam).min():.3e}")

fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.4), layout="constrained")

ax = axs[0]
is_fast = np.abs(lam) > 100
ax.scatter(np.maximum(-lam.real[is_fast], 1e-3), np.maximum(np.abs(lam.imag[is_fast]), 1e-3),
           s=70, c=C_EMT, marker="x", linewidths=2, zorder=3, label="电磁模式")
ax.scatter(np.maximum(-lam.real[~is_fast], 1e-3), np.maximum(np.abs(lam.imag[~is_fast]), 1e-3),
           s=70, marker="o", facecolors="none", edgecolors=C_RMS, linewidths=1.8, zorder=3,
           label="机电模式")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("$-\\mathrm{Re}(\\lambda)$ / rad s$^{-1}$  (对数)")
ax.set_ylabel("$|\\mathrm{Im}(\\lambda)|$ / rad s$^{-1}$  (对数)")
ax.set_title("(a) 特征值分布 (双对数): 两团相距 4~5 个数量级")
ax.legend(fontsize=8.5, loc="lower left", frameon=False)
ax.grid(True, which="both", alpha=0.25)

ax = axs[1]
idx = np.arange(1, len(lam) + 1)
ax.semilogy(idx, np.abs(lam), "o", color=C_KUR, ms=6)
ax.semilogy(idx, np.abs(lam), "-", color=C_KUR, lw=1.0, alpha=0.5)
ax.axhspan(1e2, 1e6, color=C_EMT, alpha=0.10)
ax.axhspan(1e-2, 1e2, color=C_RMS, alpha=0.10)
ax.text(1.2, 3e3, "电磁暂态模式\n(需要 $\\mu$s–ms 步长)", color=C_EMT, fontsize=8.5)
ax.text(1.2, 0.06, "机电模式\n(时间常数 0.1–10 s)", color=C_RMS, fontsize=8.5)
ax.set_xlabel("特征值编号 (按 $|\\lambda|$ 降序)")
ax.set_ylabel("$|\\lambda|$ / rad s$^{-1}$")
ax.set_title(f"(b) 刚度比 $\\approx${np.abs(lam).max()/np.abs(lam).min():.1e}: 快慢模式相差 "
             f"{np.log10(np.abs(lam).max()/np.abs(lam).min()):.0f} 个数量级")

save_data("fig07_eigen_spectrum", lam_real=lam.real, lam_imag=lam.imag,
          Pm=Pm, x0=x0, params=np.array([R1, L1, R2, L2, C2, C3, GL, Efd, Xdp, M, D]))
save(fig, "fig07_eigen_spectrum")
