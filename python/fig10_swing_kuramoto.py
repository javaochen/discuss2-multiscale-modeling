"""fig10: swing 方程 vs Kuramoto 模型 —— 等价性与失效条件。

三机环形电网 (1-2-3-1), 支路阻抗 R+jX, 电压幅值恒为 V=1。
完整 swing 方程:
    M_i d2(delta_i)/dt2 = Pm_i - Pe_i - D_i d(delta_i)/dt
    Pe_i = V_i^2 G_ii + sum_{j!=i} V_i V_j [ G_ij cos(th_ij) + B_ij sin(th_ij) ]
忽略电导 G (即 R=0, 无损纯感) 后, Pe_i 只剩 sin 项, 系统退化为 Kuramoto:
    M_i d2(delta_i)/dt2 = Pm_i - sum_{j!=i} K_ij sin(delta_i - delta_j) - D_i d(delta_i)/dt
即 "二阶 Kuramoto" = swing 方程。
本图: (a) R=0 时两者轨迹完全重合; (b) R>0 时出现偏差;
      (c) 偏差随 R/X 线性增长, 验证 "Kuramoto 假设 = 无损纯感"。
"""
import numpy as np
from scipy.integrate import solve_ivp

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save, save_data


def branch_admittance(R, X):
    y = 1.0 / (R + 1j * X)      # y = g - j b
    return y.real, -y.imag      # g=R/(R^2+X^2), b=X/(R^2+X^2)


def Pe(delta, g, b, V=1.0, kuramoto=False):
    """三角形网络的有功注入 (G_ii=3g, G_ij=-g, B_ij=b)。"""
    th12, th23, th31 = delta[0] - delta[1], delta[1] - delta[2], delta[2] - delta[0]
    s = np.array([np.sin(th12), np.sin(th23), np.sin(th31)])
    c = np.array([np.cos(th12), np.cos(th23), np.cos(th31)])
    sin_term = np.array([s[0] - s[2], s[1] - s[0], s[2] - s[1]])
    if kuramoto:
        return V**2 * b * sin_term
    cos_term = np.array([c[0] + c[2], c[1] + c[0], c[2] + c[1]])
    return V**2 * (3.0 * g - g * cos_term + b * sin_term)


def simulate(R, X, M=0.5, D=0.05, T=60.0, kuramoto=False):
    g, b = branch_admittance(R, X)
    delta0 = np.array([0.0, 0.25, -0.20])
    Pm = Pe(delta0, g, b, kuramoto=kuramoto)
    y0 = np.concatenate([delta0 + np.array([0.10, -0.05, 0.02]), np.zeros(3)])

    def rhs(t, y):
        d, w = y[:3], y[3:]
        return np.concatenate([w, (Pm - Pe(d, g, b, kuramoto=kuramoto) - D * w) / M])

    sol = solve_ivp(rhs, [0, T], y0, rtol=1e-10, atol=1e-12,
                    t_eval=np.linspace(0, T, 6000), method="RK45")
    assert sol.success
    return sol.t, sol.y[:3], Pm


def rel_dev(d_full, d_kur, frac=0.2):
    """稳态相对角偏差: 先减去各时刻的整体均值 (整体旋转是中性模式), 再取后段最大值。"""
    rf = d_full - d_full.mean(axis=0, keepdims=True)
    rk = d_kur - d_kur.mean(axis=0, keepdims=True)
    n = rf.shape[1]
    sl = slice(int((1 - frac) * n), n)
    return np.max(np.abs(rf[:, sl] - rk[:, sl]))


fig, axs = plt.subplots(1, 3, figsize=(13.0, 4.1), layout="constrained")

# (a) R=0 完全一致
ax = axs[0]
t, d_full, _ = simulate(0.0, 0.5, kuramoto=False)
_, d_kur, _ = simulate(0.0, 0.5, kuramoto=True)
for i, c in enumerate([C_EMT, C_RMS, C_PF]):
    ax.plot(t, d_full[i], color=c, lw=2.0, alpha=0.9)
    ax.plot(t, d_kur[i], color="k", lw=0.9, ls="--")
ax.plot([], [], color="k", lw=2.0, label="完整 swing (含 G,cos)")
ax.plot([], [], color="k", lw=0.9, ls="--", label="Kuramoto (仅 sin)")
ax.set_xlabel("时间 / s"); ax.set_ylabel(r"相角 $\delta_i$ / rad")
ax.set_title("(a) $R=0$ (无损纯感): 两者完全重合")
ax.legend(fontsize=8, frameon=False)

# (b) R>0 出现偏差
ax = axs[1]
t, d_full, _ = simulate(0.2, 0.4)
_, d_kur, _ = simulate(0.2, 0.4, kuramoto=True)
for i, c in enumerate([C_EMT, C_RMS, C_PF]):
    ax.plot(t, d_full[i], color=c, lw=1.9)
    ax.plot(t, d_kur[i], color=c, lw=1.1, ls="--", alpha=0.85)
ax.set_xlabel("时间 / s"); ax.set_ylabel(r"相角 $\delta_i$ / rad")
ax.set_title("(b) $R/X=0.5$: 电阻引起形状偏差与整体漂移")

# (c) 偏差 vs R/X
ax = axs[2]
ratios = np.array([0.0, 0.05, 0.1, 0.2, 0.35, 0.5, 0.75, 1.0])
dev = []
X = 0.4
for r in ratios:
    _, d_full, _ = simulate(r * X, X)
    _, d_kur, _ = simulate(r * X, X, kuramoto=True)
    dev.append(rel_dev(d_full, d_kur))
dev = np.array(dev)
ax.loglog(ratios[1:], dev[1:], "o-", color=C_KUR, lw=1.6, ms=6, label="稳态相对角偏差")
ax.loglog(ratios[1:], dev[1] * ratios[1:] / ratios[1], "k--", lw=1.0, label="斜率 1 参考线")
ax.set_xlabel("$R/X$")
ax.set_ylabel(r"$\max|\Delta\delta^{\,rel}|$ / rad")
ax.set_title("(c) 相对角偏差 $\\propto R/X$: Kuramoto 丢掉的是电导 $G$ 项")
ax.legend(fontsize=8.5, frameon=False)

save_data("fig10_swing_kuramoto", ratios=ratios, dev=dev, X=X)
save(fig, "fig10_swing_vs_kuramoto")
