from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch


OUT_DIR = Path(__file__).resolve().parent
STEM = OUT_DIR / "Fig_MFCC_program_flowchart_BW"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "DengXian", "SimHei", "Arial", "DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.unicode_minus": False,
        "font.size": 8.2,
    }
)

# Pure black-and-white palette for journal printing and photocopying.
INK = "#000000"
BLUE = "#FFFFFF"
BLUE_EDGE = "#000000"
TEAL = "#FFFFFF"
TEAL_EDGE = "#000000"
GOLD = "#FFFFFF"
GOLD_EDGE = "#000000"
NEUTRAL = "#FFFFFF"
NEUTRAL_EDGE = "#000000"
ARROW = "#000000"


def process_box(ax, x, y, w, h, text, fill=NEUTRAL, edge=NEUTRAL_EDGE,
                fontsize=8.2, radius=0.012, lw=1.15):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        facecolor=fill,
        edgecolor=edge,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", color=INK,
            fontsize=fontsize, linespacing=1.28, zorder=4)
    return box


def terminator(ax, x, y, w, h, text):
    return process_box(ax, x, y, w, h, text, fill=BLUE, edge=BLUE_EDGE,
                       fontsize=8.5, radius=h / 2.2, lw=1.25)


def io_box(ax, x, y, w, h, text):
    skew = 0.028
    pts = [
        (x - w / 2 + skew, y - h / 2),
        (x + w / 2, y - h / 2),
        (x + w / 2 - skew, y + h / 2),
        (x - w / 2, y + h / 2),
    ]
    patch = Polygon(pts, closed=True, facecolor=BLUE, edgecolor=BLUE_EDGE,
                    linewidth=1.2, zorder=3)
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", color=INK,
            fontsize=8.2, linespacing=1.25, zorder=4)
    return patch


def decision(ax, x, y, w, h, text):
    pts = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
    patch = Polygon(pts, closed=True, facecolor=GOLD, edgecolor=GOLD_EDGE,
                    linewidth=1.2, zorder=3)
    ax.add_patch(patch)
    ax.text(x, y, text, ha="center", va="center", color=INK,
            fontsize=8.3, zorder=4)
    return patch


def arrow(ax, start, end, connectionstyle="arc3", label=None, label_xy=None):
    a = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=1.1,
        color=ARROW,
        connectionstyle=connectionstyle,
        shrinkA=0,
        shrinkB=0,
        zorder=2,
    )
    ax.add_patch(a)
    if label:
        lx, ly = label_xy if label_xy else ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        ax.text(lx, ly, label, fontsize=7.6, color=INK, ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=0.5), zorder=5)
    return a


fig, ax = plt.subplots(figsize=(6.8, 10.0))
fig.patch.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

x = 0.46
w = 0.54
h = 0.047

# Stage labels provide hierarchy without decorative panel boxes.
for y, label in [(0.948, "参数与初始化"), (0.741, "逐帧 MFCC 计算"), (0.105, "特征输出")]:
    ax.text(0.018, y, label, ha="left", va="center", fontsize=7.5,
            fontweight="bold", color=BLUE_EDGE)
    ax.plot([0.018, 0.155], [y - 0.012, y - 0.012], color=BLUE_EDGE, lw=1.0)

terminator(ax, x, 0.965, 0.25, 0.038, "开始")
io_box(ax, x, 0.900, w, h,
       "输入预处理后的连续声发射波形  $x_{f}[n]$")
process_box(ax, x, 0.825, w, 0.070,
            "设置计算参数\n$f_s=1$ MS/s，$L=256$，$S=128$，$Q=26$，P=（待定）\n$f_{min}=20$ kHz，$f_{max}=300$ kHz",
            fill=TEAL, edge=TEAL_EDGE, fontsize=7.9)
process_box(ax, x, 0.745, w, 0.055,
            "计算总帧数 $M$；初始化 $m=0$\n创建特征矩阵 $\\mathbf{C}\\in\\mathbb{R}^{P\\times M}$",
            fill=TEAL, edge=TEAL_EDGE, fontsize=8.0)
