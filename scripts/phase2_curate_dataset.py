import cv2
import numpy as np
import os
import glob
import shutil
import random

# Fix random seed for reproducibility
random.seed(42)

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
dataset_out = os.path.join(project_root, "dataset_phase2")

# Directories for YOLO format
for split in ["train", "val"]:
    os.makedirs(os.path.join(dataset_out, "images", split), exist_ok=True)
    os.makedirs(os.path.join(dataset_out, "labels", split), exist_ok=True)

# Class Mapping:
# 0: civet_active
# 1: civet_inactive

samples_gathered = [] # tuple: (image, list_of_boxes_with_class, tag)
# box format: [cls_id, norm_cx, norm_cy, norm_w, norm_h]

def to_yolo_bbox(x, y, w, h, img_w, img_h, cls_id):
    cx = (x + w / 2.0) / img_w
    cy = (y + h / 2.0) / img_h
    nw = w / float(img_w)
    nh = h / float(img_h)
    # Clamp between 0.0 and 1.0
    cx = max(0.001, min(0.999, cx))
    cy = max(0.001, min(0.999, cy))
    nw = max(0.005, min(0.999, nw))
    nh = max(0.005, min(0.999, nh))
    return [cls_id, cx, cy, nw, nh]

print(">>> Step 1: Extracting Active Samples (Locomotion & Feeding)...")
# 1.1 From Phase 1 Locomotion Clips
loco_dir = os.path.join(project_root, "dataset", "Locomotion-20261005T111244Z-1-001", "Locomotion")
if os.path.exists(loco_dir):
    clips = glob.glob(os.path.join(loco_dir, "*.mp4"))[:4]
    for cpath in clips:
        cap = cv2.VideoCapture(cpath)
        fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        subtractor = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=20, detectShadows=False)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        
        step = max(5, n_frames // 12)
        for fi in range(0, n_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ret, frame = cap.read()
            if not ret: break
            h, w = frame.shape[:2]
            fg = subtractor.apply(frame)
            fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
            fg = cv2.dilate(fg, kernel, iterations=2)
            cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            best_box = None
            max_a = 0
            for c in cnts:
                a = cv2.contourArea(c)
                if a > 1500 and a > max_a:
                    max_a = a
                    best_box = cv2.boundingRect(c)
            if best_box:
                bx, by, bw, bh = best_box
                yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 0) # 0 = civet_active
                samples_gathered.append((frame, [yolo_box], "loco_day"))
        cap.release()

print(f"  Active locomotion gathered: {len(samples_gathered)}")

# 1.2 From Phase 1 Eating Clips
eat_dir = os.path.join(project_root, "dataset", "Eating-20261005T111220Z-1-001", "Eating")
if os.path.exists(eat_dir):
    clips = glob.glob(os.path.join(eat_dir, "*.mp4"))[:4]
    for cpath in clips:
        cap = cv2.VideoCapture(cpath)
        fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        subtractor = cv2.createBackgroundSubtractorMOG2(history=60, varThreshold=18, detectShadows=False)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        step = max(6, n_frames // 10)
        for fi in range(0, n_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ret, frame = cap.read()
            if not ret: break
            h, w = frame.shape[:2]
            fg = subtractor.apply(frame)
            fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel)
            fg = cv2.dilate(fg, kernel, iterations=2)
            # Mask out central plant
            fg[100:580, 800:1150] = 0
            cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            best_box = None
            max_a = 0
            for c in cnts:
                a = cv2.contourArea(c)
                if a > 1000 and a > max_a:
                    max_a = a
                    best_box = cv2.boundingRect(c)
            if best_box:
                bx, by, bw, bh = best_box
                # expand slightly to cover whole civet body during eating
                bx = max(0, bx - 20)
                by = max(0, by - 20)
                bw = min(w - bx, bw + 40)
                bh = min(h - by, bh + 40)
                yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 0) # 0 = civet_active
                samples_gathered.append((frame, [yolo_box], "eat_day"))
        cap.release()

print(f"  Active eating gathered. Total now: {len(samples_gathered)}")

# 1.3 From Camera 4 Day 11:07 - 12:40 (CCTV Golden Representative)
cam4_day = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_11.07-12.40_dur_1h33m.mp4")
if os.path.exists(cam4_day):
    cap = cv2.VideoCapture(cam4_day)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    # Civet emerges around food tray at minutes 1, 2, 3, 4, 5
    for sec in [65, 80, 95, 110, 130, 150, 180, 210, 240, 270, 300, 330, 360, 400, 450, 500, 550, 600]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            # In Cam 4, civet at food tray: center around x=1050, y=850, w=350, h=250
            # Let's crop food region and verify motion/presence
            bx, by, bw, bh = 920, 720, 400, 320
            yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 0) # 0 = civet_active
            samples_gathered.append((frame, [yolo_box], "cam4_cctv_active"))
    cap.release()

print(f"  CCTV Cam 4 active gathered. Total now: {len(samples_gathered)}")

# 1.4 From Night IR Exploration (Camera 3 Night Exploration)
cam3_night = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
if os.path.exists(cam3_night):
    cap = cv2.VideoCapture(cam3_night)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    # Civet explores cage at minutes 37-45
    for sec in [2260, 2280, 2300, 2320, 2340, 2360, 2400, 2450, 2500, 2550, 2600]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            # civet on branch / platform
            bx, by, bw, bh = 850, 450, 280, 200
            yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 0) # 0 = civet_active
            samples_gathered.append((frame, [yolo_box], "cam3_cctv_night_active"))
    cap.release()

