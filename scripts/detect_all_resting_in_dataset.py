import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"D:\CMU\4th\1 st\image processing\project cmz\pic\sleeping_evidence"
os.makedirs(out_dir, exist_ok=True)

# 1. Camera 3 Tire Bed & Under Log check
# Tire Bed ROI in 1080p: [130:420, 820:1180]
# Under Log ROI in 1080p: [350:650, 1400:1750]

cam3_vids = [
    ("A03_00.00-06.56_dur_6h56m.mp4", "00:00:00"),
    ("A03_06.56-10.54_dur_3h57m.mp4", "06:56:55"),
    ("A03_11.07-14.03_dur_2h56m.mp4", "11:07:05"),
    ("A03_14.03-18.18_dur_4h14m.mp4", "14:03:27"),
    ("A03_18.18-02.12_dur_7h54m.mp4", "18:18:06"),
]

# Let's get an empty tire bed reference frame from Cam 3 (e.g. at min 10 of A03_00.00-06.56 before civet arrives at min 37)
ref_vid = os.path.join(base_dir, "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
cap_ref = cv2.VideoCapture(ref_vid)
cap_ref.set(cv2.CAP_PROP_POS_FRAMES, int(10 * 60 * 30))
_, empty_cam3 = cap_ref.read()
cap_ref.release()

empty_tire = empty_cam3[130:420, 820:1180]
empty_tire_gray = cv2.cvtColor(empty_tire, cv2.COLOR_BGR2GRAY)

empty_log = empty_cam3[350:650, 1400:1750]
empty_log_gray = cv2.cvtColor(empty_log, cv2.COLOR_BGR2GRAY)

print("--- SCANNING CAMERA 3 VIDEOS FOR TIRE BED & UNDER LOG SLEEPING ---")
for vname, start_t in cam3_vids:
    vp = os.path.join(base_dir, "camera 3", vname)
    if not os.path.exists(vp): continue
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = (n_frames / fps) / 60.0
    
    print(f"\nScanning {vname} (Duration: {dur_min:.1f} mins, Start: {start_t})...")
    # Sample every 10 minutes
    for m in range(0, int(dur_min), 10):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(m * 60 * fps))
        ret, frame = cap.read()
        if not ret: break
        
        # Check Tire Bed
        tire_crop = frame[130:420, 820:1180]
        tire_gray = cv2.cvtColor(tire_crop, cv2.COLOR_BGR2GRAY)
        diff_tire = cv2.absdiff(empty_tire_gray, tire_gray)
        tire_score = np.mean(diff_tire)
        
        # Check Under Log
        log_crop = frame[350:650, 1400:1750]
        log_gray = cv2.cvtColor(log_crop, cv2.COLOR_BGR2GRAY)
        diff_log = cv2.absdiff(empty_log_gray, log_gray)
        log_score = np.mean(diff_log)
        
        # Calculate approximate clock time:
        sh, sm, ss = [int(x) for x in start_t.split(':')]
        curr_total_sec = sh * 3600 + sm * 60 + ss + int(m * 60)
        curr_h = (curr_total_sec // 3600) % 24
        curr_m = (curr_total_sec % 3600) // 60
        curr_s = curr_total_sec % 60
        clock_str = f"{curr_h:02d}:{curr_m:02d}:{curr_s:02d}"
        
        # If tire score > 20 or log score > 20, let's log and save frame
        status = []
        if tire_score > 22:
            status.append(f"IN_TIRE_BED (diff={tire_score:.1f})")
        if log_score > 22:
            status.append(f"UNDER_LOG (diff={log_score:.1f})")
            
        if status:
            img_name = f"cam3_{vname[:7]}_min{m:03d}_{clock_str.replace(':','')}.jpg"
            save_p = os.path.join(out_dir, img_name)
            vis = cv2.resize(frame, (640, 360))
            cv2.putText(vis, f"Clock: {clock_str} | Min: {m} | {', '.join(status)}", (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            cv2.imwrite(save_p, vis)
            print(f"  [{vname}] Min {m:3d} (Clock {clock_str}): {', '.join(status)}")
            
    cap.release()

print("\nCamera 3 scan completed.")
