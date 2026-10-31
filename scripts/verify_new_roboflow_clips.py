import cv2
import os
import sys
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')
model = YOLO('models/yolov8n_civet_phase2/weights/best.pt')

print("=== 1. VERIFYING EATING CLIPS ===")
eating_dir = r"dataset/Eating-20261005T111220Z-1-001/Eating"
for f in sorted(os.listdir(eating_dir)):
    if not f.endswith('.mp4'): continue
    vp = os.path.join(eating_dir, f)
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = total / fps
    
    # Check 5 points
    pts = [int(dur * p) for p in [0.1, 0.3, 0.5, 0.7, 0.9]]
    dets = []
    for s in pts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * fps))
        ret, frame = cap.read()
        if ret:
            res = model.predict(frame, conf=0.25, verbose=False)[0]
            if len(res.boxes) > 0:
                top_b = res.boxes[0]
                dets.append(f"s={s}:conf={float(top_b.conf[0]):.2f}")
    cap.release()
    print(f"File: {f} | dur: {dur:.1f}s | detections: {', '.join(dets) if dets else 'None'}", flush=True)

print("\n=== 2. VERIFYING RESTING CLIPS ===")
resting_dir = r"dataset/Resting-20261005T111307Z-1-001/Resting"
for f in sorted(os.listdir(resting_dir)):
    if not f.endswith('.mp4'): continue
    vp = os.path.join(resting_dir, f)
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur = total / fps
    
    pts = [int(dur * p) for p in [0.1, 0.3, 0.5, 0.7, 0.9]]
    dets = []
    for s in pts:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * fps))
        ret, frame = cap.read()
        if ret:
            res = model.predict(frame, conf=0.25, verbose=False)[0]
            if len(res.boxes) > 0:
                top_b = res.boxes[0]
                dets.append(f"s={s}:conf={float(top_b.conf[0]):.2f}")
    cap.release()
    print(f"File: {f} | dur: {dur:.1f}s | detections: {', '.join(dets) if dets else 'None'}", flush=True)