decision(ax, x, 0.670, 0.31, 0.072, "$m<M$ ？")

process_box(ax, x, 0.590, w, h,
            "提取第 $m$ 帧：$x_m[n]=x_f[n+mS]$")
process_box(ax, x, 0.520, w, h,
            "施加汉明窗，获得加窗信号 $x_m^{w}[n]$")
process_box(ax, x, 0.450, w, h,
            "执行 $N_{FFT}=256$ 点 FFT，并计算单边功率谱")
process_box(ax, x, 0.375, w, 0.056,
            "线性频率映射至梅尔尺度\n构建覆盖 20–300 kHz 的 26 个三角滤波器",
            fill=TEAL, edge=TEAL_EDGE, fontsize=8.0)
process_box(ax, x, 0.295, w, 0.056,
            "计算滤波器组能量并进行对数压缩\n$E_m(q)=\\ln[\\sum_k P_m(k)H_q(k)+\\varepsilon]$",
            fill=TEAL, edge=TEAL_EDGE, fontsize=7.9)
process_box(ax, x, 0.215, w, 0.056,
            "执行 DCT-II 并保留 $P$ 个系数\n$\\mathbf{c}(m)=[c_0(m),\\ldots,c_{P-1}(m)]^{T}$",
            fill=TEAL, edge=TEAL_EDGE, fontsize=7.9)
process_box(ax, x, 0.145, w, h,
            "写入 $\\mathbf{C}[:,m]=\\mathbf{c}(m)$；$m\\leftarrow m+1$")
io_box(ax, x, 0.072, w, 0.050,
       "输出逐帧 MFCC 矩阵  $\\mathbf{C}\\in\\mathbb{R}^{P\\times M}$")
terminator(ax, x, 0.020, 0.25, 0.034, "结束")

# Main vertical flow.
vertical_pairs = [
    (0.946, 0.924), (0.876, 0.860), (0.790, 0.773), (0.718, 0.706),
    (0.634, 0.614), (0.566, 0.544), (0.496, 0.474), (0.422, 0.403),
    (0.347, 0.323), (0.267, 0.243), (0.187, 0.169), (0.121, 0.097),
    (0.047, 0.037),
]
# The loop body returns to the decision node; it does not connect directly to output.
vertical_pairs.remove((0.121, 0.097))
for y1, y2 in vertical_pairs:
    arrow(ax, (x, y1), (x, y2))

# Decision labels and loop. Yes continues downward; no exits to output.
ax.text(x + 0.025, 0.628, "是", fontsize=7.6, color=INK, ha="left", va="center")
ax.plot([x + 0.155, 0.895, 0.895, 0.755],
        [0.670, 0.670, 0.072, 0.072], color=ARROW, lw=1.1, zorder=2)
arrow(ax, (0.755, 0.072), (x + w / 2 - 0.010, 0.072))
ax.text(0.64, 0.684, "否", fontsize=7.6, color=INK, ha="center", va="center",
        bbox=dict(facecolor="white", edgecolor="none", pad=0.5), zorder=5)

# Return loop after increment.
ax.plot([x + w / 2, 0.795, 0.795, 0.635],
        [0.145, 0.145, 0.670, 0.670], color=ARROW, lw=1.1, zorder=2)
arrow(ax, (0.635, 0.670), (x + 0.155, 0.670))

fig.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.01)
fig.savefig(STEM.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.08, facecolor="white")
fig.savefig(STEM.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.08, facecolor="white")
fig.savefig(STEM.with_suffix(".png"), dpi=400, bbox_inches="tight", pad_inches=0.08, facecolor="white")
fig.savefig(STEM.with_suffix(".tiff"), dpi=600, bbox_inches="tight", pad_inches=0.08, facecolor="white")
plt.close(fig)

print(f"Saved: {STEM}.svg/.pdf/.png/.tiff")
