import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_locomotion_demo():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_path = os.path.join(project_root, "dataset", "Locomotion-20261005T111244Z-1-001", "Locomotion", "25690518091012230.mp4")
    out_dir = os.path.join(project_root, "pic", "tracking_results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "locomotion_tracking_result.png")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=25, detectShadows=False)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    frame_idx = 0
    all_frames = []
    tracking_history = [] # (t, cx, cy, box, area, status)
    
    # Store first base frame for trajectory overlay
    base_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if base_frame is None and frame_idx == 10:
            base_frame = frame.copy()

        fg_mask = subtractor.apply(frame)

        # Sample at ~2 FPS (every 8 frames)
        if frame_idx % 8 == 0 and frame_idx >= 8:
            fg_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_clean = cv2.dilate(fg_clean, kernel, iterations=3)
            contours, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            civet_box = None
            max_area = 0
            for c in contours:
                area = cv2.contourArea(c)
                if area > 2000: # filter out noise
                    if area > max_area:
                        max_area = area
                        civet_box = cv2.boundingRect(c)

            t = frame_idx / fps
            if civet_box is not None:
                x, y, w, h = civet_box
                cx, cy = x + w // 2, y + h // 2
                tracking_history.append((t, cx, cy, civet_box, max_area, "LOCOMOTION", frame.copy()))
            else:
                tracking_history.append((t, None, None, None, 0, "STILL", frame.copy()))

        frame_idx += 1

    cap.release()

    # Calculate displacements
    displacements = [0.0]
    for i in range(1, len(tracking_history)):
        curr_pt = (tracking_history[i][1], tracking_history[i][2])
        prev_pt = (tracking_history[i-1][1], tracking_history[i-1][2])
        if curr_pt[0] is not None and prev_pt[0] is not None:
            d = np.sqrt((curr_pt[0] - prev_pt[0])**2 + (curr_pt[1] - prev_pt[1])**2)
        else:
            d = 0.0
        displacements.append(d)

    # Plot 4-Panel Figure
    fig = plt.figure(figsize=(18, 10), dpi=150)
    fig.patch.set_facecolor('#0B1120')

    # Subplot 1: Entry Frame (t = 1.07s)
    ax1 = plt.subplot(2, 3, 1)
    f1_item = [item for item in tracking_history if item[5] == "LOCOMOTION"][0]
    img1 = f1_item[6].copy()
    bx, by, bw, bh = f1_item[3]
    cv2.rectangle(img1, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    cv2.circle(img1, (f1_item[1], f1_item[2]), 10, (0, 165, 255), -1)
    cv2.putText(img1, f"START: t={f1_item[0]:.2f}s", (bx, max(30, by - 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
    ax1.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    ax1.set_title(f"1. Entry & Start of Walk (t = {f1_item[0]:.2f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # Subplot 2: Mid-Walk Frame (t = 2.67s)
    ax2 = plt.subplot(2, 3, 2)
    f2_item = [item for item in tracking_history if item[5] == "LOCOMOTION"][3]
    img2 = f2_item[6].copy()
    bx, by, bw, bh = f2_item[3]
    cv2.rectangle(img2, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    cv2.circle(img2, (f2_item[1], f2_item[2]), 10, (0, 165, 255), -1)
    cv2.putText(img2, f"WALKING: t={f2_item[0]:.2f}s", (bx, max(30, by - 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
    ax2.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"2. Active Locomotion (t = {f2_item[0]:.2f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax2.axis('off')

    # Subplot 3: End of Walk Frame (t = 4.27s)
    ax3 = plt.subplot(2, 3, 3)
    f3_item = [item for item in tracking_history if item[5] == "LOCOMOTION"][-1]
    img3 = f3_item[6].copy()
    bx, by, bw, bh = f3_item[3]
    cv2.rectangle(img3, (bx, by), (bx + bw, by + bh), (0, 255, 128), 3)
    cv2.circle(img3, (f3_item[1], f3_item[2]), 10, (0, 165, 255), -1)
    cv2.putText(img3, f"PAUSE: t={f3_item[0]:.2f}s", (bx - 50, max(30, by - 12)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
    ax3.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
    ax3.set_title(f"3. Reach Destination (t = {f3_item[0]:.2f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax3.axis('off')

    # Subplot 4: Full Trajectory Map Overlay (Spanning bottom 2 columns)
    ax4 = plt.subplot(2, 3, (4, 5))
    traj_img = base_frame.copy()
    valid_pts = [(item[1], item[2]) for item in tracking_history if item[1] is not None]

    for j in range(1, len(valid_pts)):
        p1 = valid_pts[j-1]
        p2 = valid_pts[j]
        cv2.line(traj_img, p1, p2, (0, 140, 255), 5) # Vibrant Orange-Red line
        cv2.circle(traj_img, p2, 8, (0, 255, 255), -1)

    # Start and End Markers
    p_start = valid_pts[0]
    p_end = valid_pts[-1]
    cv2.circle(traj_img, p_start, 14, (0, 255, 0), -1) # Green
    cv2.putText(traj_img, "START (t=1.07s)", (p_start[0] - 60, p_start[1] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.circle(traj_img, p_end, 14, (0, 0, 255), -1) # Red
    cv2.putText(traj_img, "DESTINATION (t=4.27s)", (p_end[0] - 120, p_end[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    ax4.imshow(cv2.cvtColor(traj_img, cv2.COLOR_BGR2RGB))
    ax4.set_title("4. Full Motion Trajectory Map Across Camera 03", color='#F59E0B', fontsize=13, fontweight='bold')
    ax4.axis('off')

    # Subplot 5: Displacement / Speed Graph (Bottom Right)
    ax5 = plt.subplot(2, 3, 6)
    times = [item[0] for item in tracking_history]
    ax5.set_facecolor('#1E293B')
    ax5.plot(times, displacements, color='#38BDF8', linewidth=2.5, marker='o', markersize=6, label='Motion Velocity')
    ax5.axhline(y=15.0, color='#EF4444', linestyle='--', linewidth=1.5, label='Locomotion Threshold (15 px)')
    ax5.fill_between(times, 0, displacements, where=[d > 15.0 for d in displacements], color='#0284C7', alpha=0.3)
    ax5.set_title("5. Motion Displacement vs. Time", color='#F8FAFC', fontsize=12, fontweight='bold')
    ax5.set_xlabel("Time (seconds)", color='#94A3B8', fontsize=10)
    ax5.set_ylabel("Displacement (pixels / 0.5s)", color='#94A3B8', fontsize=10)
    ax5.tick_params(colors='#94A3B8')
    ax5.grid(True, linestyle=':', alpha=0.3, color='#64748B')
    ax5.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=9)

    plt.suptitle("Automated Civet Tracking: Real Dataset Test (Camera 03 Locomotion)",
                 color='#F8FAFC', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Tracking demo saved successfully: {out_path}")

if __name__ == "__main__":
    create_locomotion_demo()