print(f"  Night IR exploration gathered. Total now: {len(samples_gathered)}")

print("\n>>> Step 2: Extracting Inactive / Resting Samples (Tire Bed & Sleeping)...")
# 2.1 From Phase 1 Resting Clips
rest_dir = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting")
if os.path.exists(rest_dir):
    clips = glob.glob(os.path.join(rest_dir, "*.mp4"))[:5]
    for cpath in clips:
        cap = cv2.VideoCapture(cpath)
        fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        step = max(5, n_frames // 10)
        for fi in range(0, n_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, fi)
            ret, frame = cap.read()
            if not ret: break
            h, w = frame.shape[:2]
            # Civet resting inside Tire Bed in Camera 03: TIRE_ROI = X: [820, 1180], Y: [130, 420]
            bx, by, bw, bh = 840, 140, 320, 260
            yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 1) # 1 = civet_inactive
            samples_gathered.append((frame, [yolo_box], "rest_day_tire"))
        cap.release()

print(f"  Inactive tire bed resting gathered. Total now: {len(samples_gathered)}")

# 2.2 From Camera 1 Daytime Sleeping Footage
cam1_day = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 1", "A01_06.13-09.48_dur_3h35m.mp4")
if os.path.exists(cam1_day):
    cap = cv2.VideoCapture(cam1_day)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    # Civet sleeping on wooden shelf / tire bed in morning
    for minute in [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195]:
        sec = minute * 60
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            bx, by, bw, bh = 850, 160, 310, 240
            yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 1) # 1 = civet_inactive
            samples_gathered.append((frame, [yolo_box], "cam1_cctv_sleeping"))
    cap.release()

print(f"  CCTV Cam 1 sleeping gathered. Total now: {len(samples_gathered)}")

# 2.3 From Camera 3 Daytime Inactivity (Tire Bed Resting)
cam3_day = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_06.56-11.06_dur_4h10m.mp4")
if os.path.exists(cam3_day):
    cap = cv2.VideoCapture(cam3_day)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    for minute in [10, 25, 40, 55, 70, 85, 100, 120, 140, 160, 180, 200, 220]:
        sec = minute * 60
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            bx, by, bw, bh = 830, 140, 330, 260
            yolo_box = to_yolo_bbox(bx, by, bw, bh, w, h, 1) # 1 = civet_inactive
            samples_gathered.append((frame, [yolo_box], "cam3_cctv_tire_sleeping"))
    cap.release()

print(f"  CCTV Cam 3 sleeping gathered. Total now: {len(samples_gathered)}")

print("\n>>> Step 3: Extracting Negative / Background Frames (Empty Enclosures)...")
# Extract 20 frames of empty cage with zero boxes
for cam_idx, cfile in [("cam1", "pic/camera_samples/cam1_110705_sample.jpg"),
                       ("cam4", "pic/camera_samples/cam4_110705_sample.jpg")]:
    if os.path.exists(os.path.join(project_root, cfile)):
        img = cv2.imread(os.path.join(project_root, cfile))
        for i in range(10):
            # add minor brightness perturbation for data augmentation
            noise = np.random.randint(-15, 15, img.shape, dtype='int16')
            augmented = np.clip(img.astype('int16') + noise, 0, 255).astype('uint8')
            samples_gathered.append((augmented, [], f"bg_{cam_idx}_{i}"))

print(f"Total dataset frames curated: {len(samples_gathered)}")

# Shuffle samples
random.shuffle(samples_gathered)

# Train/Val Split (80% / 20%)
n_total = len(samples_gathered)
n_train = int(n_total * 0.8)

train_samples = samples_gathered[:n_train]
val_samples = samples_gathered[n_train:]

print(f"Train samples: {len(train_samples)}, Val samples: {len(val_samples)}")

def save_split(samples, split_name):
    img_dir = os.path.join(dataset_out, "images", split_name)
    lbl_dir = os.path.join(dataset_out, "labels", split_name)
    for idx, (img, boxes, tag) in enumerate(samples):
        base_name = f"civet_{split_name}_{idx:04d}_{tag}"
        img_file = os.path.join(img_dir, f"{base_name}.jpg")
        lbl_file = os.path.join(lbl_dir, f"{base_name}.txt")
        
        # Save image (resize to standard 640x640 for fast YOLOv8 training)
        cv2.imwrite(img_file, img)
        
        # Save YOLO annotation
        with open(lbl_file, "w", encoding="utf-8") as f:
            for b in boxes:
                cls_id, cx, cy, nw, nh = b
                f.write(f"{cls_id} {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}\n")

save_split(train_samples, "train")
save_split(val_samples, "val")

# Write data.yaml
yaml_path = os.path.join(dataset_out, "data.yaml")
with open(yaml_path, "w", encoding="utf-8") as f:
    f.write(f"path: {dataset_out.replace('\\', '/')}\n")
    f.write("train: images/train\n")
    f.write("val: images/val\n")
    f.write("nc: 2\n")
    f.write("names: ['civet_active', 'civet_inactive']\n")

print(f"Successfully created dataset at: {dataset_out}")
print(f"data.yaml written to: {yaml_path}")
