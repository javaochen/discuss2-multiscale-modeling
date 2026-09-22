"""fig12: 真实网络拓扑上的 Kuramoto 同步 (IEEE 9 节点系统)。

一阶 Kuramoto on graph:
    d theta_i/dt = omega_i + K * sum_j A_ij sin(theta_j - theta_i)
A 为 IEEE 9 bus 的邻接矩阵 (9 条支路: 1-4,2-7,3-9,4-5,4-9,5-6,6-7,7-8,8-9)。
与 fig11 的全连接情形对比: 稀疏网络需要更大的耦合才能同步, 且同步从网络中心开始。
"""
import networkx as nx
import numpy as np
from scipy.integrate import solve_ivp

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save, save_data

edges = [(0, 3), (1, 6), (2, 8), (3, 4), (3, 8), (4, 5), (5, 6), (6, 7), (7, 8)]
pos = {0: (0.0, 0.0), 1: (2.0, 0.5), 2: (3.0, 1.6), 3: (1.0, 1.0),
       4: (1.0, 2.1), 5: (1.5, 3.0), 6: (2.6, 3.2), 7: (3.3, 2.2), 8: (2.5, 1.2)}
G = nx.Graph(); G.add_edges_from(edges)
A = nx.to_numpy_array(G)
N = 9
omega = np.array([0.5, -0.3, 0.8, -0.6, 0.2, -0.9, 0.4, -0.2, 0.7])


def rhs(t, th, K):
    S = A @ np.sin(th); C = A @ np.cos(th)
    return omega + K * (S * np.cos(th) - C * np.sin(th))


def run(K, T=40.0):
    sol = solve_ivp(rhs, [0, T], np.linspace(0, 2 * np.pi, N, endpoint=False),
                    args=(K,), t_eval=np.linspace(0, T, 2000), rtol=1e-9, atol=1e-11)
    return sol.t, sol.y


def order(th):
    z = np.mean(np.exp(1j * th))
    return np.abs(z), np.angle(z)


fig = plt.figure(figsize=(13.0, 4.2), layout="constrained")
gs = fig.add_gridspec(1, 3)

# (a) 拓扑 + 弱耦合相位着色
ax = fig.add_subplot(gs[0, 0])
t, th = run(0.5)
fin = th[:, -1]
nx.draw_networkx_edges(G, pos, ax=ax, width=1.0, edge_color="#bdc3c7")
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=260,
                       node_color=np.sin(fin), cmap="twilight", vmin=-1, vmax=1)
for i in range(N):
    ax.text(pos[i][0], pos[i][1], str(i + 1), ha="center", va="center", fontsize=7.5)
sm = plt.cm.ScalarMappable(cmap="twilight", norm=plt.Normalize(-1, 1))
fig.colorbar(sm, ax=ax, fraction=0.045, label="$\\sin\\theta_i$")
ax.set_title("(a) IEEE 9 节点: 弱耦合 ($K=0.5$) 下相位分散")
ax.axis("off")

# (b) r(t) 对不同 K
ax = fig.add_subplot(gs[0, 1])
for K, c in [(0.5, C_RMS), (2.0, C_EMT), (8.0, C_KUR)]:
    tt, hh = run(K)
    r_t = np.array([order(hh[:, k])[0] for k in range(hh.shape[1])])
    ax.plot(tt, r_t, color=c, lw=1.6, label=f"$K={K}$")
ax.set_xlabel("时间 / s"); ax.set_ylabel("序参量 $r(t)$")
ax.set_title("(b) 稀疏网络: 耦合越强越易同步")
ax.legend(fontsize=9, frameon=False)

# (c) 相角演化
ax = fig.add_subplot(gs[0, 2])
tt, hh = run(8.0)
for i in range(N):
    ax.plot(tt, np.unwrap(hh[i]) - np.unwrap(hh[i])[0], lw=1.3, alpha=0.85)
ax.set_xlabel("时间 / s"); ax.set_ylabel("$\\theta_i(t)-\\theta_i(0)$ / rad")
ax.set_title("(c) $K=8$: 各节点相角锁定为同一斜率")

save_data("fig12_kuramoto_grid", t=tt, theta=hh, omega=omega, A=A)
save(fig, "fig12_kuramoto_grid")
