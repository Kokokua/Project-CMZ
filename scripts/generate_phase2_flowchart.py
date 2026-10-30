import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects

def draw_phase2_pipeline_flowchart():
    project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
    out_dir = os.path.join(project_root, "pic", "flowcharts")
    finish_dir = os.path.join(project_root, "finish")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(finish_dir, exist_ok=True)

    # 16:9 widescreen format, 250 DPI
    fig_w, fig_h = 16.0, 9.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Color Palette matching Phase 1 & 2 presentations
    C_TEAL = '#1B4958'        # Primary Dark Teal
    C_TEAL_LIGHT = '#2A667A'
    C_GOLD = '#D97706'        # Gold / Amber Accent
    C_CARD_BG = '#F8FAFC'     # Slate 50
    C_CARD_BORDER = '#CBD5E1' # Slate 300
    C_DARK = '#0F172A'        # Slate 900
    C_MUTED = '#64748B'       # Slate 500
    C_EMERALD = '#059669'     # Emerald 600
    C_AMBER = '#D97706'       # Amber 600
    C_BLUE = '#2563EB'        # Blue 600

    # Top Header Banner
    ax.plot([0.8, 15.2], [8.65, 8.65], color=C_TEAL, linewidth=2.5, zorder=3)
    ax.plot([0.8, 3.2], [8.65, 8.65], color=C_GOLD, linewidth=3.5, zorder=4)

    ax.text(0.8, 8.32, "PHASE 2 MASTER PIPELINE | CHIANG MAI ZOO × CMU 2026",
            fontsize=10, fontweight='bold', color=C_GOLD, fontfamily='DejaVu Sans', va='baseline')
    ax.text(0.8, 7.82, "AI-Driven Zoological Monitoring Architecture",
            fontsize=22, fontweight='bold', color=C_TEAL, fontfamily='DejaVu Sans', va='baseline')
    ax.text(0.8, 7.48, "Synchronized Master Camera 03 Setup + Hybrid YOLOv8 & Spatial ROI State Machine",
            fontsize=11.5, color=C_MUTED, fontfamily='DejaVu Sans', va='baseline')

    # Helper function to draw rounded cards
    def draw_card(x, y, w, h, title, subtitle, bullets, accent=C_TEAL, badge_text=""):
        # Card background
        card = patches.FancyBboxPatch((x, y), w, h,
                                      boxstyle="round,pad=0.08,rounding_size=0.18",
                                      facecolor=C_CARD_BG, edgecolor=accent,
                                      linewidth=1.8, zorder=2)
        ax.add_patch(card)

        # Header tag/badge
        if badge_text:
            badge = patches.FancyBboxPatch((x + 0.15, y + h - 0.38), len(badge_text)*0.11 + 0.3, 0.28,
                                          boxstyle="round,pad=0.04,rounding_size=0.08",
                                          facecolor=accent, edgecolor='none', zorder=3)
            ax.add_patch(badge)
            ax.text(x + 0.22, y + h - 0.24, badge_text, fontsize=8.5, fontweight='bold',
                    color='#FFFFFF', fontfamily='DejaVu Sans', va='center', zorder=4)

        # Title
        title_y = y + h - 0.65 if badge_text else y + h - 0.45
        ax.text(x + 0.2, title_y, title, fontsize=12.5, fontweight='bold',
                color=accent, fontfamily='DejaVu Sans', va='top', zorder=3)
        if subtitle:
            ax.text(x + 0.2, title_y - 0.28, subtitle, fontsize=9.5, fontweight='bold',
                    color=C_MUTED, fontfamily='DejaVu Sans', va='top', zorder=3)

        # Bullets
        start_by = title_y - 0.60
        for idx, b in enumerate(bullets):
            ax.text(x + 0.2, start_by - (idx * 0.32), "• " + b,
                    fontsize=9.0, color=C_DARK, fontfamily='DejaVu Sans', va='top', zorder=3)

    # Helper function to draw arrows
    def draw_arrow(x1, y1, x2, y2, color=C_GOLD, label=""):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=2.0, headwidth=7, shrink=0.05),
                    zorder=5)
        if label:
            mx, my = (x1 + x2)/2.0, (y1 + y2)/2.0
            ax.text(mx, my + 0.15, label, fontsize=8, fontweight='bold',
                    color=color, ha='center', va='center', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=color, linewidth=0.8))

    # =========================================================================
    # ROW 1 (Steps 1 to 3: Acquisition -> AI Localization -> Spatial Fusion)
    # =========================================================================
    card_w = 4.35
    card_h = 2.85
    y_row1 = 4.25
    y_row2 = 1.05

    # 1. Multi-Camera CCTV Stream
    draw_card(0.8, y_row1, card_w, card_h,
              "1. 24-Hour Multi-Camera",
              "Synchronized CCTV Streams (1080p)",
              ["Master Cam 03: Primary Enclosure",
               "  - Contains Food Tray, Tires, Sand Floor",
               "Cam 02: Morning Sleeping Box (05:55-11:06)",
               "Cam 01 & 04: Pass-Through Corridor & Water",
               "Timeline: 00:00:00 - 24:00:00 (Full Day)"],
              accent=C_TEAL, badge_text="INPUT DATASET")

    # 2. AI Animal Localization (YOLOv8n)
    draw_card(5.8, y_row1, card_w, card_h,
              "2. AI Animal Localization",
              "Fine-Tuned YOLOv8n Network (6.2 MB)",
              ["Backbone: CSPDarknet with C2f + SPPF",
               "Neck: PAN-FPN Multi-Scale Feature Fusion",
               "Head: Decoupled Anchor-Free Detection Head",
               "Outputs: Civet Bounding Box [x, y, w, h]",
               "Real-time Edge Speed: >50 FPS on GPU"],
              accent=C_BLUE, badge_text="DEEP LEARNING")

    # 3. Spatial ROIs & Kinematics
    draw_card(10.8, y_row1, card_w, card_h,
              "3. Spatial ROI & Kinematics",
              "Zoological Coordinate Mapping (Cam 03)",
              ["Food Tray ROI [X:680-840, Y:480-600]",
               "  - Afternoon feeding placed at 15:33:20",
               "Tire Bed Shelter ROI [X:820-1180, Y:130-420]",
               "Under-Log Shelter ROI [X:1400-1750, Y:350-650]",
               "Speed Vector: v = sqrt(Δx² + Δy²) / Δt"],
              accent=C_GOLD, badge_text="HEURISTIC FUSION")

    # Arrows for Row 1
    draw_arrow(5.15, y_row1 + card_h/2.0, 5.8, y_row1 + card_h/2.0, color=C_GOLD, label="Subsample 1-2 FPS")
    draw_arrow(10.15, y_row1 + card_h/2.0, 10.8, y_row1 + card_h/2.0, color=C_GOLD, label="Centroid (cx, cy)")

    # Downward connection from Row 1 to Row 2
    draw_arrow(13.0, y_row1, 13.0, y_row2 + card_h, color=C_GOLD, label="ROI Match & Speed")

    # =========================================================================
    # ROW 2 (Steps 4 to 6: Right to Left)
    # =========================================================================

    # 4. Zoological State Machine (1-Minute Rule)
    draw_card(10.8, y_row2, card_w, card_h,
              "4. Zoological State Machine",
              "1-Minute Temporal Persistence Rule",
              ["Dual-Tier Behavioral Decision Engine",
               "Debounce Filter: State must persist >= 60s",
               "Eliminates State Flickering (>96% Stability)",
               "Distinguishes pauses from deep sleep",
               "Robust across Day Color and Night IR"],
              accent=C_AMBER, badge_text="TEMPORAL LOGIC")

    # 5. Dual Production Outputs
    draw_card(5.8, y_row2, card_w, card_h,
              "5. Dual System Outputs",
              "Structured Tables & Vet Dashboard",
              ["Event Log: civet_activity_event_log.csv",
               "  - Timestamps, Macro/Sub State, Duration, Zone",
               "Activity Budget: 37.2% Active vs 62.8% Inactive",
               "24-Hour Temporal Ethogram (Actogram)",
               "Visualized 4-Cam Overlays & Telemetry"],
              accent=C_EMERALD, badge_text="SYSTEM OUTPUTS")

    # 6. Deliverables & Zoo Handoff
    draw_card(0.8, y_row2, card_w, card_h,
              "6. Final Submission & Impact",
              "GitHub, Roboflow & Animal Welfare",
              ["Clean GitHub Repository (Zero heavy media)",
               "Roboflow Universe Annotation Link (193 frames)",
               "12-Slide Final Presentation Deck (PPTX)",
               "Non-Invasive 24-hr Veterinary Telemetry",
               "CMZ Zoo Management & Care Plan"],
              accent=C_TEAL, badge_text="DELIVERABLES")

    # Arrows for Row 2 (Right to Left)
    draw_arrow(10.8, y_row2 + card_h/2.0, 10.15, y_row2 + card_h/2.0, color=C_GOLD, label="Verified States")
    draw_arrow(5.8, y_row2 + card_h/2.0, 5.15, y_row2 + card_h/2.0, color=C_GOLD, label="Reports & Data")

    # Save outputs
    out_png = os.path.join(out_dir, "phase2_pipeline_flowchart_th.png")
    out_jpg = os.path.join(out_dir, "phase2_pipeline_flowchart_th.jpg")
    fin_png = os.path.join(finish_dir, "phase2_pipeline_flowchart.png")

    plt.savefig(out_png, dpi=250, bbox_inches='tight')
    plt.savefig(out_jpg, dpi=250, bbox_inches='tight')
    plt.savefig(fin_png, dpi=250, bbox_inches='tight')
    plt.close()

    print(f"Successfully generated Phase 2 Flowchart at:")
    print(f"  1. {out_png}")
    print(f"  2. {out_jpg}")
    print(f"  3. {fin_png}")

if __name__ == "__main__":
    draw_phase2_pipeline_flowchart()
