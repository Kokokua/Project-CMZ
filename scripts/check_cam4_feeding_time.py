import cv2, os, glob
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
vpath = os.path.join(base_dir, "camera 4", "A04_11.07-12.40_dur_1h33m.mp4")
cap = cv2.VideoCapture(vpath)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Reference empty room
ret, ref = cap.read()
ref_g = cv2.GaussianBlur(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY), (21, 21), 0)

print(f"Scanning Camera 4 11:07-12:40 ({total_frames/fps/60:.1f} mins)...")
found_list = []
for sec in range(0, int(total_frames/fps), 5):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
    ret, frame = cap.read()
    if not ret: break
    g = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    diff = cv2.absdiff(ref_g, g)
    diff[350:600, 1300:1550] = 0 # plant
    _, th = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c) > 3000:
            m = sec // 60
            s = sec % 60
            found_list.append((m, s, cv2.contourArea(c)))
            if len(found_list) <= 5:
                cv2.imwrite(f"pic/inspections/cam4_civet_{m:02d}m_{s:02d}s.jpg", frame)
                print(f"  Cam 4 found civet at {m:02d}:{s:02d} area={cv2.contourArea(c):.0f}")
            break
cap.release()
print(f"Total civet frames in Cam 4 11:07-12:40: {len(found_list)}")
