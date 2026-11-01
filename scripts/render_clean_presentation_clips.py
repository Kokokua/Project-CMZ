import cv2
import os
import shutil
from ultralytics import YOLO

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
model_path = os.path.join(project_root, "models", "yolov8n_civet_multiclass", "weights", "best.pt")
model = YOLO(model_path)

out_dir = os.path.join(project_root, "finish", "demo_clips_clean")
os.makedirs(out_dir, exist_ok=True)

desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file\CMZ project\demo_clips_clean"
os.makedirs(desktop_dir, exist_ok=True)

CLASS_COLORS = {
    0: (234, 179, 8),    # locomotion: Amber / Yellow
    1: (168, 85, 247),   # resting: Purple
    2: (34, 197, 94),    # feeding: Green
    3: (6, 182, 212),    # drinking: Cyan
    4: (236, 72, 153),   # grooming: Pink / Rose
}

CLASS_NAMES = ['locomotion', 'resting', 'feeding', 'drinking', 'grooming']

def draw_clean_tag(img, x1, y1, x2, y2, cls_id, conf, extra_label=""):
    color = CLASS_COLORS.get(cls_id, (0, 255, 0))
    # Sleek modern box: corner brackets or clean rounded rectangle
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
    
    label = f"civet: {CLASS_NAMES[cls_id].upper()} | {conf:.2f}"
    if extra_label:
        label += f" {extra_label}"
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    thickness = 1
    (t_w, t_h), baseline = cv2.getTextSize(label, font, font_scale, thickness)
    
    # Tag badge background
    b_y1 = max(0, y1 - t_h - 10)
    b_y2 = y1
    b_x1 = x1
    b_x2 = min(img.shape[1], x1 + t_w + 14)
    
    cv2.rectangle(img, (b_x1, b_y1), (b_x2, b_y2), (15, 23, 42), -1)
    cv2.rectangle(img, (b_x1, b_y1), (b_x2, b_y2), color, 1, cv2.LINE_AA)
    cv2.putText(img, label, (b_x1 + 7, b_y2 - 6), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

out_w, out_h = 960, 540
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# =========================================================================
# 1. CLEAN CLIP 1: RESTING (Tire Bed Sleep)
# =========================================================================
print("[1/5] Rendering Clean RESTING clip...")
v_rest = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting", "25690519194809256.mp4")
cap1 = cv2.VideoCapture(v_rest)
out_mp4_1 = os.path.join(out_dir, "clean_demo_resting_tire_bed.mp4")
writer1 = cv2.VideoWriter(out_mp4_1, fourcc, 15.0, (out_w, out_h))
poster1 = None

for f_idx in range(6 * 15):
    ret, frame = cap1.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.30, verbose=False)[0]
    
    # Draw tire bed ROI (strictly around tire bed, excluding plant)
    cv2.rectangle(disp, (int(0.42*out_w), int(0.14*out_h)), (int(0.60*out_w), int(0.38*out_h)), (168, 85, 247), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Tire Bed", (int(0.42*out_w)+5, int(0.14*out_h)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (168, 85, 247), 1, cv2.LINE_AA)
    
    for b in res.boxes:
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        # Clip bounding box to tire bed region to avoid overlapping plant leaves
        by2 = min(by2, int(0.37 * out_h))
        by1 = max(by1, int(0.14 * out_h))
        bx1 = max(bx1, int(0.42 * out_w))
        bx2 = min(bx2, int(0.60 * out_w))
        draw_clean_tag(disp, bx1, by1, bx2, by2, int(b.cls[0]), float(b.conf[0]), "")
        break
        
    writer1.write(disp)
    if poster1 is None and f_idx == 30: poster1 = disp.copy()

cap1.release()
writer1.release()
if poster1 is not None:
    cv2.imwrite(os.path.join(out_dir, "clean_demo_resting_tire_bed_poster.jpg"), poster1)
print("  Done Clean RESTING")

# =========================================================================
# 2. CLEAN CLIP 2: FEEDING (Cam 03 Fruit Tray)
# =========================================================================
print("[2/5] Rendering Clean FEEDING clip...")
v_feed = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 1", "A01_15.16-18.55_dur_3h38m.mp4")
cap2 = cv2.VideoCapture(v_feed)
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(1320 * 30))
out_mp4_2 = os.path.join(out_dir, "clean_demo_feeding_fruit_tray.mp4")
writer2 = cv2.VideoWriter(out_mp4_2, fourcc, 15.0, (out_w, out_h))
poster2 = None

