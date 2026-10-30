import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_data_flow_pipeline():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(project_root, "pic", "flowcharts")
    os.makedirs(out_dir, exist_ok=True)
    out_jpg = os.path.join(out_dir, "civet_dataflow_pipeline.jpg")
    out_png = os.path.join(out_dir, "civet_dataflow_pipeline.png")

    # Figure dimensions (16:9 widescreen format, high-res)
    fig_w, fig_h = 16.0, 9.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=250)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Color Palette (Teal & Gold Theme)
    C_TEAL = '#1B4958'        # Dark Teal Primary
    C_GOLD = '#E5A93C'        # Gold / Amber Accent
    C_CARD_BG = '#F8FAFC'     # Off-white / light slate card
    C_CARD_BORDER = '#CBD5E1' # Card border
    C_DARK = '#1E293B'        # Dark text
    C_MUTED = '#64748B'       # Muted text
    C_ARROW = '#94A3B8'       # Arrow connector

    # Top Decorative Line (Matching Canva Theme)
    ax.plot([0.8, 15.2], [8.65, 8.65], color=C_TEAL, linewidth=2.5, zorder=3)
    ax.plot([0.8, 2.5], [8.65, 8.65], color=C_GOLD, linewidth=3.5, zorder=4)

    # Category Tag & Title (Matching Canva Deck)
    ax.text(0.8, 8.35, "SYSTEM PIPELINE", fontsize=12, fontweight='bold',
            color=C_GOLD, fontfamily='DejaVu Sans', va='baseline')
    ax.text(0.8, 7.85, "Complete Data Flow Pipeline", fontsize=26, fontweight='bold',
            color=C_TEAL, fontfamily='DejaVu Sans', va='baseline')
    ax.text(0.8, 7.50, "9-Step End-to-End Processing Architecture | Chiang Mai Zoo × CMU",
            fontsize=12, color=C_MUTED, fontfamily='DejaVu Sans', va='baseline')

    # Card geometry
    card_w = 2.65
    card_h = 2.70
    r_corner = 0.15

    # Coordinates for Row 1 (Steps 1 to 5: Left to Right)
    col_x = [0.8, 3.8, 6.8, 9.8, 12.8]
    row1_y = 4.35
    row2_y = 1.05

    # Step Data: (Step Num, Title, Detail)
    steps_row1 = [
        (1, "Camera Streams", "4 CCTV cameras,\none per room (1080p)"),
        (2, "Video Processing", "2 FPS subsampling,\nsaves 85% compute"),
        (3, "Animal Detection", "Adaptive MOG2 vision,\nignores static plants"),
        (4, "Animal Tracking", "Centroid extraction &\nbounding box tracking"),
        (5, "Feature Extraction", "Position, speed,\nFood Tray & Tire ROIs")
    ]

    # Steps for Row 2 (6 to 9 and Scope Box: Right to Left)
    steps_row2 = [
        (6, "Behavior\nClassification", "1-min debounce rule,\nWalk, Eat, Sleep"),
        (7, "Behavior Events", "Timestamped start &\nend event records"),
        (8, "Data Storage", "Animal, Camera, Room,\nCSV & JSON logs"),
        (9, "Visualization", "Daily activity budget,\nfeeding & sleep charts")
    ]

    def draw_card(x, y, num, title, detail, is_scope=False):
        if is_scope:
            # Dark Scope Card
            rect = patches.FancyBboxPatch((x, y), card_w, card_h,
                                         boxstyle=f"round,pad=0,rounding_size={r_corner}",
                                         facecolor=C_TEAL, edgecolor=C_TEAL, linewidth=1.5, zorder=2)
            ax.add_patch(rect)
            
            # Gold Accent Top Bar
            accent = patches.FancyBboxPatch((x, y + card_h - 0.12), card_w, 0.12,
                                           boxstyle=f"round,pad=0,rounding_size=0.04",
                                           facecolor=C_GOLD, edgecolor=C_GOLD, zorder=3)
            ax.add_patch(accent)

            ax.text(x + 0.25, y + card_h - 0.55, "Phase 1 Scope", fontsize=15, fontweight='bold',
                    color='#FFFFFF', fontfamily='DejaVu Sans', va='top')
            
            scope_desc = ("Core behavior tracking\n(Walk, Eat, Sleep).\n\n"
                          "Lightweight edge vision\nrunning on standard\nzoo office PC.\n\n"
                          "No expensive GPU or\ncomplex servers needed.")
            ax.text(x + 0.25, y + card_h - 0.88, scope_desc, fontsize=10, color='#E2E8F0',
                    fontfamily='DejaVu Sans', va='top', linespacing=1.22)
        else:
            # Standard Card
            rect = patches.FancyBboxPatch((x, y), card_w, card_h,
                                         boxstyle=f"round,pad=0,rounding_size={r_corner}",
                                         facecolor=C_CARD_BG, edgecolor=C_CARD_BORDER, linewidth=1.2, zorder=2)
            ax.add_patch(rect)

            # Number Circle
            circle = plt.Circle((x + 0.52, y + card_h - 0.52), 0.32, color=C_TEAL, zorder=4)
            ax.add_patch(circle)
            ax.text(x + 0.52, y + card_h - 0.52, str(num), fontsize=13, fontweight='bold',
                    color='#FFFFFF', fontfamily='DejaVu Sans', ha='center', va='center', zorder=5)

            # Title
            ax.text(x + 0.25, y + card_h - 1.15, title, fontsize=13.5, fontweight='bold',
                    color=C_DARK, fontfamily='DejaVu Sans', va='top', linespacing=1.2)

            # Detail
            ax.text(x + 0.25, y + 0.45, detail, fontsize=11, color=C_MUTED,
                    fontfamily='DejaVu Sans', va='bottom', linespacing=1.3)

    # Draw Row 1 Cards
    for idx, (num, title, detail) in enumerate(steps_row1):
        x = col_x[idx]
        draw_card(x, row1_y, num, title, detail)

        # Arrow to next card
        if idx < 4:
            ax.annotate('', xy=(x + card_w + 0.32, row1_y + card_h/2),
                        xytext=(x + card_w + 0.03, row1_y + card_h/2),
                        arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.45',
                                        color=C_GOLD, lw=3.2), zorder=3)

    # Downward Arrow from Step 5 to Step 6
    x5 = col_x[4]
    ax.annotate('', xy=(x5 + card_w/2, row2_y + card_h + 0.05),
                xytext=(x5 + card_w/2, row1_y - 0.05),
                arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.45',
                                color=C_GOLD, lw=3.2), zorder=3)

    # Draw Row 2 Cards (Columns: 4=Step6, 3=Step7, 2=Step8, 1=Step9, 0=Scope)
    row2_cols = [
        (4, steps_row2[0]), # Step 6 at col 4
        (3, steps_row2[1]), # Step 7 at col 3
        (2, steps_row2[2]), # Step 8 at col 2
        (1, steps_row2[3]), # Step 9 at col 1
    ]

    for col_idx, (num, title, detail) in row2_cols:
        x = col_x[col_idx]
        draw_card(x, row2_y, num, title, detail)

        # Leftward arrows: from col 4 -> 3 -> 2 -> 1 -> 0
        ax.annotate('', xy=(x - 0.32, row2_y + card_h/2),
                    xytext=(x - 0.03, row2_y + card_h/2),
                    arrowprops=dict(arrowstyle='->,head_width=0.45,head_length=0.45',
                                    color=C_GOLD, lw=3.2), zorder=3)

    # Draw Phase 1 Scope Card at col 0
    draw_card(col_x[0], row2_y, 0, "", "", is_scope=True)

    plt.tight_layout()
    # Save as both JPG and PNG
    plt.savefig(out_jpg, format='jpeg', dpi=250, bbox_inches='tight', pil_kwargs={'quality': 95})
    plt.savefig(out_png, format='png', dpi=250, bbox_inches='tight')
    plt.close()
    print(f"Data Flow Pipeline diagram generated successfully:\n{out_jpg}\n{out_png}")

if __name__ == "__main__":
    draw_data_flow_pipeline()
