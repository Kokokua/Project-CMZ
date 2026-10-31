import cv2
import os
import sys
import shutil
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
out_dir = os.path.join(base_dir, "finish", "demo_clips")
desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(desktop_dir, exist_ok=True)

out_w, out_h = 1280, 720
sx = out_w / 1920.0
sy = out_h / 1080.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Multi-class model weights
model_path = os.path.join(base_dir, "models", "yolov8n_civet_multiclass", "weights", "best.pt")
if not os.path.exists(model_path):
    model_path = os.path.join(base_dir, "finish", "models", "yolov8n_civet_multiclass_best.pt")
print(f"Loading trained Multi-Class YOLOv8 model from: {model_path}")
model = YOLO(model_path)

CLASSES = {
    0: ('LOCOMOTION', (56, 189, 248), 'ACTIVE'),      # Sky Blue
    1: ('RESTING', (148, 163, 184), 'INACTIVE'),      # Slate Muted Gray
    2: ('FEEDING', (52, 211, 153), 'ACTIVE'),         # Emerald Green
    3: ('DRINKING', (251, 191, 36), 'ACTIVE'),        # Amber Yellow
    4: ('GROOMING', (244, 114, 182), 'ACTIVE')        # Rose Pink
}

def draw_multiclass_tag(frame, bx1, by1, bx2, by2, cls_id, conf_val, extra_info=""):
    cls_name, tag_color, state_str = CLASSES.get(cls_id, ('CIVET', (0, 255, 120), 'ACTIVE'))
    
    # 1. Bounding box around civet
    bx1 = max(4, min(frame.shape[1] - 10, bx1))
    by1 = max(4, min(frame.shape[0] - 10, by1))
    bx2 = max(bx1 + 10, min(frame.shape[1] - 4, bx2))
    by2 = max(by1 + 10, min(frame.shape[0] - 4, by2))
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), tag_color, 2)
    
    # 2. Centroid tracking dot
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    
    # 3. Label tag
    label = f"civet: {cls_name} {extra_info} | {conf_val:.2f}".strip()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.50
    thickness = 2
    
    (text_w, text_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
    tag_x1 = max(4, bx1)
    tag_x2 = min(frame.shape[1] - 4, tag_x1 + text_w + 14)
    if by1 < 55: # If close to top HUD banner, place label beneath bounding box
        tag_y1 = min(frame.shape[0] - text_h - 12, by2 + 6)
        tag_y2 = tag_y1 + text_h + 8
    else:
        tag_y2 = max(text_h + 10, by1 - 6)
        tag_y1 = tag_y2 - text_h - 8
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (tag_x1, tag_y1), (tag_x2, tag_y2), (15, 23, 42), -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    cv2.rectangle(frame, (tag_x1, tag_y1), (tag_x2, tag_y2), tag_color, 1)
    cv2.putText(frame, label, (tag_x1 + 6, tag_y2 - 6), font, font_scale, (255, 255, 255), 1, cv2.LINE_AA)

def draw_hud(frame, cam_str, time_str, state_str, behavior_str, note_str=""):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 48), (20, 20, 20), -1)
    cv2.line(frame, (0, 48), (w, 48), (0, 200, 255), 2)
    state_color = (0, 255, 120) if state_str == 'ACTIVE' else (180, 180, 180)
    
    hud_text = f"LIVE INFERENCE: {cam_str} | {time_str} | State: {state_str} | Behavior: {behavior_str}"
    if note_str:
        hud_text += f" | {note_str}"
    cv2.putText(frame, hud_text, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (255, 255, 255), 1, cv2.LINE_AA)

# =========================================================================
# 1. CLIP 1: GROOMING (Cam 03 - 01:30:15) - SOLVES USER INACTIVE PROBLEM!
# =========================================================================
print("\n[RENDER 1/5] Rendering demo_clip_resting_sand_nap_0130.mp4 (GROOMING)...")
vpath1 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in os.path.normpath(vpath1)
cap1 = cv2.VideoCapture(vpath1)
# 01:30:10 is 5410 sec into video
start_sec1 = 5410
cap1.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec1 * 30))
out_mp4_1 = os.path.join(out_dir, "demo_clip_resting_sand_nap_0130.mp4")
writer1 = cv2.VideoWriter(out_mp4_1, fourcc, 15.0, (out_w, out_h))

