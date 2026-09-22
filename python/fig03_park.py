"""fig03: Park 变换 (abc -> dq0) 的数值验证。

说明 EMT 的 abc 瞬时量如何变成 RMS 使用的 dq / 相量量, 以及
"平衡正序 -> 直流" 这一相量假设成立的边界:
  * 平衡正序 -> dq 为直流 (相量法的前提)
  * 三相不平衡 (含负序) -> dq 出现 2w 纹波 (相量法失效)
  * 幅值慢变 -> dq 出现慢变包络 (QSTS / 准稳态的用武之地)
"""
import numpy as np

from common import C_EMT, C_KUR, C_PF, C_RMS, plt, save

f, w = 50.0, 2 * np.pi * 50.0
fs = 20000.0
t = np.arange(0, 0.06, 1 / fs)

# 三相平衡正序
va_p = np.cos(w * t)
vb_p = np.cos(w * t - 2 * np.pi / 3)
vc_p = np.cos(w * t + 2 * np.pi / 3)
# 叠加负序 (不平衡)
e = 0.3
va_u = va_p + e * np.cos(w * t)
vb_u = vb_p + e * np.cos(w * t + 2 * np.pi / 3)
vc_u = vc_p + e * np.cos(w * t - 2 * np.pi / 3)
# 幅值慢变 (5 Hz 调制), 平衡正序
A = 1.0 + 0.4 * np.sin(2 * np.pi * 5.0 * t)
va_m, vb_m, vc_m = A * va_p, A * vb_p, A * vc_p


def park(a, b, c, th):
    d = (2 / 3) * (a * np.cos(th) + b * np.cos(th - 2 * np.pi / 3) + c * np.cos(th + 2 * np.pi / 3))
    q = -(2 / 3) * (a * np.sin(th) + b * np.sin(th - 2 * np.pi / 3) + c * np.sin(th + 2 * np.pi / 3))
    return d, q


def clarke(a, b, c):
    al = (2 / 3) * (a - 0.5 * b - 0.5 * c)
    be = (2 / 3) * (np.sqrt(3) / 2) * (b - c)
    return al, be


th = w * t  # 同步旋转角
d_p, q_p = park(va_p, vb_p, vc_p, th)
d_u, q_u = park(va_u, vb_u, vc_u, th)
d_m, q_m = park(va_m, vb_m, vc_m, th)
al_p, be_p = clarke(va_p, vb_p, vc_p)
al_u, be_u = clarke(va_u, vb_u, vc_u)

fig, axs = plt.subplots(2, 2, figsize=(10.5, 6.8), layout="constrained")

ax = axs[0, 0]
for sig, lbl, c in [(va_p, "$v_a$", C_EMT), (vb_p, "$v_b$", C_RMS), (vc_p, "$v_c$", C_PF)]:
    ax.plot(t * 1e3, sig, color=c, lw=1.3, label=lbl)
ax.set_title("(a) EMT 侧: 三相瞬时电压 $v_{abc}(t)$")
ax.set_xlabel("时间 / ms"); ax.set_ylabel("电压 / pu")
ax.legend(ncol=3, loc="upper right", frameon=False)

ax = axs[0, 1]
ax.plot(t * 1e3, d_p, color=C_EMT, lw=1.6, label="$v_d$ (平衡正序)")
ax.plot(t * 1e3, q_p, color=C_RMS, lw=1.6, label="$v_q$ (平衡正序)")
ax.plot(t * 1e3, d_u, color=C_EMT, lw=1.0, ls="--", alpha=0.8, label="$v_d$ (含负序不平衡)")
ax.plot(t * 1e3, q_u, color=C_RMS, lw=1.0, ls="--", alpha=0.8, label="$v_q$ (含负序不平衡)")
ax.set_title("(b) RMS 侧: dq 分量 —— 平衡正序时为直流, 不平衡时出现 $2\\omega$ 纹波")
ax.set_xlabel("时间 / ms"); ax.set_ylabel("电压 / pu")
ax.set_ylim(-0.6, 1.6); ax.legend(fontsize=7.5, loc="upper right", ncol=2, frameon=False)
ax.annotate("$2\\omega$ 纹波 = 相量法失效区", xy=(0.045, d_u[t > 0.044][20]),
            xytext=(0.020, -0.45), fontsize=8, color="#922b21",
            arrowprops=dict(arrowstyle="->", color="#922b21", lw=0.9))

ax = axs[1, 0]
ax.plot(al_p, be_p, color=C_RMS, lw=1.8, label="平衡正序 (圆)")
ax.plot(al_u, be_u, color=C_EMT, lw=1.2, ls="--", label="含负序 (椭圆)")
ax.plot([0, 1.3], [0, 0], color=C_KUR, lw=1.0)
ax.plot([0, 0], [0, 1.3], color=C_KUR, lw=1.0)
ax.text(1.33, 0, "$\\alpha$", color=C_KUR); ax.text(0, 1.33, "$\\beta$", color=C_KUR)
ax.plot([0, np.cos(0.9)], [0, np.sin(0.9)], color="k", lw=1.0)
ax.text(0.55, 0.62, "$\\theta=\\omega t$", fontsize=8)
ax.set_aspect("equal")
ax.set_title("(c) $\\alpha\\beta$ 轨迹: 旋转矢量在 dq 系中成为常矢量")
ax.set_xlabel("$\\alpha$ / pu"); ax.set_ylabel("$\\beta$ / pu")
ax.legend(fontsize=8, loc="lower right", frameon=False); ax.set_xlim(-1.5, 1.6); ax.set_ylim(-1.5, 1.6)

ax = axs[1, 1]
ax.plot(t * 1e3, va_m, color=C_PF, lw=1.0, alpha=0.6, label="$v_a$ (幅值 5 Hz 调制)")
ax.plot(t * 1e3, d_m, color=C_EMT, lw=1.8, label="$v_d$ (慢变包络)")
ax.plot(t * 1e3, A, color=C_KUR, lw=1.2, ls=":", label="$A(t)=1+0.4\\sin(2\\pi 5t)$")
ax.set_title("(d) 幅值慢变: dq 变成慢变量 —— QSTS/准稳态的适用区")
ax.set_xlabel("时间 / ms"); ax.set_ylabel("电压 / pu")
ax.legend(fontsize=8, loc="upper right", frameon=False)

save(fig, "fig03_park_transform")
