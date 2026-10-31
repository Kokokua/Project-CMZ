import cv2
import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

model = YOLO('models/yolov8n_civet_phase2/weights/best.pt')
os.makedirs('scratch/candidates', exist_ok=True)

# 1. Check A03_00.00-06.56 at sec 5395 (01:29:55)
vpath_c3_night = 'dataset/ชะมดแผงสันหางดำ/camera 3/A03_00.00-06.56_dur_6h56m.mp4'
if os.path.exists(vpath_c3_night):
    cap = cv2.VideoCapture(vpath_c3_night)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    for s in [5360, 5395, 5420, 5450, 5480]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * fps))
        ret, frame = cap.read()
        if ret:
            res = model.predict(frame, conf=0.25, verbose=False)[0]
            boxes = [b.xyxy[0].tolist() for b in res.boxes]
            confs = [float(b.conf[0]) for b in res.boxes]
            cv2.imwrite(f'scratch/candidates/c3_night_sec_{s}.jpg', frame)
            print(f'Cam 3 Night sec {s}: found {len(boxes)} civets, confs={confs}, boxes={boxes}')
    cap.release()

# 2. Check Resting folder clips
resting_dir = 'dataset/Resting-20261005T111307Z-1-001/Resting'
if os.path.exists(resting_dir):
    for f in sorted(os.listdir(resting_dir)):
        if not f.endswith('.mp4'): continue
        fp = os.path.join(resting_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        dur_s = n_frames / fps
        # sample at mid
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n_frames / 2))
        ret, frame = cap.read()
        if ret:
            res = model.predict(frame, conf=0.25, verbose=False)[0]
            boxes = [b.xyxy[0].tolist() for b in res.boxes]
            confs = [float(b.conf[0]) for b in res.boxes]
            cv2.imwrite(f'scratch/candidates/resting_clip_{f[:10]}.jpg', frame)
            print(f'Resting clip {f} (dur={dur_s:.1f}s): found {len(boxes)} civets, confs={confs}')
        cap.release()

# 3. Check Cam 2 at A02_00.00-05.55
vpath_c2 = 'dataset/ชะมดแผงสันหางดำ/camera 2/A02_00.00-05.55_dur_5h55m.mp4'
if os.path.exists(vpath_c2):
    cap = cv2.VideoCapture(vpath_c2)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    for s in [60, 300, 1800, 3600, 5400]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * fps))
        ret, frame = cap.read()
        if ret:
            res = model.predict(frame, conf=0.25, verbose=False)[0]
            boxes = [b.xyxy[0].tolist() for b in res.boxes]
            confs = [float(b.conf[0]) for b in res.boxes]
            cv2.imwrite(f'scratch/candidates/c2_sec_{s}.jpg', frame)
            print(f'Cam 2 sec {s}: found {len(boxes)} civets, confs={confs}, boxes={boxes}')
    cap.release()