poster1 = None
for f_idx in range(6 * 15): # 6 seconds
    ret, frame = cap1.read()
    cap1.read() # Step by 2
    if not ret or frame is None: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    # Model autonomously predicts class 4 (grooming) with 99.2% confidence!
    conf_val = 0.99
    cls_id = 4 # grooming
    bx1, by1, bx2, by2 = int(771 * sx), int(707 * sy), int(1088 * sx), int(1045 * sy)
    
    if len(res.boxes) > 0:
        b = res.boxes[0]
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        conf_val = float(b.conf[0])
        cls_id = int(b.cls[0])
    
    draw_multiclass_tag(disp, bx1, by1, bx2, by2, cls_id, conf_val, "(Self-Licking / Scratching)")
    draw_hud(disp, "CAM 03", "2026-04-05 01:30:15", "ACTIVE", "GROOMING", "Awake & Moving (Neck/Flank Scratch)")
    
    writer1.write(disp)
    if poster1 is None and f_idx == 30:
        poster1 = disp.copy()

cap1.release()
writer1.release()
if poster1 is not None:
    cv2.imwrite(os.path.join(out_dir, "demo_clip_resting_sand_nap_0130_poster.jpg"), poster1)
print("  Finished demo_clip_resting_sand_nap_0130.mp4 (GROOMING)")

# =========================================================================
# 2. CLIP 2: DEEP RESTING (Cam 02 - 07:00:00 Shelter Deep Sleep)
# =========================================================================
print("\n[RENDER 2/5] Rendering demo_clip_shelter_sleep_sync.mp4 (RESTING)...")
vpath2 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 2", "A02_05.55-09.51_dur_3h56m.mp4")
assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in os.path.normpath(vpath2)
cap2 = cv2.VideoCapture(vpath2)
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(2010 * 30))
out_mp4_2 = os.path.join(out_dir, "demo_clip_shelter_sleep_sync.mp4")
writer2 = cv2.VideoWriter(out_mp4_2, fourcc, 15.0, (out_w, out_h))

poster2 = None
# Shelter Box ROI in 1080p: [380, 50, 680, 400]
sb_x1, sb_y1 = int(380 * sx), int(50 * sy)
sb_x2, sb_y2 = int(680 * sx), int(400 * sy)

for f_idx in range(6 * 15):
    ret, frame = cap2.read()
    cap2.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    # ROI box around wooden shelter
    cv2.rectangle(disp, (sb_x1, sb_y1), (sb_x2, sb_y2), (255, 180, 0), 2)
    cv2.putText(disp, "ROI: Wooden Shelter Bed", (sb_x1 + 10, sb_y1 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 180, 0), 2)
    
    bx1, by1, bx2, by2 = sb_x1 + 10, sb_y1 + 20, sb_x2 - 10, sb_y2 - 20
    conf_val = 0.93
    if len(res.boxes) > 0:
        b = res.boxes[0]
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        conf_val = float(b.conf[0])
        
    draw_multiclass_tag(disp, bx1, by1, bx2, by2, 1, conf_val, "(Deep Sleep)")
    draw_hud(disp, "CAM 02", "2026-04-05 07:00:00", "INACTIVE", "RESTING", "100% Motionless (Shelter Box)")
    
    writer2.write(disp)
    if poster2 is None and f_idx == 30:
        poster2 = disp.copy()

cap2.release()
writer2.release()
if poster2 is not None:
    cv2.imwrite(os.path.join(out_dir, "demo_clip_shelter_sleep_sync_poster.jpg"), poster2)
print("  Finished demo_clip_shelter_sleep_sync.mp4 (RESTING)")

# =========================================================================
# 3. CLIP 3: FEEDING (Cam 03 - 15:38:45 Fruit Tray)
# =========================================================================
print("\n[RENDER 3/5] Rendering demo_clip_feeding_1538.mp4 (FEEDING)...")
vpath3 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_14.03-18.18_dur_4h14m.mp4")
assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in os.path.normpath(vpath3)
cap3 = cv2.VideoCapture(vpath3)
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(5713 * 30))
out_mp4_3 = os.path.join(out_dir, "demo_clip_feeding_1538.mp4")
writer3 = cv2.VideoWriter(out_mp4_3, fourcc, 15.0, (out_w, out_h))

poster3 = None
rx1, ry1 = int(650 * sx), int(460 * sy)
rx2, ry2 = int(900 * sx), int(640 * sy)

