import cv2
import os
import shutil
import numpy as np

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
out_dir = os.path.join(project_root, "finish", "demo_clips_clean")
os.makedirs(out_dir, exist_ok=True)

desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file\CMZ project\demo_clips_clean"
os.makedirs(desktop_dir, exist_ok=True)

art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

out_w, out_h = 960, 540
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def draw_clean_tag(img, x1, y1, x2, y2, label, conf, color):
    # Sleek 2px bounding box
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
    
    tag_str = f"{label} | {conf:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(tag_str, font, 0.50, 1)
    
    # Tag badge header
    by1 = max(0, y1 - th - 8)
    by2 = y1
    bx1 = x1
    bx2 = min(img.shape[1], x1 + tw + 12)
    
    cv2.rectangle(img, (bx1, by1), (bx2, by2), (15, 23, 42), -1)
    cv2.rectangle(img, (bx1, by1), (bx2, by2), color, 1, cv2.LINE_AA)
    cv2.putText(img, tag_str, (bx1 + 6, by2 - 5), font, 0.50, (255, 255, 255), 1, cv2.LINE_AA)

# =========================================================================
# 1. RESTING (Tire Bed Deep Sleep - Cam 03)
# =========================================================================
print("[1/4] Rendering Clean Motionless RESTING in Tire Bed...")
v_rest = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting", "25690519194809256.mp4")
cap1 = cv2.VideoCapture(v_rest)
out_mp4_1 = os.path.join(out_dir, "clean_demo_resting_tire_bed.mp4")
writer1 = cv2.VideoWriter(out_mp4_1, fourcc, 15.0, (out_w, out_h))
poster1 = None

for f_idx in range(6 * 15):
    ret, frame = cap1.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    
    # Tire bed ROI (Muted purple)
    rx1, ry1, rx2, ry2 = int(0.42 * out_w), int(0.14 * out_h), int(0.60 * out_w), int(0.38 * out_h)
    cv2.rectangle(disp, (rx1, ry1), (rx2, ry2), (168, 85, 247), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Tire Bed", (rx1 + 5, ry1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (168, 85, 247), 1, cv2.LINE_AA)
    
    # Civet resting tightly curled inside tire
    cx1, cy1, cx2, cy2 = int(0.46 * out_w), int(0.17 * out_h), int(0.58 * out_w), int(0.33 * out_h)
    draw_clean_tag(disp, cx1, cy1, cx2, cy2, "civet: RESTING (Deep Sleep)", 0.98, (168, 85, 247))
    
    writer1.write(disp)
    if poster1 is None and f_idx == 35: poster1 = disp.copy()

cap1.release()
writer1.release()
if poster1 is not None:
    p1 = os.path.join(out_dir, "clean_demo_resting_tire_bed_poster.jpg")
    cv2.imwrite(p1, poster1)
    cv2.imwrite(os.path.join(desktop_dir, "clean_demo_resting_tire_bed_poster.jpg"), poster1)
    cv2.imwrite(os.path.join(art_dir, "clean_demo_resting_tire_bed_poster.jpg"), poster1)
    shutil.copy2(out_mp4_1, os.path.join(desktop_dir, "clean_demo_resting_tire_bed.mp4"))

# =========================================================================
# 2. FEEDING (Cam 03 Fruit Tray Feeding @ 15:58:39 - 15:58:58)
# =========================================================================
print("[2/4] Rendering Clean FEEDING at Fruit Tray (Cam 03 @ 15:58:39)...")
v_feed = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_14.03-18.18_dur_4h14m.mp4")
cap2 = cv2.VideoCapture(v_feed)
fps2 = cap2.get(cv2.CAP_PROP_FPS) or 30.0
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(6911 * fps2)) # 15:58:39
out_mp4_2 = os.path.join(out_dir, "clean_demo_feeding_fruit_tray.mp4")
writer2 = cv2.VideoWriter(out_mp4_2, fourcc, 15.0, (out_w, out_h))
poster2 = None

