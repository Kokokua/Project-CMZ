import cv2, os, glob
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

# We want to examine all files in Camera 2 and Camera 3 in dataset/ชะมดแผงสันหางดำ
# To find every single sleeping/resting event and its exact video name, timestamp, and duration!

print("Scanning 24h files in Camera 2 and Camera 3 for resting events...")

# Let's inspect Camera 3 files during daytime
# In daytime (e.g. 06:56 - 10:54, 11:07 - 14:03, 14:03 - 18:18), does Hompom sleep in the tire bed or under the log?
cam3_files = [
    'A03_00.00-06.56_dur_6h56m.mp4',
    'A03_06.56-10.54_dur_3h57m.mp4',
    'A03_11.07-14.03_dur_2h56m.mp4',
    'A03_14.03-18.18_dur_4h14m.mp4',
]

for f in cam3_files:
    fp = os.path.join(base_dir, 'camera 3', f)
    if not os.path.exists(fp): continue
    cap = cv2.VideoCapture(fp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = (n_frames / fps) / 60.0
    
    # Check tire bed ROI: X in [820, 1180], Y in [130, 420]
    # Check under log ROI: X in [1200, 1750], Y in [300, 700]
    # Sample every 10 minutes
    print(f"\n--- {f} ({dur_min:.1f} mins) ---")
    for m in range(0, int(dur_min), 10):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(m * 60 * fps))
        ret, frame = cap.read()
        if not ret: break
        
        # Check mean intensity in tire bed
        tire_crop = frame[130:420, 820:1180]
        # Let's save a thumbnail if something is there or check visually
        if m in [0, 30, 60, 90, 120, 150, 180, 210]:
            out_p = f"pic/inspections/cam3_{f[:7]}_min_{m:03d}.jpg"
            os.makedirs("pic/inspections", exist_ok=True)
            cv2.imwrite(out_p, cv2.resize(frame, (640, 360)))
    cap.release()
print("Sampled successfully.")
