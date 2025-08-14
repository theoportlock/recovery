#!/usr/bin/env python
# Create an improved study timeline subplot as an SVG/PNG
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.lines import Line2D

# Figure
fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

ax.set_xlim(0, 10)
ax.set_ylim(-1, 6)
ax.axis('off')

# Helper to draw a row
def draw_row(y, label_left, label_right, t1_label="12 mo (T1)", t2_label="24 mo (T2)", n=None, intervention_label=None):
    # timeline
    ax.add_line(Line2D([1, 9], [y, y]))
    # sample points
    ax.plot([2, 8], [y, y], marker='s', linestyle='None', markersize=10)
    # labels for timepoints
    ax.text(2, y+0.35, t1_label, ha='center', va='bottom', fontsize=9)
    ax.text(8, y+0.35, t2_label, ha='center', va='bottom', fontsize=9)
    # left/right group labels
    ax.text(0.2, y, label_left, ha='left', va='center', fontsize=10)
    if label_right:
        ax.text(9.3, y, label_right, ha='left', va='center', fontsize=10)
    # n
    if n is not None:
        ax.text(0.2, y-0.45, f"n={n}", ha='left', va='center', fontsize=9)
    # intervention band
    if intervention_label:
        rect = Rectangle((2.25, y-0.25), 5.5, 0.5, alpha=0.15, lw=0)
        ax.add_patch(rect)
        ax.text(5.0, y, intervention_label, ha='center', va='center', fontsize=9)
        # direction arrow (optional visual flow)
        arrow = FancyArrowPatch((2.25, y-0.35), (7.75, y-0.35), arrowstyle='-|>', mutation_scale=8, lw=1)
        ax.add_patch(arrow)

# Rows
draw_row(4.5, "MAM cohort", "ERUSF + ESQLNS", n=70, intervention_label="Enhanced refeed & supplement")
draw_row(3.0, "MAM cohort", "RUSF + SQLNS", n=70, intervention_label="Local refeed & supplement")
draw_row(1.5, "Well-nourished controls", "", n=70)

# Global time labels across top
ax.text(2, 5.4, "Baseline sampling", ha='center', fontsize=9)
ax.text(5, 5.4, "Intervention period", ha='center', fontsize=9)
ax.text(8, 5.4, "Post-refeed sampling", ha='center', fontsize=9)

# Brackets / guides
ax.add_line(Line2D([2, 2], [1.0, 5.0], linestyle='--', linewidth=0.8))
ax.add_line(Line2D([8, 8], [1.0, 5.0], linestyle='--', linewidth=0.8))

# Recovery definition note
ax.text(5, 0.2, "Primary outcome: Recovery = WLZ ≥ -1 SD", ha='center', fontsize=10)

# Measurement boxes
# Repeated measures box
rm_box = Rectangle((0.2, 5.2), 4.2, 0.9, linewidth=0.8, fill=False)
ax.add_patch(rm_box)
ax.text(0.4, 6.0, "Measured at both T1 & T2:", fontsize=9, va='top')
ax.text(0.4, 5.75, "• Anthropometry    • Stool microbiome", fontsize=8, va='top')
ax.text(0.4, 5.52, "• Plasma lipids, vitamins, amino acids", fontsize=8, va='top')
ax.text(0.4, 5.29, "• Sleep    • FCI    • Perceived stress", fontsize=8, va='top')

# Baseline/no-timepoint box
bt_box = Rectangle((4.6, 5.2), 5.2, 0.9, linewidth=0.8, fill=False)
ax.add_patch(bt_box)
ax.text(4.8, 6.0, "Baseline / one-time (or no-timepoint):", fontsize=9, va='top')
ax.text(4.8, 5.75, "• Parent education & economics    • Family structure", fontsize=8, va='top')
ax.text(4.8, 5.52, "• Household (roof, water, sanitation)    • Media use", fontsize=8, va='top')
ax.text(4.8, 5.29, "• Polygenic risk scores (PRS)", fontsize=8, va='top')

# Covariates note
ax.text(9.8, 0.2, "Covariates: Sex, Delivery mode, Place of birth", ha='right', fontsize=8)

# Save
svg_path = "results/study_timeline_subplot.svg"
png_path = "results/study_timeline_subplot.png"
fig.savefig(svg_path, bbox_inches="tight")
fig.savefig(png_path, bbox_inches="tight")
svg_path, png_path

