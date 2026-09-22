"""fig06: 奇异摄动 / 慢流形 —— 为什么快变量可以被代数约束替代。

两时间尺度系统 (Tikhonov 标准型):
    dx/dt = f(x,z) = -x + z
    eps dz/dt = g(x,z) = tanh(x) - z
令 eps -> 0 得代数约束 z = tanh(x) (慢流形), 代入得降阶慢系统
    dx/dt = -x + tanh(x)
本图数值展示: 轨迹先沿快方向 (~eps) 落到慢流形, 再沿流形慢演化;
边界层时间与 eps 成正比 (log-log 斜率 1), 即"忽略快动态"的误差可控。
这正是 EMT (完整) -> RMS (降阶) 的数学骨架。
"""
import numpy as np
from scipy.integrate import solve_ivp

from common import C_EMT, C_GREY, C_KUR, C_PF, C_RMS, plt, save, save_data


def rhs(t, y, eps):
    x, z = y
    return [-x + z, (np.tanh(x) - z) / eps]


def fast_time(x0, z0, eps):
    """估计边界层时间: x 首次进入慢流形邻域的时间。"""
    sol = solve_ivp(rhs, [0, 20], [x0, z0], args=(eps,), method="LSODA",
                    rtol=1e-8, atol=1e-10, dense_output=True, max_step=0.5)
    tt = np.linspace(0, sol.t[-1], 4000)
    xx, zz = sol.sol(tt)
    idx = np.where(np.abs(zz - np.tanh(xx)) < 0.02)[0]
    return tt[idx[0]] if len(idx) else np.nan


fig, axs = plt.subplots(1, 3, figsize=(12.6, 4.0), layout="constrained")

# (a) 相平面
ax = axs[0]
xg = np.linspace(-2.5, 2.5, 400)
ax.plot(xg, np.tanh(xg), color="k", lw=1.6, ls="--", alpha=0.75, zorder=1,
        label="慢流形 $z=\\tanh x$")
for eps, c in zip([0.5, 0.1, 0.01], [C_PF, C_RMS, C_EMT]):
    sol = solve_ivp(rhs, [0, 20], [2.0, -1.5], args=(eps,), method="Radau",
                    rtol=1e-8, atol=1e-10, t_eval=np.linspace(0, 20, 1500))
    assert sol.success, f"积分失败 eps={eps}"
    xx, zz = sol.y
    ax.plot(xx, zz, color=c, lw=1.8, zorder=3, label=f"$\\varepsilon={eps}$")
    ax.plot(xx[0], zz[0], "o", color=c, ms=4, zorder=4)
    ax.plot(xx[-1], zz[-1], "s", color=c, ms=4, zorder=4)
ax.set_xlabel("慢变量 $x$"); ax.set_ylabel("快变量 $z$")
ax.set_title("(a) 相平面: 先到慢流形, 再沿岸演化")
ax.legend(fontsize=8, frameon=False)

# (b) 时间序列
ax = axs[1]
eps = 0.05
sol = solve_ivp(rhs, [0, 8], [2.0, -1.5], args=(eps,), method="LSODA",
                rtol=1e-9, atol=1e-11, dense_output=True, max_step=0.2)
tt = np.linspace(0, 8, 4000)
xx, zz = sol.sol(tt)
ax.plot(tt, xx, color=C_RMS, lw=1.8, label="$x(t)$ 慢变量")
ax.plot(tt, zz, color=C_EMT, lw=1.5, label="$z(t)$ 快变量")
ax.plot(tt, np.tanh(sol.sol(tt)[0]), color="k", lw=1.0, ls=":",
        label="$z=\\tanh x$ (代数约束)")
ax.axvspan(0, fast_time(2.0, -1.5, eps), color="#ecf0f1", zorder=0)
ax.text(fast_time(2.0, -1.5, eps) * 1.1, -1.0, "边界层 $O(\\varepsilon)$", fontsize=8.5,
        color="#7f8c8d")
ax.set_xlabel("时间 $t$"); ax.set_ylabel("状态")
ax.set_title(f"(b) 快动态只在 $O(\\varepsilon)$ 边界层内, $\\varepsilon={eps}$")
ax.legend(fontsize=8, frameon=False)

# (c) 边界层时间 vs eps
ax = axs[2]
epss = np.array([0.2, 0.1, 0.05, 0.02, 0.01])
tb = np.array([fast_time(2.0, -1.5, e) for e in epss])
ax.loglog(epss, tb, "o-", color=C_KUR, lw=1.6, ms=5, label="数值边界层时间 $t_b$")
ax.loglog(epss, tb[0] * epss / epss[0], "k--", lw=1.0, label="斜率 1 参考线")
ax.set_xlabel("奇异摄动参数 $\\varepsilon$")
ax.set_ylabel("边界层时间 $t_b$")
ax.set_title("(c) 快动态时间 $\\propto\\varepsilon$: $\\varepsilon\\to 0$ 即降阶")
ax.legend(fontsize=8.5, frameon=False)

save_data("fig06_singular_perturbation", eps=epss, t_b=tb)
save(fig, "fig06_singular_perturbation")
