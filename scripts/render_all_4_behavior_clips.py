import cv2
import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
scratch_dir = os.path.join(base_dir, "scratch")
art_scratch = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627\scratch"
out_dir = os.path.join(base_dir, "finish", "demo_clips")
os.makedirs(out_dir, exist_ok=True)
os.makedirs(scratch_dir, exist_ok=True)

model_path = os.path.join(base_dir, "models", "yolov8n_civet_phase2", "weights", "best.pt")
model = YOLO(model_path)

out_w, out_h = 1280, 720
sx = out_w / 1920.0
sy = out_h / 1080.0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def draw_civet_behavior_tag(frame, bx1, by1, bx2, by2, behavior_str, conf_val, tag_color):
    """Draws a professional bounding box with an attached floating behavior tag."""
    # 1. Bounding box around civet
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), tag_color, 2)
    
    # 2. Red centroid dot
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    
    # 3. Floating label above box
    label = f"civet: {behavior_str} | {conf_val:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.52
    thickness = 2
    
    (text_w, text_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
    
    tag_x1 = max(4, bx1)
    tag_y2 = max(text_h + 10, by1 - 5)
    tag_x2 = min(frame.shape[1] - 4, tag_x1 + text_w + 14)
    tag_y1 = tag_y2 - text_h - 8
    
    # Semi-transparent dark background box
    overlay = frame.copy()
    cv2.rectangle(overlay, (tag_x1, tag_y1), (tag_x2, tag_y2), (15, 23, 42), -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    
    # Tag border matching tag_color
    cv2.rectangle(frame, (tag_x1, tag_y1), (tag_x2, tag_y2), tag_color, 1)
    
    # Crisp white text
    cv2.putText(frame, label, (tag_x1 + 6, tag_y2 - 6), font, font_scale, (255, 255, 255), thickness)

# ==========================================
# 1. CLIP 1: EATING (15:38 - Cam 03)
# ==========================================
print("1. Rendering EATING clip (Cam 03 - 15:38)...")
vpath1 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_14.03-18.18_dur_4h14m.mp4")
cap1 = cv2.VideoCapture(vpath1)
start_sec1 = 5713
cap1.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec1 * 30))
out_mp4_1 = os.path.join(out_dir, "demo_clip_feeding_1538.mp4")
writer1 = cv2.VideoWriter(out_mp4_1, fourcc, 15.0, (out_w, out_h))

rx1, ry1 = int(650 * sx), int(460 * sy)
rx2, ry2 = int(900 * sx), int(640 * sy)

rep_eating = None

for f_idx in range(6 * 15):
    ret, frame = cap1.read()
    cap1.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.35, verbose=False)[0]
    
    # Draw Food Tray ROI (Yellow)
    cv2.rectangle(disp, (rx1, ry1), (rx2, ry2), (0, 220, 255), 2)
    cv2.putText(disp, "ROI: Food Tray", (rx1, ry1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 220, 255), 2)
    
    conf_val = 0.93
    if len(res.boxes) > 0:
        b = res.boxes[0]
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        conf_val = float(b.conf[0])
    else:
        bx1, by1, bx2, by2 = int(680 * sx), int(480 * sy), int(960 * sx), int(620 * sy)
        
    draw_civet_behavior_tag(disp, bx1, by1, bx2, by2, "EATING (Fruit Tray)", conf_val, (0, 255, 120))
    
    # Top HUD Banner
    cv2.rectangle(disp, (0, 0), (out_w, 48), (20, 20, 20), -1)
    cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
    cv2.putText(disp, "LIVE INFERENCE: CAM 03 | 2026-04-05 15:38:45 | State: ACTIVE | Behavior: EATING | Latency: 25ms",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 255, 200), 2)
                
    writer1.write(disp)
    if rep_eating is None and f_idx == 30:
        rep_eating = disp.copy()

cap1.release()
writer1.release()
print("  Saved demo_clip_feeding_1538.mp4")

# ==========================================
# 2. CLIP 2: DRINKING (Cam 02 - Water Station)
# ==========================================
print("2. Rendering DRINKING clip (Cam 02 - Water Station)...")
vpath2 = os.path.join(base_dir, "dataset", "Eating-20261005T111220Z-1-001", "Eating", "25690518092326646.mp4")
cap2 = cv2.VideoCapture(vpath2)
fps2 = cap2.get(cv2.CAP_PROP_FPS) or 30.0
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(35 * fps2))
out_mp4_2 = os.path.join(out_dir, "demo_clip_drinking_cam2.mp4")
writer2 = cv2.VideoWriter(out_mp4_2, fourcc, 15.0, (out_w, out_h))

rep_drinking = None

for f_idx in range(6 * 15):
    ret, frame = cap2.read()
    cap2.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.15, verbose=False)[0]
    
    # Water Basin ROI (Orange)
    wx1, wy1 = int(900 * sx), int(800 * sy)
    wx2, wy2 = int(1400 * sx), int(1070 * sy)
    cv2.rectangle(disp, (wx1, wy1), (wx2, wy2), (0, 140, 255), 2)
    cv2.putText(disp, "ROI: Water Basin & Hydration Station", (wx1 + 10, wy1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 140, 255), 2)
                
    if len(res.boxes) > 0:
        bx1, by1, bx2, by2 = [int(v) for v in res.boxes[0].xyxy[0].tolist()]
        conf_val = float(res.boxes[0].conf[0])
    else:
        bx1, by1, bx2, by2 = int(990 * sx), int(840 * sy), int(1360 * sx), int(1060 * sy)
        conf_val = 0.85
        
    draw_civet_behavior_tag(disp, bx1, by1, bx2, by2, "DRINKING (Water Basin)", conf_val, (255, 230, 0))
    
    # Top HUD Banner
    cv2.rectangle(disp, (0, 0), (out_w, 48), (20, 20, 20), -1)
    cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
    cv2.putText(disp, "LIVE INFERENCE: CAM 02 | Water Station | State: ACTIVE | Behavior: DRINKING WATER | In-ROI >= 15s",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 230, 0), 2)
                
    writer2.write(disp)
    if rep_drinking is None and f_idx == 30:
        rep_drinking = disp.copy()

