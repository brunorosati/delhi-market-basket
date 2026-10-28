"""Figures 1 and 2 of the data note. Run: python figures.py (writes PDF and PNG to figures/)."""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

installed = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ["Arial", "Helvetica", "Liberation Sans"] if f in installed), "DejaVu Sans")

plt.rcParams.update({
    "font.family": FONT, "font.size": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#8A8A8A", "axes.linewidth": 0.6,
    "xtick.color": "#4D4D4D", "ytick.color": "#4D4D4D", "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "text.color": "#222222", "axes.labelcolor": "#222222", "pdf.fonttype": 42, "savefig.dpi": 300})
BRAND, RIVAL, LINE = "#B6522C", "#A9A9A9", "#555555"
thousands = FuncFormatter(lambda v, _: f"{v:,.0f}")

df = pd.read_csv("data/market_data.csv")
vk = df[df.event == "Vasant Kunj"].copy()
vk["rpc"] = vk.revenue_inr / vk.customers
rivals = vk[vk.brand != "Montrega"]
median_rpc = rivals.rpc.median()

# Figure 1: revenue per customer by brand
d = vk.sort_values("rpc")
fig, ax = plt.subplots(figsize=(6.3, 3.8))
colors = [BRAND if b == "Montrega" else RIVAL for b in d.brand]
ax.barh(d.brand, d.rpc, color=colors, height=0.68, zorder=2)
for y, (b, v) in enumerate(zip(d.brand, d.rpc)):
    ax.text(v + 60, y, f"{v:,.0f}", va="center", fontsize=7.3, color="#333333", zorder=4,
            bbox=dict(boxstyle="square,pad=0.08", fc="white", ec="none"))
ax.axvline(median_rpc, color=LINE, lw=0.8, ls=(0, (3, 2)), zorder=3)
ax.text(median_rpc + 70, 1.0, f"Median of the other 26 brands: {median_rpc:,.0f}", fontsize=7.6, color=LINE, va="center")
ax.set_xlim(0, 7300)
ax.xaxis.set_major_formatter(thousands)
ax.set_xlabel("Revenue per unique customer (INR)")
ax.tick_params(axis="y", length=0, labelsize=7.6)
ax.spines["left"].set_visible(False)
for lab in ax.get_yticklabels():
    if lab.get_text() == "Montrega":
        lab.set_fontweight("bold")
ax.set_ylim(-0.6, len(d) - 0.4)
fig.tight_layout(pad=0.3)
for ext in ("pdf", "png"):
    fig.savefig(f"figures/figure1.{ext}")
plt.close(fig)

# Figure 2: revenue against customers, log scales, with lines of constant revenue per customer
fig, ax = plt.subplots(figsize=(6.3, 3.45))
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(2.3, 75); ax.set_ylim(3000, 200000)
xs = np.array([2.3, 75])
m = vk[vk.brand == "Montrega"].iloc[0]
ax.plot(xs, median_rpc * xs, color=LINE, lw=0.8, ls=(0, (3, 2)), zorder=1)
ax.plot(xs, m.rpc * xs, color=BRAND, lw=0.8, ls=(0, (1, 1.6)), zorder=1)
ax.scatter(rivals.customers, rivals.revenue_inr, s=20, color=RIVAL, edgecolor="white", linewidth=0.5, zorder=3)
ax.scatter([m.customers], [m.revenue_inr], s=42, color=BRAND, edgecolor="white", linewidth=0.6, zorder=4)
ax.annotate("Montrega\n16 customers, INR 106,450", (m.customers, m.revenue_inr), xytext=(10, -4),
            textcoords="offset points", fontsize=7.6, color=BRAND, fontweight="bold", va="top")
for name, dx, dy, ha in [("Root club", 6, 4, "left"), ("Root Rahasya", 6, -2, "left"), ("Clasp", 6, -6, "left"), ("Bombaloca", 6, -6, "left")]:
    r = vk[vk.brand == name].iloc[0]
    ax.annotate(name, (r.customers, r.revenue_inr), xytext=(dx, dy), textcoords="offset points", fontsize=7.2, color="#555555", ha=ha, va="center")
ax.xaxis.set_major_locator(FixedLocator([3, 5, 10, 20, 50])); ax.xaxis.set_minor_locator(NullLocator())
ax.yaxis.set_major_locator(FixedLocator([5000, 10000, 20000, 50000, 100000])); ax.yaxis.set_minor_locator(NullLocator())
ax.xaxis.set_major_formatter(thousands); ax.yaxis.set_major_formatter(thousands)
ax.set_xlabel("Unique customers (log scale)"); ax.set_ylabel("Revenue, INR (log scale)")
fig.tight_layout(pad=0.3)

def along(x0, rpc, text, color, below):
    """Write a label parallel to the line revenue = rpc * customers, just above or below it."""
    p1, p2 = ax.transData.transform([(x0, rpc * x0), (x0 * 1.5, rpc * x0 * 1.5)])
    angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
    ax.annotate(text, (x0, rpc * x0), xytext=(0, -9 if below else 4), textcoords="offset points", rotation=angle,
                rotation_mode="anchor", fontsize=7.3, color=color, ha="left", va="center" if below else "bottom")

along(21, median_rpc, f"INR {median_rpc:,.0f} per customer (rival median)", LINE, below=False)
along(2.9, m.rpc, f"INR {m.rpc:,.0f} per customer (Montrega)", BRAND, below=False)
for ext in ("pdf", "png"):
    fig.savefig(f"figures/figure2.{ext}")
plt.close(fig)
print("figures written")
