"""公共绘图与数据保存工具。

所有图脚本统一 import 本模块, 保证:
  * 中文字体正确 (Noto Sans CJK SC)
  * 统一的配色、线宽、字号
  * 图同时输出 pdf (供 LaTeX 引用) 与 png (供 md 内嵌)
  * 关键数值数据保存为 npz, 便于复现与引用

用法:
    from common import plt, np, save, save_data, FIGDIR
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parent.parent
FIGDIR = ROOT / "figures"
DATADIR = ROOT / "data"
FIGDIR.mkdir(exist_ok=True)
DATADIR.mkdir(exist_ok=True)

plt.rcParams.update(
    {
        "font.sans-serif": ["Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans"],
        "font.family": "sans-serif",
        "axes.unicode_minus": False,
        "font.size": 12,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "legend.fontsize": 10.5,
        "xtick.labelsize": 10.5,
        "ytick.labelsize": 10.5,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.5,
        "axes.axisbelow": True,
        "figure.dpi": 110,
        "savefig.bbox": "tight",
        "mathtext.fontset": "dejavusans",
        "lines.linewidth": 1.6,
    }
)

# 三类模型统一配色
C_EMT = "#c0392b"   # 红: EMT
C_RMS = "#2471a3"   # 蓝: RMS
C_PF = "#1e8449"    # 绿: 潮流/准稳态
C_KUR = "#8e44ad"   # 紫: Kuramoto
C_GREY = "#7f8c8d"
C_ORANGE = "#d35400"

MODEL_COLORS = {"EMT": C_EMT, "RMS": C_RMS, "PF/QSTS": C_PF}


def save(fig, name, dpi=200):
    """保存 fig 为 figures/<name>.pdf 与 .png, 并打印信息。"""
    pdf = FIGDIR / f"{name}.pdf"
    png = FIGDIR / f"{name}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=dpi)
    plt.close(fig)
    print(f"[saved] {pdf.name}  ({pdf.stat().st_size/1024:.1f} KB)")
    return pdf, png


def save_data(name, **arrays):
    """保存关键数值数据到 data/<name>.npz。"""
    path = DATADIR / f"{name}.npz"
    np.savez(path, **arrays)
    print(f"[data ] {path.name}")
    return path


def band(ax, y, x0, x1, color, label=None, height=0.62, alpha=0.85, text=None):
    """在对数 x 轴 ax 上画一条横向区间带。"""
    ax.add_patch(
        Rectangle((x0, y - height / 2), x1 - x0, height,
                  facecolor=color, edgecolor="none", alpha=alpha, zorder=2,
                  label=label)
    )
    if text:
        ax.text(np.sqrt(x0 * x1), y, text, ha="center", va="center",
                color="white", fontsize=9, zorder=3, fontweight="bold")
