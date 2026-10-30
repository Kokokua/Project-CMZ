import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"D:\CMU\4th\1 st\image processing\project cmz\pic\sleeping_evidence\cam2"
os.makedirs(out_dir, exist_ok=True)

cam2_vids = [
    ("A02_00.00-05.55_dur_5h55m.mp4", "00:00:00"),
    ("A02_05.55-09.51_dur_3h56m.mp4", "05:55:26"),
    ("A02_09.51-11.06_dur_1h14m.mp4", "09:51:30"),
    ("A02_11.07-12.41_dur_1h34m.mp4", "11:07:05"),
    ("A02_12.41-15.22_dur_2h41m.mp4", "12:41:27"),
    ("A02_15.22-19.33_dur_4h10m.mp4", "15:22:41"),
    ("A02_19.33-01.49_dur_6h15m.mp4", "19:33:16"),
]

# Let's inspect where civet is in Room 2:
# 1. Sleeping box / ledge behind plant (X: 300..1600, Y: 50..450)
# 2. Ramp near doorway (X: 100..450, Y: 350..700)
# 3. Floor (X: 450..1200, Y: 450..1080)

# We check whether the floor is empty (civet not on floor)
# And whether civet is on ramp or in box.
for vname, start_t in cam2_vids:
    vp = os.path.join(base_dir, "camera 2", vname)
    if not os.path.exists(vp): continue
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = (n_frames / fps) / 60.0
    
    print(f"\nChecking {vname} ({dur_min:.1f} mins, Start: {start_t})...")
    # Sample every 15 minutes
    for m in range(0, int(dur_min), 15):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(m * 60 * fps))
        ret, frame = cap.read()
        if not ret: break
        
        # Calculate clock time
        sh, sm, ss = [int(x) for x in start_t.split(':')]
        curr_total_sec = sh * 3600 + sm * 60 + ss + int(m * 60)
        curr_h = (curr_total_sec // 3600) % 24
        curr_m = (curr_total_sec % 3600) // 60
        curr_s = curr_total_sec % 60
        clock_str = f"{curr_h:02d}:{curr_m:02d}:{curr_s:02d}"
        
        # Check ramp crop: [350:700, 100:450]
        # Check sleeping box crop: [60:350, 300:750] (left ledge behind plant)
        ramp_crop = frame[350:700, 100:450]
        box_crop = frame[60:350, 300:750]
        
        # Save a sample image
        save_p = os.path.join(out_dir, f"{vname[:7]}_min{m:03d}_{clock_str.replace(':','')}.jpg")
        vis = cv2.resize(frame, (640, 360))
        cv2.putText(vis, f"{vname[:7]} | Min {m} | Clock {clock_str}", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.imwrite(save_p, vis)
        
    cap.release()
print("Camera 2 sampling finished.")
