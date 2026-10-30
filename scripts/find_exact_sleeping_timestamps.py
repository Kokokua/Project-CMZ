import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"D:\CMU\4th\1 st\image processing\project cmz\pic\sleeping_evidence"
os.makedirs(out_dir, exist_ok=True)

# We want to check all files in Camera 2 and Camera 3:
cam2_files = sorted(glob.glob(os.path.join(base_dir, "camera 2", "*.mp4")))
cam3_files = sorted(glob.glob(os.path.join(base_dir, "camera 3", "*.mp4")))

print(f"Total Cam 2 files: {len(cam2_files)}")
print(f"Total Cam 3 files: {len(cam3_files)}")

# 1. Inspect Camera 2 files:
# Check if civet is visible on floor, or if room is empty (meaning civet is in sleeping box / ledge behind plant or in room 3)
# Specifically, we know:
# - A02_00.00-05.55_dur_5h55m.mp4: 00:00:00 to 00:35:40 is sleeping in box.
# Let's inspect where civet is at various times:
# Check at 01:00, 02:00, 03:00, 04:00, 05:00
# Check A02_05.55-09.51_dur_3h56m.mp4
# Check A02_09.51-11.06_dur_1h14m.mp4
# Check A02_11.07-12.41_dur_1h34m.mp4
# Check A02_12.41-15.22_dur_2h41m.mp4
# Check A02_15.22-19.33_dur_4h10m.mp4
# Check A02_19.33-01.49_dur_6h15m.mp4

# Also inspect Camera 3 files:
# Check A03_00.00-06.56_dur_6h56m.mp4
# Check A03_06.56-10.54_dur_3h57m.mp4
# Check A03_11.07-14.03_dur_2h56m.mp4
# Check A03_14.03-18.18_dur_4h14m.mp4
# Check A03_18.18-02.12_dur_7h54m.mp4

def sample_video_every_n_minutes(video_path, step_minutes=15, prefix=""):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = (n_frames / fps) / 60.0
    fname = os.path.basename(video_path)
    
    print(f"\nScanning {fname} (total {dur_min:.1f} mins)...")
    results = []
    
    for m in range(0, int(dur_min), step_minutes):
        frame_idx = int(m * 60 * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret: break
        
        # Save a compressed preview
        save_name = f"{prefix}_{fname[:7]}_min_{m:03d}.jpg"
        save_path = os.path.join(out_dir, save_name)
        # resize for quick review
        preview = cv2.resize(frame, (640, 360))
        cv2.imwrite(save_path, preview)
        results.append((m, save_name))
        
    cap.release()
    return results

print("Starting sampling...")