for f_idx in range(6 * 15):
    ret, frame = cap2.read()
    cap2.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    # Draw fruit tray ROI
    cv2.rectangle(disp, (int(0.24*out_w), int(0.50*out_h)), (int(0.48*out_w), int(0.85*out_h)), (34, 197, 94), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Fruit Tray", (int(0.24*out_w)+5, int(0.50*out_h)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (34, 197, 94), 1, cv2.LINE_AA)
    
    for b in res.boxes:
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        draw_clean_tag(disp, bx1, by1, bx2, by2, int(b.cls[0]), float(b.conf[0]), "(Fruit Tray)")
        break
        
    writer2.write(disp)
    if poster2 is None and f_idx == 30: poster2 = disp.copy()

cap2.release()
writer2.release()
if poster2 is not None:
    cv2.imwrite(os.path.join(out_dir, "clean_demo_feeding_fruit_tray_poster.jpg"), poster2)
print("  Done Clean FEEDING")

# =========================================================================
# 3. CLEAN CLIP 3: DRINKING (Cam 04 Water Basin @ 04:40:08)
# =========================================================================
print("[3/5] Rendering Clean DRINKING clip...")
v_drink = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")
cap3 = cv2.VideoCapture(v_drink)
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(1335 * 30))
out_mp4_3 = os.path.join(out_dir, "clean_demo_drinking_water_basin.mp4")
writer3 = cv2.VideoWriter(out_mp4_3, fourcc, 15.0, (out_w, out_h))
poster3 = None

for f_idx in range(6 * 15):
    ret, frame = cap3.read()
    cap3.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    # Draw water basin ROI
    cv2.rectangle(disp, (int(0.31*out_w), int(0.48*out_h)), (int(0.44*out_w), int(0.64*out_h)), (6, 182, 212), 1, cv2.LINE_AA)
    cv2.putText(disp, "ROI: Water Basin", (int(0.31*out_w)+5, int(0.48*out_h)-6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (6, 182, 212), 1, cv2.LINE_AA)
    
    drinking_boxes = [b for b in res.boxes if b.xyxy[0][1] > int(0.35*out_h)]
    if drinking_boxes:
        b = max(drinking_boxes, key=lambda x: x.conf[0])
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        draw_clean_tag(disp, bx1, by1, bx2, by2, int(b.cls[0]), float(b.conf[0]), "(Hydration)")
        
    writer3.write(disp)
    if poster3 is None and f_idx == 30: poster3 = disp.copy()

cap3.release()
writer3.release()
if poster3 is not None:
    cv2.imwrite(os.path.join(out_dir, "clean_demo_drinking_water_basin_poster.jpg"), poster3)
print("  Done Clean DRINKING")

# =========================================================================
# 4. CLEAN CLIP 4: GROOMING (Cam 03 Sand Floor Scratching)
# =========================================================================
print("[4/5] Rendering Clean GROOMING clip...")
v_groom = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
cap4 = cv2.VideoCapture(v_groom)
cap4.set(cv2.CAP_PROP_POS_FRAMES, int(5415 * 30))
out_mp4_4 = os.path.join(out_dir, "clean_demo_grooming_sand_floor.mp4")
writer4 = cv2.VideoWriter(out_mp4_4, fourcc, 15.0, (out_w, out_h))
poster4 = None

for f_idx in range(6 * 15):
    ret, frame = cap4.read()
    cap4.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    for b in res.boxes:
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        draw_clean_tag(disp, bx1, by1, bx2, by2, int(b.cls[0]), float(b.conf[0]), "(Self-Scratching)")
        break
        
    writer4.write(disp)
    if poster4 is None and f_idx == 30: poster4 = disp.copy()

cap4.release()
writer4.release()
if poster4 is not None:
    cv2.imwrite(os.path.join(out_dir, "clean_demo_grooming_sand_floor_poster.jpg"), poster4)
print("  Done Clean GROOMING")

# =========================================================================
# 5. CLEAN CLIP 5: LOCOMOTION (Cam 03 Night Patrol)
# =========================================================================
print("[5/5] Rendering Clean LOCOMOTION clip...")
cap5 = cv2.VideoCapture(v_groom)
cap5.set(cv2.CAP_PROP_POS_FRAMES, int(5250 * 30))
out_mp4_5 = os.path.join(out_dir, "clean_demo_locomotion_patrol.mp4")
writer5 = cv2.VideoWriter(out_mp4_5, fourcc, 15.0, (out_w, out_h))
poster5 = None

for f_idx in range(6 * 15):
    ret, frame = cap5.read()
    cap5.read()
    if not ret or frame is None: break
    disp = cv2.resize(frame, (out_w, out_h))
    res = model.predict(disp, conf=0.25, verbose=False)[0]
    
    for b in res.boxes:
        bx1, by1, bx2, by2 = [int(v) for v in b.xyxy[0].tolist()]
        draw_clean_tag(disp, bx1, by1, bx2, by2, int(b.cls[0]), float(b.conf[0]), "(Night Patrol)")
        break
        
    writer5.write(disp)
    if poster5 is None and f_idx == 30: poster5 = disp.copy()

cap5.release()
writer5.release()
if poster5 is not None:
    cv2.imwrite(os.path.join(out_dir, "clean_demo_locomotion_patrol_poster.jpg"), poster5)
print("  Done Clean LOCOMOTION")

# Mirror all clean clips & posters to Desktop CMZ project folder
for f in os.listdir(out_dir):
    src = os.path.join(out_dir, f)
    dst = os.path.join(desktop_dir, f)
    shutil.copy2(src, dst)

print(f"\nSuccessfully rendered and synced all 5 Clean Presentation Clips to:\n{desktop_dir}")
