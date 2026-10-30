import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

def check_time_segment(cam, fname, min_start, min_end, step_min=5):
    fpath = os.path.join(base, f"camera {cam}", fname)
    cap = cv2.VideoCapture(fpath)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    print(f"\nChecking Cam {cam} [{fname}] from Min {min_start} to {min_end}:")
    for m in range(min_start, min_end + 1, step_min):
        sec = m * 60
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if not ret: break
        
        # Save frame to check
        out_f = f"D:/CMU/4th/1 st/image processing/project cmz/pic/sleeping_evidence/verify_c{cam}_{fname[:7]}_m{m:03d}.jpg"
        cv2.imwrite(out_f, cv2.resize(frame, (640, 360)))
        print(f"  Min {m:3d} saved to {os.path.basename(out_f)}")
    cap.release()

# Let's check:
# 1. Cam 3 at night: A03_00.00-06.56 from min 40 to min 240
check_time_segment(3, "A03_00.00-06.56_dur_6h56m.mp4", 60, 200, step_min=20)

# 2. Cam 2 at feeding time: A02_11.07-12.41 from min 0 to min 60
check_time_segment(2, "A02_11.07-12.41_dur_1h34m.mp4", 0, 60, step_min=10)

# 3. Cam 3 afternoon: A03_14.03-18.18 from min 100 to min 180
check_time_segment(3, "A03_14.03-18.18_dur_4h14m.mp4", 110, 170, step_min=10)
