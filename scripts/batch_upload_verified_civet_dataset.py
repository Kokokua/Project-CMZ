import os
import sys
import time
import cv2
from ultralytics import YOLO
from roboflow import Roboflow

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
backup_dir = os.path.join(project_root, "dataset", "roboflow_backup")
img_backup_dir = os.path.join(backup_dir, "images")
lbl_backup_dir = os.path.join(backup_dir, "labels")

os.makedirs(img_backup_dir, exist_ok=True)
os.makedirs(lbl_backup_dir, exist_ok=True)

# 1. Connect to Roboflow
API_KEY = "Dbsq4wpnTVr9UkRb7YBj"
WORKSPACE = "mes-workspace-02uvi"
PROJECT_ID = "civet-monitoring"

print("==================================================================")
print("1. CONNECTING TO ROBOFLOW...")
print(f"Workspace: {WORKSPACE} | Project: {PROJECT_ID}")
print("==================================================================")

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT_ID)
print(f"Successfully connected to project: '{project.name}'")

# 2. Load Local YOLO Model for Pre-Annotation Verification
model_path = os.path.join(project_root, "models", "yolov8n_civet_phase2", "weights", "best.pt")
print(f"Loading pre-annotation model from: {model_path}")
model = YOLO(model_path)

# 3. Define Sources of 100% Genuine Civet Video Clips
sources = [
    {
        "category": "day_eating",
        "video": os.path.join(project_root, "dataset", "robo", "04_civet_eating_fruit_tray_peak_day.mp4"),
        "target_count": 20,
        "min_conf": 0.80
    },
    {
        "category": "day_resting_shelf",
        "video": os.path.join(project_root, "dataset", "robo", "03_civet_resting_shelf_day.mp4"),
        "target_count": 20,
        "min_conf": 0.90
    },
    {
        "category": "night_resting_sand",
        "video": os.path.join(project_root, "dataset", "robo", "03_civet_resting_sand_nap_night_ir.mp4"),
        "target_count": 20,
        "min_conf": 0.90
    },
    {
        "category": "night_locomotion_patrol",
        "video": os.path.join(project_root, "dataset", "robo", "02_civet_locomotion_night_ir.mp4"),
        "target_count": 15,
        "min_conf": 0.50
    },
    {
        "category": "day_eating_tray_start",
        "video": os.path.join(project_root, "dataset", "robo", "01_civet_eating_fruit_tray_day.mp4"),
        "target_count": 15,
        "min_conf": 0.70
    }
]

# 4. Extract, Pre-Annotate, and Save to Local Backup
extracted_items = []
total_target = sum(s["target_count"] for s in sources)
print(f"\nTargeting ~{total_target} verified civet frames across 5 behavioral categories...")

frame_global_id = 1

for src in sources:
    vpath = src["video"]
    cat = src["category"]
    need_count = src["target_count"]
    min_c = src["min_conf"]
    
    if not os.path.exists(vpath):
        print(f"[WARN] Video not found: {vpath}")
        continue
        
    cap = cv2.VideoCapture(vpath)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_f = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_s = total_f / fps
    
    print(f"\nProcessing: {cat} ({os.path.basename(vpath)}) - Duration {dur_s:.1f}s")
    
    step_s = max(0.5, (dur_s - 2.0) / float(need_count))
    found_in_src = 0
    cur_s = 1.0
    
    while found_in_src < need_count and cur_s < (dur_s - 1.0):
        f_idx = int(cur_s * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, frame = cap.read()
        cur_s += step_s
        
        if not ret:
            continue
            
        res = model.predict(frame, conf=min_c, verbose=False)[0]
        if len(res.boxes) == 0:
            continue
            
        top_box = res.boxes[0]
        conf_val = float(top_box.conf[0])
        h_img, w_img = frame.shape[:2]
        
        # YOLO normalized bounding box format: class x_center y_center width height
        x1, y1, x2, y2 = top_box.xyxy[0].tolist()
        bw = (x2 - x1) / float(w_img)
        bh = (y2 - y1) / float(h_img)
        bcx = (x1 + x2) / 2.0 / float(w_img)
        bcy = (y1 + y2) / 2.0 / float(h_img)
        
        # Deterministic 70% Train, 20% Valid, 10% Test
        split_idx = (frame_global_id - 1) % 10
        if split_idx < 7:
            split_type = "train"
        elif split_idx < 9:
            split_type = "valid"
        else:
            split_type = "test"
            
        fname_base = f"civet_{frame_global_id:03d}_{cat}_{int(cur_s)}s"
        img_name = f"{fname_base}.jpg"
        lbl_name = f"{fname_base}.txt"
        
        img_full_path = os.path.join(img_backup_dir, img_name)
        lbl_full_path = os.path.join(lbl_backup_dir, lbl_name)
        
        # Save image
        cv2.imwrite(img_full_path, frame)
        
        # Save YOLO annotation (class 0 = civet)
        with open(lbl_full_path, "w", encoding="utf-8") as f_lbl:
            f_lbl.write(f"0 {bcx:.6f} {bcy:.6f} {bw:.6f} {bh:.6f}\n")
            
        extracted_items.append({
            "img_path": img_full_path,
            "lbl_path": lbl_full_path,
            "category": cat,
            "conf": round(conf_val, 2),
            "split": split_type
        })
        
        found_in_src += 1
        frame_global_id += 1
        
    cap.release()
    print(f"  Extracted {found_in_src}/{need_count} verified civet frames for {cat}")

print(f"\nTotal verified frames extracted and pre-annotated: {len(extracted_items)}")
print(f"Local backup saved at: {backup_dir}")

# 5. Batch Upload to Roboflow
print("\n==================================================================")
print(f"STARTING BATCH UPLOAD TO ROBOFLOW (Total: {len(extracted_items)} Images)")
print("==================================================================")

t_start = time.time()
uploaded_count = 0
failed_count = 0

train_count = sum(1 for it in extracted_items if it["split"] == "train")
valid_count = sum(1 for it in extracted_items if it["split"] == "valid")
test_count = sum(1 for it in extracted_items if it["split"] == "test")

print(f"Dataset Split Plan: Train={train_count} (70%), Valid={valid_count} (20%), Test={test_count} (10%)")

for idx, item in enumerate(extracted_items, 1):
    img_p = item["img_path"]
    lbl_p = item["lbl_path"]
    spl = item["split"]
    
    try:
        project.upload(
            image_path=img_p,
            annotation_path=lbl_p,
            split=spl,
            num_retry_uploads=3
        )
        uploaded_count += 1
        if idx % 10 == 0 or idx == len(extracted_items):
            pct = (idx / len(extracted_items)) * 100.0
            elapsed = time.time() - t_start
            print(f"  Progress: {idx}/{len(extracted_items)} uploaded ({pct:.1f}%) | Elapsed: {elapsed:.1f}s")
    except Exception as e:
        print(f"  [ERROR] Upload failed for {os.path.basename(img_p)}: {e}")
        failed_count += 1

print("\n==================================================================")
print("BATCH UPLOAD PROCESS FINISHED!")
print(f"Successfully Uploaded: {uploaded_count}/{len(extracted_items)}")
print(f"Failed: {failed_count}")
print(f"Total Time: {time.time() - t_start:.1f}s")
print(f"Check your Roboflow project: https://app.roboflow.com/{WORKSPACE}/{PROJECT_ID}")
print("==================================================================")
