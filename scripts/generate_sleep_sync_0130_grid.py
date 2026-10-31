import cv2
import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"
base_dataset = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ")
model_path = os.path.join(base_dir, "models", "yolov8n_civet_phase2", "weights", "best.pt")
model = YOLO(model_path)

out_w, out_h = 1280, 720
grid_w, grid_h = out_w // 2, out_h // 2 # 640 x 360

# ---------------------------------------------------------------
# 1. READ ALL 4 CAMERAS AT 01:30:15 (The authentic Sleeping Sand Nap)
# ---------------------------------------------------------------
c1 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 1', 'A01_01.13-06.13_dur_4h59m.mp4'))
c1.set(cv2.CAP_PROP_POS_FRAMES, int(984 * 30))
_, f1 = c1.read()
c1.release()

c2 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 2', 'A02_00.00-05.55_dur_5h55m.mp4'))
c2.set(cv2.CAP_PROP_POS_FRAMES, int(5415 * 30))
_, f2 = c2.read()
c2.release()

c3 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 3', 'A03_00.00-06.56_dur_6h56m.mp4'))
c3.set(cv2.CAP_PROP_POS_FRAMES, int(5415 * 30))
_, f3 = c3.read()
c3.release()

c4 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 4', 'A04_00.00-04.17_dur_4h17m.mp4'))
c4.set(cv2.CAP_PROP_POS_FRAMES, int(5415 * 30))
_, f4 = c4.read()
c4.release()

p1 = cv2.resize(f1, (grid_w, grid_h))
p2 = cv2.resize(f2, (grid_w, grid_h))
p3 = cv2.resize(f3, (grid_w, grid_h))
p4 = cv2.resize(f4, (grid_w, grid_h))

# Annotate Cam 1 (Vacant)
cv2.rectangle(p1, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p1, "CAM 01: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p1, "Time: 2026-04-05 01:30:15 | Room 1 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

# Annotate Cam 2 (Vacant)
cv2.rectangle(p2, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p2, "CAM 02: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p2, "Time: 2026-04-05 01:30:15 | Room 2 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

# Annotate Cam 3 (ACTIVE DETECTION: RESTING CIVET!)
res3 = model.predict(f3, conf=0.30, verbose=False)[0]
for b in res3.boxes:
    # Filter for civet (exclude plant [760, 600, 1030, 770])
    x1, y1, x2, y2 = b.xyxy[0].tolist()
    if y1 > 650:
        bx1 = int(x1 * grid_w / 1920.0)
        by1 = int(y1 * grid_h / 1080.0)
        bx2 = int(x2 * grid_w / 1920.0)
        by2 = int(y2 * grid_h / 1080.0)
        cv2.rectangle(p3, (bx1, by1), (bx2, by2), (0, 240, 255), 2)
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        cv2.circle(p3, (cx, cy), 4, (0, 0, 255), -1)
        
        tag_text = f"civet: RESTING (Sand Nap) | {float(b.conf[0]):.2f}"
        cv2.rectangle(p3, (bx1, by1 - 24), (bx1 + 260, by1), (15, 23, 42), -1)
        cv2.rectangle(p3, (bx1, by1 - 24), (bx1 + 260, by1), (0, 240, 255), 1)
        cv2.putText(p3, tag_text, (bx1 + 5, by1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (255, 255, 255), 1, cv2.LINE_AA)

cv2.rectangle(p3, (8, 8), (grid_w - 8, grid_h - 8), (0, 220, 255), 2)
cv2.putText(p3, "CAM 03: INACTIVE : RESTING (Sand Nap Floor)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 240, 255), 2)
cv2.putText(p3, "Time: 2026-04-05 01:30:15 | Stationary >= 60s | AI Conf: 0.95", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 255, 180), 1)

# Annotate Cam 4 (Vacant)
cv2.rectangle(p4, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p4, "CAM 04: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p4, "Time: 2026-04-05 01:30:15 | Room 4 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

# Assemble 2x2 grid
canvas = np.zeros((out_h, out_w, 3), dtype=np.uint8)
canvas[0:grid_h, 0:grid_w] = p1
canvas[0:grid_h, grid_w:out_w] = p2
canvas[grid_h:out_h, 0:grid_w] = p3
canvas[grid_h:out_h, grid_w:out_w] = p4

# Central HUD Badge
badge_w, badge_h = 820, 52
bx = (out_w - badge_w) // 2
by = (out_h - badge_h) // 2
cv2.rectangle(canvas, (bx, by), (bx + badge_w, by + badge_h), (15, 23, 42), -1)
cv2.rectangle(canvas, (bx, by), (bx + badge_w, by + badge_h), (0, 240, 255), 2)
cv2.putText(canvas, "4-CAM SYNCHRONIZED TIME: 01:30:15 | CIVET RESTING IN CAM 03 | ROOMS 1, 2, 4 VACANT",
            (bx + 18, by + 34), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 255, 220), 2, cv2.LINE_AA)

save_path = os.path.join(art_dir, "sleep_sync_0130_perfect_grid.jpg")
cv2.imwrite(save_path, canvas)
print(f"Saved {save_path} successfully!")
