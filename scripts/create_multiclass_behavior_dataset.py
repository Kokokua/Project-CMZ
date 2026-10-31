import cv2
import os
import sys
import glob
import random
import shutil
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

def build_multiclass_dataset():
    project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
    out_dataset = os.path.join(project_root, "dataset_multiclass")
    
    # Subdirectories
    train_img_dir = os.path.join(out_dataset, "images", "train")
    val_img_dir = os.path.join(out_dataset, "images", "val")
    train_lbl_dir = os.path.join(out_dataset, "labels", "train")
    val_lbl_dir = os.path.join(out_dataset, "labels", "val")
    preview_dir = os.path.join(out_dataset, "annotated_previews")
    
    for d in [train_img_dir, val_img_dir, train_lbl_dir, val_lbl_dir, preview_dir]:
        os.makedirs(d, exist_ok=True)
        
    # Load detector to assist accurate bounding box localization
    model_path = os.path.join(project_root, "models", "yolov8n_civet_phase2", "weights", "best.pt")
    detector = YOLO(model_path)
    print("Loaded YOLOv8 detector for precise bounding box discovery.")
    
    # Class mapping
    # 0: locomotion, 1: resting, 2: feeding, 3: drinking, 4: grooming
    CLASSES = {
        'locomotion': 0,
        'resting': 1,
        'feeding': 2,
        'drinking': 3,
        'grooming': 4
    }
    
    # 1. Existing Phase 2 images that map cleanly
    src_phase2 = os.path.join(project_root, "dataset_phase2")
    src_imgs = glob.glob(os.path.join(src_phase2, "images", "**", "*.jpg"), recursive=True)
    print(f"Found {len(src_imgs)} existing source images in dataset_phase2.")
    
    dataset_records = [] # (img_path, class_name, bbox_xywh_norm_or_None)
    
    for ip in src_imgs:
        fname = os.path.basename(ip)
        base = os.path.splitext(fname)[0]
        # find corresponding label in dataset_phase2
        # check both train and val
        lp_train = os.path.join(src_phase2, "labels", "train", f"{base}.txt")
        lp_val = os.path.join(src_phase2, "labels", "val", f"{base}.txt")
        lp = lp_train if os.path.exists(lp_train) else (lp_val if os.path.exists(lp_val) else None)
        
        if lp and os.path.getsize(lp) == 0 or "empty" in fname or "bg" in fname:
            dataset_records.append((ip, 'bg', None))
            continue
            
        if lp and os.path.exists(lp):
            with open(lp, 'r') as f:
                lines = f.readlines()
            if not lines:
                dataset_records.append((ip, 'bg', None))
                continue
                
            parts = lines[0].strip().split()
            if len(parts) >= 5:
                # read existing bbox
                bbox = [float(p) for p in parts[1:5]]
                
                # classify based on behavior in fname
                if "eat" in fname or "food" in fname:
                    dataset_records.append((ip, 'feeding', bbox))
                elif "loco" in fname:
                    dataset_records.append((ip, 'locomotion', bbox))
                elif "rest" in fname or "sleep" in fname:
                    # In dataset_phase2, if it's tire bed or sleeping quarters -> true resting
                    dataset_records.append((ip, 'resting', bbox))
                elif "cam4_cctv_active" in fname or "cam3_cctv_night_active" in fname:
                    dataset_records.append((ip, 'locomotion', bbox))

    print(f"Mapped {len(dataset_records)} records from dataset_phase2.")

    # 2. Extract GROOMING frames (Cam 3 @ 01:29:45 - 01:31:20)
    # Strictly from dataset/ชะมดแผงสันหางดำ
    v_c3 = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
    cap3 = cv2.VideoCapture(v_c3)
    # 01:29:45 is sec 5385; extract 25 frames up to sec 5470
    groom_sec_list = list(range(5385, 5470, 3)) # 28 frames
    groom_extracted = 0
    for s_idx, sec in enumerate(groom_sec_list):
        cap3.set(cv2.CAP_PROP_POS_FRAMES, int(sec * 30.0))
        ret, frame = cap3.read()
        if not ret: continue
        
        # detect with model
        res = detector.predict(frame, conf=0.30, verbose=False)[0]
        if len(res.boxes) > 0:
            box = res.boxes[0].xywhn[0].tolist() # x_center, y_center, w, h
            out_img_name = f"civet_grooming_c3_0130_{s_idx:03d}.jpg"
            out_img_path = os.path.join(out_dataset, "images", out_img_name)
            cv2.imwrite(out_img_path, frame)
            dataset_records.append((out_img_path, 'grooming', box))
            groom_extracted += 1
    cap3.release()
    print(f"Extracted {groom_extracted} new GROOMING frames from Cam 3 (01:29:45 - 01:31:10).")

    # 3. Extract DRINKING frames (Cam 4 @ 04:39:00)
    v_c4 = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")
    cap4 = cv2.VideoCapture(v_c4)
    # 04:39:00 is sec 1320; extract 20 frames from sec 1315 to 1355
    drink_sec_list = list(range(1315, 1355, 2)) # 20 frames
    drink_extracted = 0
    for s_idx, sec in enumerate(drink_sec_list):
        cap4.set(cv2.CAP_PROP_POS_FRAMES, int(sec * 30.0))
        ret, frame = cap4.read()
        if not ret: continue
        
        res = detector.predict(frame, conf=0.25, verbose=False)[0]
        if len(res.boxes) > 0:
            box = res.boxes[0].xywhn[0].tolist()
            out_img_name = f"civet_drinking_c4_0439_{s_idx:03d}.jpg"
            out_img_path = os.path.join(out_dataset, "images", out_img_name)
            cv2.imwrite(out_img_path, frame)
            dataset_records.append((out_img_path, 'drinking', box))
            drink_extracted += 1
        else:
            # Civet is dipping mouth into water basin: manual bounding box around basin in 1080p
            # basin is around x: 590..840, y: 540..800
            h, w = frame.shape[:2]
            box = [(590 + 840) / 2 / w, (540 + 800) / 2 / h, (840 - 590) / w, (800 - 540) / h]
            out_img_name = f"civet_drinking_c4_0439_{s_idx:03d}.jpg"
            out_img_path = os.path.join(out_dataset, "images", out_img_name)
            cv2.imwrite(out_img_path, frame)
            dataset_records.append((out_img_path, 'drinking', box))
            drink_extracted += 1
    cap4.release()
    print(f"Extracted {drink_extracted} new DRINKING frames from Cam 4 (04:39:00).")

    # 4. Extract MORNING SHELTER SLEEPING frames (Cam 2 @ 07:00:00)
    v_c2 = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 2", "A02_05.55-09.51_dur_3h56m.mp4")
    cap2 = cv2.VideoCapture(v_c2)
    # Sec 2000 to 2040: civet sleeping in shelter box
    sleep_sec_list = list(range(2000, 2040, 3))
    sleep_extracted = 0
    for s_idx, sec in enumerate(sleep_sec_list):
        cap2.set(cv2.CAP_PROP_POS_FRAMES, int(sec * 30.0))
        ret, frame = cap2.read()
        if not ret: continue
        
        # Bounding box in sleeping shelter box
        h, w = frame.shape[:2]
        # Shelter box in 1080p: [380, 50, 680, 400]
        box = [(380 + 680) / 2 / w, (50 + 400) / 2 / h, (680 - 380) / w, (400 - 50) / h]
        out_img_name = f"civet_resting_shelter_c2_0700_{s_idx:03d}.jpg"
        out_img_path = os.path.join(out_dataset, "images", out_img_name)
        cv2.imwrite(out_img_path, frame)
        dataset_records.append((out_img_path, 'resting', box))
        sleep_extracted += 1
    cap2.release()
    print(f"Extracted {sleep_extracted} new DEEP RESTING frames from Cam 2 shelter.")

    # 5. Extract Negative Background frames (empty cage, empty ramp, empty tire)
    v_c3_empty = cv2.VideoCapture(v_c3)
    for s_idx, sec in enumerate(range(100, 200, 15)):
        v_c3_empty.set(cv2.CAP_PROP_POS_FRAMES, int(sec * 30.0))
        ret, frame = v_c3_empty.read()
        if ret:
            out_img_name = f"bg_empty_cam3_floor_{s_idx:02d}.jpg"
            out_img_path = os.path.join(out_dataset, "images", out_img_name)
            cv2.imwrite(out_img_path, frame)
            dataset_records.append((out_img_path, 'bg', None))
    v_c3_empty.release()

    # Summarize dataset records by class
    from collections import Counter
    counts = Counter([r[1] for r in dataset_records])
    print("\nDataset Class Distribution:")
    for k, v in counts.items():
        print(f"  {k:12s}: {v:3d} images")

    # Stratified Train / Val split (80% Train, 20% Val)
    random.seed(42)
    by_class = {}
    for r in dataset_records:
        by_class.setdefault(r[1], []).append(r)

    train_records = []
    val_records = []
    for cls_name, recs in by_class.items():
        random.shuffle(recs)
        n_val = max(1, int(len(recs) * 0.20))
        val_records.extend(recs[:n_val])
        train_records.extend(recs[n_val:])

    print(f"\nTotal Dataset: {len(dataset_records)} | Train: {len(train_records)} | Val: {len(val_records)}")

    # Write out files to train and val directories
    def write_split(records, img_dest_dir, lbl_dest_dir, split_name):
        for idx, (ipath, cls_name, bbox) in enumerate(records):
            ext = os.path.splitext(ipath)[1]
            out_base = f"civet_{split_name}_{idx:04d}_{cls_name}"
            out_img = os.path.join(img_dest_dir, f"{out_base}{ext}")
            out_lbl = os.path.join(lbl_dest_dir, f"{out_base}.txt")
            
            # Copy image
            shutil.copy2(ipath, out_img)
            
            # Write YOLO label
            with open(out_lbl, 'w') as f:
                if cls_name != 'bg' and bbox is not None:
                    cls_id = CLASSES[cls_name]
                    f.write(f"{cls_id} {bbox[0]:.6f} {bbox[1]:.6f} {bbox[2]:.6f} {bbox[3]:.6f}\n")
                    
            # Generate preview on first 5 of each class
            if idx % 8 == 0 and cls_name != 'bg' and bbox is not None:
                img = cv2.imread(out_img)
                h, w = img.shape[:2]
                bx, by, bw, bh = bbox
                x1 = int((bx - bw/2) * w)
                y1 = int((by - bh/2) * h)
                x2 = int((bx + bw/2) * w)
                y2 = int((by + bh/2) * h)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{cls_name} (ID: {CLASSES[cls_name]})", (x1, max(25, y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imwrite(os.path.join(preview_dir, f"preview_{out_base}.jpg"), img)

    write_split(train_records, train_img_dir, train_lbl_dir, "train")
    write_split(val_records, val_img_dir, val_lbl_dir, "val")

    # Generate data_multiclass.yaml
    yaml_path = os.path.join(out_dataset, "data_multiclass.yaml")
    yaml_content = f"""path: {out_dataset.replace(chr(92), '/')}
train: images/train
val: images/val
nc: 5
names: ['locomotion', 'resting', 'feeding', 'drinking', 'grooming']
"""
    with open(yaml_path, 'w') as f:
        f.write(yaml_content)

    print(f"\nGenerated YAML config at: {yaml_path}")
    print(yaml_content)
    return yaml_path

if __name__ == '__main__':
    build_multiclass_dataset()
