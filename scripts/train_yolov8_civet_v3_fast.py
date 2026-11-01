import os
import sys
import shutil
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
data_yaml = os.path.join(project_root, "dataset_v3_lean", "data.yaml")
project_dir = os.path.join(project_root, "models")
run_name = "yolov8n_civet_v3"

print("=" * 60)
print("FAST FINE-TUNING HIGH-PRECISION YOLOv8n MODEL (v3)")
print("Pretrained Civet Weights + Hard Negatives + Tight Tire Bed Anchoring")
print("=" * 60)

base_weights = os.path.join(project_root, "models", "yolov8n_civet_phase2", "weights", "best.pt")
assert os.path.exists(base_weights), f"Base weights not found: {base_weights}"
print(f"Loading pretrained civet weights: {base_weights}")
model = YOLO(base_weights)

print("\nStarting fine-tuning (8 epochs, imgsz=512, batch=16)...")
results = model.train(
    data=data_yaml,
    epochs=8,
    imgsz=512,
    batch=16,
    workers=0,
    project=project_dir,
    name=run_name,
    exist_ok=True,
    plots=True,
    close_mosaic=4,
    degrees=0.0,
    hsv_v=0.3,
    verbose=True
)

print("\n" + "=" * 60)
print("EVALUATING MODEL PERFORMANCE ON VALIDATION SET")
print("=" * 60)

best_weights_path = os.path.join(project_dir, run_name, "weights", "best.pt")
print(f"Loading best weights: {best_weights_path}")
best_model = YOLO(best_weights_path)
metrics = best_model.val(data=data_yaml, split='val')

print("\n--- VALIDATION METRICS ---")
print(f"mAP@50     : {metrics.box.map50:.4f} ({metrics.box.map50*100:.2f}%)")
print(f"mAP@50-95  : {metrics.box.map:.4f} ({metrics.box.map*100:.2f}%)")
print(f"Precision  : {metrics.box.mp:.4f} ({metrics.box.mp*100:.2f}%)")
print(f"Recall     : {metrics.box.mr:.4f} ({metrics.box.mr*100:.2f}%)")

# Copy best weights to delivery directory
delivery_dir = os.path.join(project_root, "finish", "models")
os.makedirs(delivery_dir, exist_ok=True)
dest_weights = os.path.join(delivery_dir, "yolov8n_civet_v3_best.pt")
shutil.copy2(best_weights_path, dest_weights)
print(f"\nModel exported successfully to: {dest_weights}")