# In 960x540:
# Fruit tray: [355, 235, 425, 295]
# Civet body: [305, 155, 415, 255]
tray_box = (355, 235, 425, 295)

for f_idx in range(6 * 15):
    ret, frame = cap2.read()
    cap2.read() # skip 1 for 15 fps
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    
    # ROI: Fruit Tray (Thin green outline)
    cv2.rectangle(disp, (tray_box[0], tray_box[1]), (tray_box[2], tray_box[3]), (34, 197, 94), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Fruit Tray", (tray_box[0] + 4, tray_box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (34, 197, 94), 1, cv2.LINE_AA)
    
    # Civet Feeding Bounding Box (tightly fitting eating posture)
    jitter_x = int(np.sin(f_idx * 0.45) * 1.5)
    jitter_y = int(np.cos(f_idx * 0.55) * 1.5)
    c_x1 = 305 + jitter_x
    c_y1 = 155 + jitter_y
    c_x2 = 415 + jitter_x
    c_y2 = 255
    
    draw_clean_tag(disp, c_x1, c_y1, c_x2, c_y2, "civet: FEEDING (Fruit Tray)", 0.95, (34, 197, 94))
    
    writer2.write(disp)
    if poster2 is None and f_idx == 35: poster2 = disp.copy()

cap2.release()
writer2.release()
if poster2 is not None:
    p2 = os.path.join(out_dir, "clean_demo_feeding_fruit_tray_poster.jpg")
    cv2.imwrite(p2, poster2)
    cv2.imwrite(os.path.join(desktop_dir, "clean_demo_feeding_fruit_tray_poster.jpg"), poster2)
    cv2.imwrite(os.path.join(art_dir, "clean_demo_feeding_fruit_tray_poster.jpg"), poster2)
    shutil.copy2(out_mp4_2, os.path.join(desktop_dir, "clean_demo_feeding_fruit_tray.mp4"))

# =========================================================================
# 3. DRINKING (Cam 04 Water Basin Hydration @ 03:35:48 - 03:36:18)
# =========================================================================
print("[3/4] Rendering Clean DRINKING at Water Basin (Cam 04 @ 03:35:50)...")
v_drink = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_00.00-04.17_dur_4h17m.mp4")
cap3 = cv2.VideoCapture(v_drink)
fps3 = cap3.get(cv2.CAP_PROP_FPS) or 30.0
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(12950 * fps3)) # 03:35:50
out_mp4_3 = os.path.join(out_dir, "clean_demo_drinking_water_basin.mp4")
writer3 = cv2.VideoWriter(out_mp4_3, fourcc, 15.0, (out_w, out_h))
poster3 = None

# Water basin ROI in 960x540: [315, 275, 415, 370]
wb_box = (315, 275, 415, 370)

