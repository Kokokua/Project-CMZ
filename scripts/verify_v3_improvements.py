import os
import sys
import cv2
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
v3_weights = os.path.join(project_root, "finish", "models", "yolov8n_civet_v3_best.pt")

if not os.path.exists(v3_weights):
    v3_weights = os.path.join(project_root, "models", "yolov8n_civet_v3", "weights", "best.pt")

assert os.path.exists(v3_weights), f"Model weights not found: {v3_weights}"
print(f"Loading evaluated model: {v3_weights}")
model = YOLO(v3_weights)

print("\n" + "=" * 60)
print("TEST 1: HARD NEGATIVE SUPPRESSION — Cam 01 Empty Tree Stump")
print("=" * 60)
v_cam1 = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 1", "A01_00.00-01.13_dur_1h13m.mp4")
cap1 = cv2.VideoCapture(v_cam1)
cap1.set(cv2.CAP_PROP_POS_FRAMES, 100 * 30)
ret1, f1 = cap1.read()
cap1.release()

r1 = model.predict(f1, conf=0.25, verbose=False)[0]
print(f"Cam 01 Empty Tree Stump detections: {len(r1.boxes)} (Expected: 0)")
for b in r1.boxes:
    print(f"  Ghost Box Detected: conf={float(b.conf[0]):.4f}, xyxy={[int(x) for x in b.xyxy[0].tolist()]}")
stump_clean = (len(r1.boxes) == 0)
print(f"Tree Stump False Positive Eliminated: {stump_clean}")

print("\n" + "=" * 60)
print("TEST 2: TIGHT TIRE BED SLEEP — Cam 03 Curled Civet (No Plant Bleed)")
print("=" * 60)
v_rest = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting", "25690519194809256.mp4")
cap3 = cv2.VideoCapture(v_rest)
cap3.set(cv2.CAP_PROP_POS_FRAMES, 30)
ret3, f3 = cap3.read()
cap3.release()

disp3 = cv2.resize(f3, (960, 540))
r3 = model.predict(disp3, conf=0.20, verbose=False)[0]
print(f"Cam 03 Tire Bed detections: {len(r3.boxes)} (Expected: >= 1)")
tight_box = None
for b in r3.boxes:
    bx1, by1, bx2, by2 = [int(x) for x in b.xyxy[0].tolist()]
    conf = float(b.conf[0])
    print(f"  Civet Box: conf={conf:.4f}, xyxy=[{bx1}, {by1}, {bx2}, {by2}], height={by2-by1}")
    tight_box = (bx1, by1, bx2, by2, conf)

# Render verification crop
if tight_box is not None:
    vis = disp3.copy()
    bx1, by1, bx2, by2, conf = tight_box
    cv2.rectangle(vis, (bx1, by1), (bx2, by2), (168, 85, 247), 2)
    label = f"civet: RESTING | {conf:.2f}"
    cv2.putText(vis, label, (bx1, by1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (168, 85, 247), 1, cv2.LINE_AA)
    out_crop = vis[max(0, by1-40):min(540, by2+60), max(0, bx1-40):min(960, bx2+40)]
    out_p = os.path.join(project_root, "finish", "v3_tire_bed_tight_detection.jpg")
    cv2.imwrite(out_p, out_crop)
    print(f"Visual verification saved to: {out_p}")

print("\n" + "=" * 60)
print("TEST 3: ACTIVE FEEDING — Cam 03 Fruit Tray @ 15:58:39")
print("=" * 60)
v_feed = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_14.03-18.18_dur_4h14m.mp4")
cap_feed = cv2.VideoCapture(v_feed)
cap_feed.set(cv2.CAP_PROP_POS_FRAMES, int((15*3600 + 58*60 + 40 - (14*3600 + 3*60)) * 30))
ret_f, f_feed = cap_feed.read()
cap_feed.release()
if ret_f and f_feed is not None:
    r_feed = model.predict(cv2.resize(f_feed, (960, 540)), conf=0.20, verbose=False)[0]
    print(f"Feeding detection: {len(r_feed.boxes)} civet(s) detected at fruit tray")
    for b in r_feed.boxes:
        print(f"  conf={float(b.conf[0]):.4f}, xyxy={[int(x) for x in b.xyxy[0].tolist()]}")

print("\n" + "=" * 60)
print("VERIFICATION AUDIT COMPLETE")
print("=" * 60)