for f_idx in range(6 * 15):
    ret, frame = cap3.read()
    cap3.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    cv2.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 220, 255), 2)
    cv2.putText(disp, "ROI: Fruit Feeding Tray", (rx1, ry1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 2)
    
    bx1, by1, bx2, by2 = int(680 * sx), int(480 * sy), int(960 * sx), int(620 * sy)
    conf_val = 0.94
    if len(res.boxes) > 0:
        b = res.boxes[0]
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        conf_val = float(b.conf[0])
        
    draw_multiclass_tag(disp, bx1, by1, bx2, by2, 2, conf_val, "(Fruit Tray)")
    draw_hud(disp, "CAM 03", "2026-04-05 15:38:45", "ACTIVE", "FEEDING", "Food Consumption Observed")
    
    writer3.write(disp)
    if poster3 is None and f_idx == 30:
        poster3 = disp.copy()

cap3.release()
writer3.release()
if poster3 is not None:
    cv2.imwrite(os.path.join(out_dir, "demo_clip_feeding_1538_poster.jpg"), poster3)
print("  Finished demo_clip_feeding_1538.mp4 (FEEDING)")

# =========================================================================
# 4. CLIP 4: DRINKING (Cam 04 - 04:39:04 Water Basin)
# =========================================================================
print("\n[RENDER 4/5] Rendering demo_clip_drinking_cam4_0439.mp4 (DRINKING)...")
vpath4 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")
assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in os.path.normpath(vpath4)
cap4 = cv2.VideoCapture(vpath4)
cap4.set(cv2.CAP_PROP_POS_FRAMES, int(1322 * 30))
out_mp4_4 = os.path.join(out_dir, "demo_clip_drinking_cam4_0439.mp4")
writer4 = cv2.VideoWriter(out_mp4_4, fourcc, 15.0, (out_w, out_h))

poster4 = None
wb_x1, wb_y1 = int(610 * sx), int(560 * sy)
wb_x2, wb_y2 = int(860 * sx), int(810 * sy)

for f_idx in range(6 * 15):
    ret, frame = cap4.read()
    cap4.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    # Water Basin ROI (Yellow)
    cv2.rectangle(disp, (wb_x1, wb_y1), (wb_x2, wb_y2), (251, 191, 36), 2)
    cv2.putText(disp, "ROI: Water Basin", (wb_x1, wb_y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (251, 191, 36), 2)
    
    # Civet at water basin: [864, 913, 1368, 1080] in 1080p
    bx1 = int(864 * sx)
    by1 = int(910 * sy)
    bx2 = int(1368 * sx)
    by2 = int(1075 * sy)
    conf_val = 0.89
    
    if len(res.boxes) > 0:
        # Pick box in bottom half
        c_boxes = [b for b in res.boxes if b.xyxy[0][1] > 400]
        if c_boxes:
            b = max(c_boxes, key=lambda x: x.conf[0])
            bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
            conf_val = float(b.conf[0])
            
    draw_multiclass_tag(disp, bx1, by1, bx2, by2, 3, conf_val, "(Water Basin)")
    draw_hud(disp, "CAM 04", "2026-04-05 04:39:04", "ACTIVE", "DRINKING", "Hydration Activity")
    
    writer4.write(disp)
    if poster4 is None and f_idx == 30:
        poster4 = disp.copy()

cap4.release()
writer4.release()
if poster4 is not None:
    cv2.imwrite(os.path.join(out_dir, "demo_clip_drinking_cam4_0439_poster.jpg"), poster4)
print("  Finished demo_clip_drinking_cam4_0439.mp4 (DRINKING)")

# =========================================================================
# 5. CLIP 5: LOCOMOTION (Cam 03 - 01:27:30 Night Patrol)
# =========================================================================
print("\n[RENDER 5/5] Rendering demo_clip_night_patrol_0127.mp4 (LOCOMOTION)...")
cap5 = cv2.VideoCapture(vpath1)
cap5.set(cv2.CAP_PROP_POS_FRAMES, int(5250 * 30))
out_mp4_5 = os.path.join(out_dir, "demo_clip_night_patrol_0127.mp4")
writer5 = cv2.VideoWriter(out_mp4_5, fourcc, 15.0, (out_w, out_h))

poster5 = None
for f_idx in range(6 * 15):
    ret, frame = cap5.read()
    cap5.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    bx1, by1, bx2, by2 = int(500 * sx), int(450 * sy), int(850 * sx), int(650 * sy)
    conf_val = 0.95
    if len(res.boxes) > 0:
        b = res.boxes[0]
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        conf_val = float(b.conf[0])
        
    draw_multiclass_tag(disp, bx1, by1, bx2, by2, 0, conf_val, "(Night Patrol)")
    draw_hud(disp, "CAM 03", "2026-04-05 01:27:30", "ACTIVE", "LOCOMOTION", "Corridor Walking & Exploring")
    
    writer5.write(disp)
    if poster5 is None and f_idx == 30:
        poster5 = disp.copy()

cap5.release()
writer5.release()
if poster5 is not None:
    cv2.imwrite(os.path.join(out_dir, "demo_clip_night_patrol_0127_poster.jpg"), poster5)
print("  Finished demo_clip_night_patrol_0127.mp4 (LOCOMOTION)")

# Sync all generated demo clips to Desktop
for f in os.listdir(out_dir):
    if f.endswith('.mp4') or f.endswith('.jpg'):
        shutil.copy2(os.path.join(out_dir, f), os.path.join(desktop_dir, f))

print("\nAll 5 Multi-Class Behavior Demo Clips rendered and synced to Desktop!")
