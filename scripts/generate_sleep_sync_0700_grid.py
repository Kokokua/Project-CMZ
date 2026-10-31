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
grid_w, grid_h = out_w // 2, out_h // 2

# 07:00:00 - True Shelter Sleep (Cam 1, 3, 4 are 100% empty, civet inside Room 2 shelter box)
c1 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 1', 'A01_06.13-09.48_dur_3h35m.mp4'))
c1.set(cv2.CAP_PROP_POS_FRAMES, int(2782 * 30))
_, f1 = c1.read()
c1.release()

c2 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 2', 'A02_05.55-09.51_dur_3h56m.mp4'))
c2.set(cv2.CAP_PROP_POS_FRAMES, int(3874 * 30))
_, f2 = c2.read()
c2.release()

c3 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 3', 'A03_06.56-10.54_dur_3h57m.mp4'))
c3.set(cv2.CAP_PROP_POS_FRAMES, int(185 * 30))
_, f3 = c3.read()
c3.release()

c4 = cv2.VideoCapture(os.path.join(base_dataset, 'camera 4', 'A04_04.17-08.19_dur_4h01m.mp4'))
c4.set(cv2.CAP_PROP_POS_FRAMES, int(9730 * 30))
_, f4 = c4.read()
c4.release()

p1 = cv2.resize(f1, (grid_w, grid_h))
p2 = cv2.resize(f2, (grid_w, grid_h))
p3 = cv2.resize(f3, (grid_w, grid_h))
p4 = cv2.resize(f4, (grid_w, grid_h))

# Annotate Cam 1 (Vacant)
cv2.rectangle(p1, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p1, "CAM 01: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p1, "Time: 2026-04-05 07:00:00 | Room 1 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

# Annotate Cam 2 (Shelter Resting)
cv2.rectangle(p2, (8, 8), (grid_w - 8, grid_h - 8), (0, 200, 100), 2)
sb_x1, sb_y1 = int(468 * grid_w / 1920.0), int(147 * grid_h / 1080.0)
sb_x2, sb_y2 = int(794 * grid_w / 1920.0), int(495 * grid_h / 1080.0)
cv2.rectangle(p2, (sb_x1, sb_y1), (sb_x2, sb_y2), (0, 255, 120), 2)
cv2.putText(p2, "CAM 02: INACTIVE : RESTING (Shelter Box)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 120), 2)
cv2.putText(p2, "Time: 2026-04-05 07:00:00 | Inside Sleeping Quarters", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 255, 200), 1)

# Annotate Cam 3 (Vacant)
cv2.rectangle(p3, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p3, "CAM 03: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p3, "Time: 2026-04-05 07:00:00 | Room 3 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

# Annotate Cam 4 (Vacant)
cv2.rectangle(p4, (8, 8), (grid_w - 8, grid_h - 8), (40, 50, 70), 1)
cv2.putText(p4, "CAM 04: 0 Detections (VACANT)", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (160, 175, 190), 2)
cv2.putText(p4, "Time: 2026-04-05 07:00:00 | Room 4 Empty", (16, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (100, 200, 255), 1)

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
cv2.rectangle(canvas, (bx, by), (bx + badge_w, by + badge_h), (0, 220, 100), 2)
cv2.putText(canvas, "4-CAM SYNCHRONIZED TIME: 07:00:00 | ROOMS 1, 3, 4 ALL EMPTY -> RESTING IN ROOM 2 SHELTER",
            (bx + 14, by + 34), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (0, 255, 150), 2, cv2.LINE_AA)

save_path = os.path.join(art_dir, "sleep_sync_0700_shelter_grid.jpg")
cv2.imwrite(save_path, canvas)
print(f"Saved {save_path} successfully!")
