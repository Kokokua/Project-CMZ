import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
data_yaml = os.path.join(project_root, "dataset_multiclass", "data_multiclass.yaml")
project_dir = os.path.join(project_root, "models")
model_out_dir = os.path.join(project_dir, "yolov8n_civet_multiclass")

print("=" * 60)
print("TRAINING MULTI-CLASS BEHAVIOR / POSE YOLOv8 MODEL")
print("Classes: [0: locomotion, 1: resting, 2: feeding, 3: drinking, 4: grooming]")
print("=" * 60)

# Check base weights
base_weights = os.path.join(project_root, "models", "yolov8n.pt")
if not os.path.exists(base_weights):
    base_weights = "yolov8n.pt"

print(f"Loading base YOLOv8n weights from: {base_weights}")
model = YOLO(base_weights)

print("\nStarting training (25 epochs, imgsz=640, batch=8)...")
results = model.train(
    data=data_yaml,
    epochs=25,
    imgsz=640,
    batch=8,
    workers=2,
    project=project_dir,
    name="yolov8n_civet_multiclass",
    exist_ok=True,
    plots=True,
    verbose=True
)

print("\n" + "=" * 60)
print("VALIDATION & QUANTITATIVE EVALUATION")
print("=" * 60)

val_model_path = os.path.join(model_out_dir, "weights", "best.pt")
print(f"Loading best weights: {val_model_path}")
best_model = YOLO(val_model_path)
metrics = best_model.val(data=data_yaml, split='val')

class_names = ['locomotion', 'resting', 'feeding', 'drinking', 'grooming']
print("\n--- OVERALL METRICS ---")
print(f"mAP@50     : {metrics.box.map50:.4f} ({metrics.box.map50*100:.2f}%)")
print(f"mAP@50-95  : {metrics.box.map:.4f} ({metrics.box.map*100:.2f}%)")
print(f"Precision  : {metrics.box.mp:.4f} ({metrics.box.mp*100:.2f}%)")
print(f"Recall     : {metrics.box.mr:.4f} ({metrics.box.mr*100:.2f}%)")

print("\n--- PER-CLASS METRICS ---")
for idx, cname in enumerate(class_names):
    if idx < len(metrics.box.p):
        p = metrics.box.p[idx]
        r = metrics.box.r[idx]
        ap50 = metrics.box.ap50[idx]
        ap = metrics.box.ap[idx]
        print(f"Class {idx} [{cname:10s}]: Precision={p:.4f}, Recall={r:.4f}, mAP@50={ap50:.4f}, mAP@50-95={ap:.4f}")

# Copy best weights to finish / delivery directory
delivery_weights_dir = os.path.join(project_root, "finish", "models")
os.makedirs(delivery_weights_dir, exist_ok=True)
import shutil
target_weights = os.path.join(delivery_weights_dir, "yolov8n_civet_multiclass_best.pt")
shutil.copy2(val_model_path, target_weights)
print(f"\nDeliverable weights mirrored to: {target_weights}")

print("\nMulti-Class Pose/Behavior YOLO training and validation COMPLETE!")
