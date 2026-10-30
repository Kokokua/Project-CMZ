import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_eating_demo():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_path = os.path.join(project_root, "dataset", "Eating-20261005T111220Z-1-001", "Eating", "25690518092326646.mp4")
    out_dir = os.path.join(project_root, "pic", "tracking_results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "eating_tracking_result.png")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total_frames / fps
    print(f"Eating Video: {total_frames} frames, {fps:.1f} fps, {duration_s:.1f}s")

    # Define Food Zone ROI in Camera 02
    # Food Tray center is at approx (1140, 900), radius ~160 px
    # Expanded Food Zone ROI: X in [960, 1340], Y in [740, 1060]
    ROI_X1, ROI_Y1, ROI_X2, ROI_Y2 = 960, 740, 1340, 1060
    food_center = ((ROI_X1 + ROI_X2) // 2, (ROI_Y1 + ROI_Y2) // 2)

    subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=16, detectShadows=False)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    frame_idx = 0
    tracking_data = [] # (t, cx, cy, in_roi, dist_to_food, status, frame)
    base_frame = None

    sample_step = int(round(fps / 2.0)) # 2 FPS

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if base_frame is None and frame_idx == 15:
            base_frame = frame.copy()

        fg_mask = subtractor.apply(frame)

        if frame_idx % sample_step == 0 and frame_idx >= sample_step:
            t = frame_idx / fps
            fg_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_clean = cv2.dilate(fg_clean, kernel, iterations=3)

            # Mask out the plant area at center to avoid plant breeze noise
            # Plant is approx X in [800, 1150], Y in [100, 580]
            fg_clean[100:580, 800:1150] = 0

            contours, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            civet_box = None
            max_area = 0

            for c in contours:
                area = cv2.contourArea(c)
                if area > 1200:
                    if area > max_area:
                        max_area = area
                        civet_box = cv2.boundingRect(c)

            cx, cy = None, None
            in_roi = False
            dist = 999.0
            status = "MOVING"

            if civet_box is not None:
                bx, by, bw, bh = civet_box
                cx = bx + bw // 2
                cy = by + bh // 2
                
                dist = np.sqrt((cx - food_center[0])**2 + (cy - food_center[1])**2)
                # Check if centroid or head overlaps with Food Zone ROI
                if (ROI_X1 <= cx <= ROI_X2 and ROI_Y1 <= cy <= ROI_Y2) or dist < 220:
                    in_roi = True
                    status = "EATING"
                else:
                    status = "APPROACHING" if dist < 450 else "LOCOMOTION"
            else:
                # If civet is still while eating right at the tray
                if len(tracking_data) > 0 and tracking_data[-1][3]: # was in roi
                    in_roi = True
                    status = "EATING"
                    cx, cy = tracking_data[-1][1], tracking_data[-1][2]
                    dist = tracking_data[-1][4]

            tracking_data.append((t, cx, cy, in_roi, dist, status, civet_box, frame.copy()))

        frame_idx += 1

    cap.release()

    eating_frames = [item for item in tracking_data if item[3]]
    eating_duration = len(eating_frames) * 0.5
    print(f"Detected Eating Duration: {eating_duration:.1f} seconds (out of {duration_s:.1f}s)")

    # Plot 5-Panel Visualization
    fig = plt.figure(figsize=(18, 10), dpi=150)
    fig.patch.set_facecolor('#0B1120')

    # Panel 1: Approaching the Tray (t ~ 4s)
    ax1 = plt.subplot(2, 3, 1)
    f1_item = tracking_data[min(8, len(tracking_data)-1)]
    img1 = f1_item[7].copy()
    cv2.rectangle(img1, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 165, 255), 2) # ROI box
    cv2.putText(img1, "FOOD ZONE ROI", (ROI_X1, ROI_Y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
    if f1_item[6] is not None:
        bx, by, bw, bh = f1_item[6]
        cv2.rectangle(img1, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    ax1.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    ax1.set_title(f"1. Approach Food Tray (t = {f1_item[0]:.1f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # Panel 2: Actively Eating at Tray (t ~ 18s)
    ax2 = plt.subplot(2, 3, 2)
    f2_item = tracking_data[min(36, len(tracking_data)-1)]
    img2 = f2_item[7].copy()
    cv2.rectangle(img2, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 255, 0), 3) # Active Eating ROI (Green)
    cv2.putText(img2, "EATING IN PROGRESS", (ROI_X1 - 20, ROI_Y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    if f2_item[6] is not None:
        bx, by, bw, bh = f2_item[6]
        cv2.rectangle(img2, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    ax2.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"2. Feeding at Tray (t = {f2_item[0]:.1f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax2.axis('off')

    # Panel 3: Sustained Feeding (t ~ 40s)
    ax3 = plt.subplot(2, 3, 3)
    f3_item = tracking_data[min(80, len(tracking_data)-1)]
    img3 = f3_item[7].copy()
    cv2.rectangle(img3, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 255, 0), 3)
    cv2.putText(img3, f"EATING: {eating_duration:.0f}s", (ROI_X1, ROI_Y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
    if f3_item[6] is not None:
        bx, by, bw, bh = f3_item[6]
        cv2.rectangle(img3, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    ax3.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
    ax3.set_title(f"3. Sustained Eating Bout (t = {f3_item[0]:.1f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax3.axis('off')

    # Panel 4: Spatial Context Map & Food Zone Overlay
    ax4 = plt.subplot(2, 3, (4, 5))
    overlay_img = base_frame.copy()
    # Draw Food Zone Polygon
    cv2.rectangle(overlay_img, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 140, 255), 4)
    cv2.putText(overlay_img, "TARGET FOOD TRAY ZONE (ROI)", (ROI_X1 - 80, ROI_Y1 - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 140, 255), 2)

    # Draw Civet positions while eating
    for item in tracking_data:
        if item[3] and item[1] is not None: # in roi
            cv2.circle(overlay_img, (int(item[1]), int(item[2])), 6, (0, 255, 0), -1)

    cv2.putText(overlay_img, f"FEEDING BOUT CONFIRMED: Duration = {eating_duration:.1f}s (Freq count: +1)", 
                (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 128), 2)

    ax4.imshow(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB))
    ax4.set_title("4. Spatial Food Zone ROI & Head Localization Map (Camera 02)", color='#F59E0B', fontsize=13, fontweight='bold')
    ax4.axis('off')

    # Panel 5: Eating State & Distance to Tray Graph
    ax5 = plt.subplot(2, 3, 6)
    times = [item[0] for item in tracking_data]
    distances = [min(600, item[4]) for item in tracking_data]
    eating_mask = [1 if item[3] else 0 for item in tracking_data]

    ax5.set_facecolor('#1E293B')
    ax5.plot(times, distances, color='#F59E0B', linewidth=2.0, label='Distance to Tray (px)')
    ax5.axhline(y=220, color='#10B981', linestyle='--', linewidth=1.5, label='Food Zone Threshold')
    ax5.fill_between(times, 0, 600, where=[m == 1 for m in eating_mask], color='#10B981', alpha=0.25, label='Active Eating Window')
    
    ax5.set_title("5. Food Zone Proximity & Eating Bout", color='#F8FAFC', fontsize=12, fontweight='bold')
    ax5.set_xlabel("Time (seconds)", color='#94A3B8', fontsize=10)
    ax5.set_ylabel("Distance to Food Tray (pixels)", color='#94A3B8', fontsize=10)
    ax5.set_ylim(0, 550)
    ax5.tick_params(colors='#94A3B8')
    ax5.grid(True, linestyle=':', alpha=0.3, color='#64748B')
    ax5.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=9)

    plt.suptitle("Automated Civet Behavior: Real Eating & Feeding Duration Analysis (Camera 02)",
                 color='#F8FAFC', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Eating demo saved successfully: {out_path}")

if __name__ == "__main__":
    create_eating_demo()
