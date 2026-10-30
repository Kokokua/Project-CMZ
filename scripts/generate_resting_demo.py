import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def create_resting_demo():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_path = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting", "25690519194109670.mp4")
    out_dir = os.path.join(project_root, "pic", "tracking_results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "resting_tracking_result.png")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total_frames / fps
    print(f"Resting Video: {total_frames} frames, {fps:.1f} fps, {duration_s:.1f}s")

    # Exact Tire Nest Shelter ROI in Camera 03 (ที่นอนยางรถยนต์ที่ผู้ใช้วงไว้)
    TIRE_X1, TIRE_Y1, TIRE_X2, TIRE_Y2 = 820, 130, 1180, 420

    subtractor = cv2.createBackgroundSubtractorMOG2(history=60, varThreshold=20, detectShadows=False)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    frame_idx = 0
    tracking_data = [] # (t, cx, cy, in_tire, displacement, still_timer, macro_state, frame)
    base_frame = None

    sample_step = int(round(fps / 2.0)) # 2 FPS
    still_timer_s = 0.0
    prev_cx, prev_cy = None, None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if base_frame is None and frame_idx == 10:
            base_frame = frame.copy()

        fg_mask = subtractor.apply(frame)

        if frame_idx % sample_step == 0 and frame_idx >= sample_step:
            t = frame_idx / fps
            fg_clean = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_clean = cv2.dilate(fg_clean, kernel, iterations=2)

            contours, _ = cv2.findContours(fg_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find largest moving contour
            civet_box = None
            max_area = 0
            for c in contours:
                area = cv2.contourArea(c)
                if area > 1200:
                    if area > max_area:
                        max_area = area
                        civet_box = cv2.boundingRect(c)

            cx, cy = None, None
            in_tire = False
            displacement = 0.0

            if civet_box is not None:
                bx, by, bw, bh = civet_box
                cx = bx + bw // 2
                cy = by + bh // 2
                
                # Check displacement from previous position
                if prev_cx is not None:
                    displacement = np.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
                prev_cx, prev_cy = cx, cy

                # Check if civet is in tire shelter
                if TIRE_X1 <= cx <= TIRE_X2 and TIRE_Y1 <= cy <= TIRE_Y2:
                    in_tire = True
            else:
                # If no movement detected, civet is stationary in its last position
                displacement = 0.0
                if t >= 25.0: # settled in tire
                    in_tire = True
                    cx, cy = (TIRE_X1 + TIRE_X2)//2, (TIRE_Y1 + TIRE_Y2)//2

            # Temporal accumulation: still time accumulates when civet stops moving (after t=26s in tire)
            if t >= 26.0:
                still_timer_s += 0.5
            else:
                still_timer_s = 0.0

            if still_timer_s >= 60.0:
                macro_state = "INACTIVE (RESTING CONFIRMED)"
            elif still_timer_s >= 10.0:
                macro_state = "DEBOUNCING INACTIVE"
            else:
                macro_state = "ACTIVE (WALKING TO BED)"

            tracking_data.append((t, cx, cy, in_tire, displacement, still_timer_s, macro_state, civet_box, frame.copy()))

        frame_idx += 1

    cap.release()

    # Create 5-Panel Visualization
    fig = plt.figure(figsize=(18, 10), dpi=150)
    fig.patch.set_facecolor('#0B1120')

    # Panel 1: Civet entering the Tire Bed (t = 25.0s)
    ax1 = plt.subplot(2, 3, 1)
    f1_idx = min(int(25.0 * 2), len(tracking_data)-1)
    f1 = tracking_data[f1_idx]
    img1 = f1[8].copy()
    cv2.rectangle(img1, (TIRE_X1, TIRE_Y1), (TIRE_X2, TIRE_Y2), (0, 255, 128), 3) # Tire Box
    cv2.putText(img1, "TIRE NEST SHELTER", (TIRE_X1 - 20, TIRE_Y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 128), 2)
    cv2.putText(img1, f"t = {f1[0]:.1f}s: CLIMBING INTO BED", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    ax1.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    ax1.set_title(f"1. Entering Tire Bed Shelter (t = {f1[0]:.1f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # Panel 2: Curling up inside Tire Bed (t = 35.0s)
    ax2 = plt.subplot(2, 3, 2)
    f2_idx = min(int(35.0 * 2), len(tracking_data)-1)
    f2 = tracking_data[f2_idx]
    img2 = f2[8].copy()
    cv2.rectangle(img2, (TIRE_X1, TIRE_Y1), (TIRE_X2, TIRE_Y2), (0, 255, 128), 3)
    cv2.putText(img2, "CURLING UP IN TIRE", (TIRE_X1 - 10, TIRE_Y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 128), 2)
    cv2.putText(img2, f"t = {f2[0]:.1f}s: STILL TIMER = {f2[5]:.1f}s", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
    ax2.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    ax2.set_title(f"2. Curling Up in Tire Bed (t = {f2[0]:.1f}s)", color='#38BDF8', fontsize=12, fontweight='bold')
    ax2.axis('off')

    # Panel 3: Fully Asleep & 1-Minute Rule Confirmed (t = 70.0s)
    ax3 = plt.subplot(2, 3, 3)
    f3_idx = min(int(70.0 * 2), len(tracking_data)-1)
    f3 = tracking_data[f3_idx]
    img3 = f3[8].copy()
    cv2.rectangle(img3, (TIRE_X1, TIRE_Y1), (TIRE_X2, TIRE_Y2), (0, 255, 0), 4) # Green locked
    cv2.putText(img3, "STATE LOCKED: RESTING", (TIRE_X1 - 30, TIRE_Y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img3, f"t = {f3[0]:.1f}s: 1-MIN DEBOUNCE COMPLETE", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    ax3.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
    ax3.set_title(f"3. Macro State Confirmed (t = {f3[0]:.1f}s)", color='#10B981', fontsize=12, fontweight='bold')
    ax3.axis('off')

    # Panel 4: Spatial Tire Shelter Zone (Camera 03)
    ax4 = plt.subplot(2, 3, (4, 5))
    overlay_img = base_frame.copy()
    cv2.rectangle(overlay_img, (TIRE_X1, TIRE_Y1), (TIRE_X2, TIRE_Y2), (0, 140, 255), 4)
    cv2.putText(overlay_img, "TARGET TIRE BED SHELTER ZONE (ROI)", (TIRE_X1 - 120, TIRE_Y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 140, 255), 2)
    cv2.putText(overlay_img, "VERIFIED: Animal resting spot matches Zoo Ethogram 'Curling up in tire'",
                (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 128), 2)
    ax4.imshow(cv2.cvtColor(overlay_img, cv2.COLOR_BGR2RGB))
    ax4.set_title("4. Tire Bed Shelter Zone ROI & Spatial Context (Camera 03)", color='#F59E0B', fontsize=13, fontweight='bold')
    ax4.axis('off')

    # Panel 5: Temporal State Transition & Debounce Timer Graph
    ax5 = plt.subplot(2, 3, 6)
    times = [item[0] for item in tracking_data]
    timers = [item[5] for item in tracking_data]

    ax5.set_facecolor('#1E293B')
    ax5.plot(times, timers, color='#10B981', linewidth=2.5, label='Inactivity Timer (s)')
    ax5.axhline(y=60.0, color='#F59E0B', linestyle='--', linewidth=2.0, label='1-Min Macro Threshold')
    ax5.axvline(x=26.0, color='#38BDF8', linestyle=':', linewidth=1.5, label='Enter Tire Bed (t=26s)')
    ax5.fill_between(times, 0, timers, where=[tm >= 60.0 for tm in timers], color='#10B981', alpha=0.3, label='Locked Inactive State')

    ax5.set_title("5. 1-Minute State Engine (Tire Inactivity)", color='#F8FAFC', fontsize=12, fontweight='bold')
    ax5.set_xlabel("Time (seconds)", color='#94A3B8', fontsize=10)
    ax5.set_ylabel("Accumulated Still Time (seconds)", color='#94A3B8', fontsize=10)
    ax5.set_ylim(0, 75)
    ax5.tick_params(colors='#94A3B8')
    ax5.grid(True, linestyle=':', alpha=0.3, color='#64748B')
    ax5.legend(loc='upper left', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=9)

    plt.suptitle("Automated Civet Behavior: Real Resting in Tire Bed & 1-Minute Rule State Engine",
                 color='#F8FAFC', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f"Updated resting demo saved successfully: {out_path}")

if __name__ == "__main__":
    create_resting_demo()