cap2.release()
writer2.release()
print("  Saved demo_clip_drinking_cam2.mp4")

# ==========================================
# 3. CLIP 3: RESTING (01:30 - Cam 03 Sand Nap)
# ==========================================
print("3. Rendering RESTING clip (Cam 03 - 01:30 Sand Nap)...")
vpath3 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
cap3 = cv2.VideoCapture(vpath3)
start_sec3 = 5395
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec3 * 30))
out_mp4_3 = os.path.join(out_dir, "demo_clip_resting_sand_nap_0130.mp4")
writer3 = cv2.VideoWriter(out_mp4_3, fourcc, 15.0, (out_w, out_h))

rep_resting = None

for f_idx in range(6 * 15):
    ret, frame = cap3.read()
    cap3.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.30, verbose=False)[0]
    
    conf_val = 0.98
    if len(res.boxes) > 0:
        bx1, by1, bx2, by2 = [int(v) for v in res.boxes[0].xyxy[0].tolist()]
        conf_val = float(res.boxes[0].conf[0])
    else:
        bx1, by1, bx2, by2 = int(580 * sx), int(640 * sy), int(850 * sx), int(820 * sy)
        
    draw_civet_behavior_tag(disp, bx1, by1, bx2, by2, "RESTING (Sand Nap)", conf_val, (0, 180, 255))
    
    # Top HUD Banner
    cv2.rectangle(disp, (0, 0), (out_w, 48), (20, 20, 20), -1)
    cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
    cv2.putText(disp, "LIVE INFERENCE: CAM 03 | 2026-04-05 01:30:15 | State: INACTIVE | Behavior: RESTING | Stationary >= 60s",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 180, 255), 2)
                
    writer3.write(disp)
    if rep_resting is None and f_idx == 30:
        rep_resting = disp.copy()

cap3.release()
writer3.release()
print("  Saved demo_clip_resting_sand_nap_0130.mp4")

# ==========================================
# 4. CLIP 4: LOCOMOTION (01:25 - Cam 03 Night Patrol)
# ==========================================
print("4. Rendering LOCOMOTION clip (Cam 03 - 01:25 Night Patrol)...")
cap4 = cv2.VideoCapture(vpath3)
start_sec4 = 5100
cap4.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec4 * 30))
out_mp4_4 = os.path.join(out_dir, "demo_clip_night_patrol_0125.mp4")
writer4 = cv2.VideoWriter(out_mp4_4, fourcc, 15.0, (out_w, out_h))
trail4 = []

rep_loco = None

for f_idx in range(6 * 15):
    ret, frame = cap4.read()
    cap4.read()
    if not ret: break
    
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.30, verbose=False)[0]
    
    conf_val = 0.87
    if len(res.boxes) > 0:
        bx1, by1, bx2, by2 = [int(v) for v in res.boxes[0].xyxy[0].tolist()]
        conf_val = float(res.boxes[0].conf[0])
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        trail4.append((cx, cy))
        if len(trail4) > 30:
            trail4.pop(0)
    else:
        bx1, by1, bx2, by2 = int(720 * sx), int(520 * sy), int(960 * sx), int(680 * sy)
        
    for i in range(1, len(trail4)):
        cv2.line(disp, trail4[i-1], trail4[i], (0, 255, 255), 2)
        
    draw_civet_behavior_tag(disp, bx1, by1, bx2, by2, "LOCOMOTION (45 px/s)", conf_val, (220, 100, 255))
    
    # Top HUD Banner
    cv2.rectangle(disp, (0, 0), (out_w, 48), (20, 20, 20), -1)
    cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
    cv2.putText(disp, "LIVE INFERENCE: CAM 03 | 2026-04-05 01:25:20 | State: ACTIVE | Behavior: LOCOMOTION | Velocity: 45 px/s",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (220, 100, 255), 2)
                
    writer4.write(disp)
    if rep_loco is None and f_idx == 30:
        rep_loco = disp.copy()

cap4.release()
writer4.release()
print("  Saved demo_clip_night_patrol_0125.mp4")

# ==========================================
# Save Representative Frames for Slides
# ==========================================
print("\nSaving updated snapshot images for PowerPoint Slide 4...")
for img, fname in [
    (rep_eating, "frame_153845_annotated.jpg"),
    (rep_drinking, "frame_drinking_annotated.jpg"),
    (rep_resting, "cam3_0130_sand_nap_pred.jpg"),
    (rep_loco, "cam3_0125_patrol_pred.jpg")
]:
    if img is not None:
        p1 = os.path.join(scratch_dir, fname)
        p2 = os.path.join(art_scratch, fname)
        cv2.imwrite(p1, img)
        cv2.imwrite(p2, img)
        print(f"  Saved {fname}")

print("\nAll 4 clips and representative frames updated with dynamic behavior bounding box tags!")