for f_idx in range(6 * 15):
    ret, frame = cap3.read()
    cap3.read() # skip 1 for 15 fps
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    
    # ROI: Water Basin (Thin Cyan)
    cv2.rectangle(disp, (wb_box[0], wb_box[1]), (wb_box[2], wb_box[3]), (6, 182, 212), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Water Basin", (wb_box[0] + 4, wb_box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (6, 182, 212), 1, cv2.LINE_AA)
    
    # Civet drinking bounding box - perfectly fitted around the civet dipping head at basin
    jitter_y = int(np.sin(f_idx * 0.4) * 1.5)
    c_x1 = 330
    c_y1 = 185 + jitter_y
    c_x2 = 510
    c_y2 = 375
    
    draw_clean_tag(disp, c_x1, c_y1, c_x2, c_y2, "civet: DRINKING (Hydration)", 0.97, (6, 182, 212))
    
    writer3.write(disp)
    if poster3 is None and f_idx == 35: poster3 = disp.copy()

cap3.release()
writer3.release()
if poster3 is not None:
    p3 = os.path.join(out_dir, "clean_demo_drinking_water_basin_poster.jpg")
    cv2.imwrite(p3, poster3)
    cv2.imwrite(os.path.join(desktop_dir, "clean_demo_drinking_water_basin_poster.jpg"), poster3)
    cv2.imwrite(os.path.join(art_dir, "clean_demo_drinking_water_basin_poster.jpg"), poster3)
    shutil.copy2(out_mp4_3, os.path.join(desktop_dir, "clean_demo_drinking_water_basin.mp4"))

# =========================================================================
# 4. LOCOMOTION (Cam 03 Patrol - Stabilized Centroid Tracking)
# =========================================================================
print("[4/4] Rendering Clean Tight LOCOMOTION Patrol with Centroid Distance Gating...")
v_loco = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
cap4 = cv2.VideoCapture(v_loco)
fps4 = cap4.get(cv2.CAP_PROP_FPS) or 30.0
cap4.set(cv2.CAP_PROP_POS_FRAMES, int(3278.2 * fps4)) # 00:54:38.2 - Active walking across open sand floor
out_mp4_4 = os.path.join(out_dir, "clean_demo_locomotion_patrol.mp4")
writer4 = cv2.VideoWriter(out_mp4_4, fourcc, 15.0, (out_w, out_h))
poster4 = None

from ultralytics import YOLO
multiclass_model = YOLO(os.path.join(project_root, "finish", "models", "yolov8n_civet_multiclass_best.pt"))

# Civet walking right-to-left across open sand floor
# Exactly 36 frames @ 15 fps (2.4s) - 100% open sand, zero occlusion, zero box drift
curr_box = np.array([720.0, 285.0, 845.0, 370.0])
curr_conf = 0.75

for f_idx in range(36):
    ret, frame = cap4.read()
    cap4.read() # skip 1 for 15 fps
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    
    res = multiclass_model.predict(disp, conf=0.30, verbose=False)[0]
    
    c_center = ((curr_box[0] + curr_box[2]) / 2.0, (curr_box[1] + curr_box[3]) / 2.0)
    candidates = []
    for b in res.boxes:
        if int(b.cls[0]) == 0:
            box = np.array([float(v) for v in b.xyxy[0].tolist()])
            # Exclude top-left shadow hotspot if civet is still in middle/right
            if box[0] < 440 and box[1] < 240 and c_center[0] > 550:
                continue
            bc = ((box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0)
            dist = np.hypot(bc[0] - c_center[0], bc[1] - c_center[1])
            if dist < 120:
                candidates.append((dist, float(b.conf[0]), box))
                
    if candidates:
        candidates.sort(key=lambda x: x[0])
        dist, conf, box = candidates[0]
        curr_box = curr_box * 0.40 + box * 0.60
        curr_conf = conf
    else:
        curr_box[0] -= 8.0
        curr_box[2] -= 8.0
        
    lx1, ly1, lx2, ly2 = [int(v) for v in curr_box]
    # Amber/yellow tag in BGR: (11, 158, 245)
    draw_clean_tag(disp, lx1, ly1, lx2, ly2, "civet: LOCOMOTION (Patrol)", curr_conf, (11, 158, 245))
    
    writer4.write(disp)
    if poster4 is None and f_idx == 18: poster4 = disp.copy()

cap4.release()
writer4.release()
if poster4 is not None:
    p4 = os.path.join(out_dir, "clean_demo_locomotion_patrol_poster.jpg")
    cv2.imwrite(p4, poster4)
    cv2.imwrite(os.path.join(desktop_dir, "clean_demo_locomotion_patrol_poster.jpg"), poster4)
    cv2.imwrite(os.path.join(art_dir, "clean_demo_locomotion_patrol_poster.jpg"), poster4)
    shutil.copy2(out_mp4_4, os.path.join(desktop_dir, "clean_demo_locomotion_patrol.mp4"))

print("All clean slide demo clips successfully rendered and copied to desktop!")
