"""fig11: Kuramoto 模型的同步相变与临界耦合。

全连接 Kuramoto 模型可用平均场形式精确积分 (O(N) 每步):
    r e^{j psi} = (1/N) sum_i e^{j theta_i}
    d theta_i/dt = omega_i + K r sin(psi - theta_i)
自然频率取 Lorentzian 分布 g(omega)=gamma/(pi(omega^2+gamma^2)), 其解析临界耦合
    K_c = 2 / (pi g(0)) = 2 gamma.
本图给出 r(K) 的相变, 以及 K<Kc / K>Kc 两种动力学。
"""
import numpy as np

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save, save_data

rng = np.random.default_rng(7)
N, gamma = 400, 1.0
u = rng.uniform(0.02, 0.98, N)
omega = gamma * np.tan(np.pi * (u - 0.5))       # Lorentzian
omega = omega[np.abs(omega) < 60]


def order(theta):
    z = np.mean(np.exp(1j * theta))
    return np.abs(z), np.angle(z)


def integrate(K, T=30.0, dt=0.02, seed=1):
    r = np.random.default_rng(seed)
    th = r.uniform(0, 2 * np.pi, len(omega))
    n = int(T / dt)
    hist = np.zeros((n, len(omega))); tt = np.arange(n) * dt
    for k in range(n):
        f = lambda th_: omega + K * order(th_)[0] * np.sin(order(th_)[1] - th_)
        k1 = f(th); k2 = f(th + 0.5 * dt * k1); k3 = f(th + 0.5 * dt * k2); k4 = f(th + dt * k3)
        th = th + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        hist[k] = th
    return tt, hist


Ks = np.linspace(0.0, 4.0, 33)
r_ss = []
for K in Ks:
    tt, hist = integrate(K)
    m = int(0.8 * len(tt))
    r_ss.append(np.mean([order(h)[0] for h in hist[m:]]))
r_ss = np.array(r_ss)

fig, axs = plt.subplots(1, 3, figsize=(13.0, 4.1), layout="constrained")

ax = axs[0]
ax.plot(Ks, r_ss, "o-", color=C_KUR, lw=1.8, ms=5, label="数值 $r(K)$")
ax.axvline(2 * gamma, color=C_EMT, ls="--", lw=1.4)
ax.text(2 * gamma + 0.06, 0.15, "理论 $K_c=2\\gamma=2$", color=C_EMT, fontsize=9)
ax.set_xlabel("耦合强度 $K$"); ax.set_ylabel("序参量 $r$")
ax.set_title("(a) 同步相变: $r>0$ 仅当 $K>K_c$")
ax.legend(fontsize=9, frameon=False)

ax = axs[1]
for K, c in [(1.5, C_RMS), (3.0, C_EMT)]:
    tt, hist = integrate(K)
    r_t = np.array([order(h)[0] for h in hist])
    ax.plot(tt, r_t, color=c, lw=1.8, label=f"$K={K}$")
ax.axhline(0, color="k", lw=0.6)
ax.set_xlabel("时间 / s"); ax.set_ylabel("序参量 $r(t)$")
ax.set_title("(b) $K<K_c$ 趋向无序, $K>K_c$ 同步")
ax.legend(fontsize=9, frameon=False)

ax = axs[2]
for K, c in [(1.0, C_RMS), (4.0, C_EMT)]:
    tt, hist = integrate(K, T=40.0)
    m = int(0.9 * len(tt))
    dw = np.array([(np.unwrap(hist[m:, i])[-1] - np.unwrap(hist[m:, i])[0]) /
                   (tt[-1] - tt[m]) for i in range(len(omega))])
    ax.plot(omega, dw, "o", color=c, ms=3.5, alpha=0.8, label=f"$K={K}$")
ax.plot(omega, omega, "k--", lw=0.9, label="未耦合 $\\dot\\theta=\\omega$")
ax.set_xlabel("自然频率 $\\omega_i$"); ax.set_ylabel("平均频率 $\\langle\\dot\\theta_i\\rangle$")
ax.set_title("(c) $K>K_c$ 时中心振子频率被锁定")
ax.legend(fontsize=9, frameon=False)

save_data("fig11_kuramoto_transition", Ks=Ks, r_ss=r_ss, gamma=gamma, Kc=2 * gamma)
save(fig, "fig11_kuramoto_transition")
