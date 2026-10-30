import os
import sys
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

data_yaml = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_civet_dataset\data.yaml"
project_dir = r"D:\CMU\4th\1 st\image processing\project cmz\models"

print("Loading base YOLOv8n model...")
model = YOLO("yolov8n.pt")

print("Starting YOLOv8 fine-tuning on Civet Dataset...")
# Train 25 epochs, imgsz=640, batch=8, workers=2
results = model.train(
    data=data_yaml,
    epochs=25,
    imgsz=640,
    batch=8,
    workers=2,
    project=project_dir,
    name="yolov8n_civet_phase2",
    exist_ok=True,
    plots=True
)

print("\nEvaluating model performance on Validation set...")
metrics = model.val()

print(f"\n=== TRAINING METRICS RESULTS ===")
print(f"mAP@0.5: {metrics.box.map50:.4f}")
print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
print(f"Precision: {metrics.box.mp:.4f}")
print(f"Recall: {metrics.box.mr:.4f}")

# Export weights to best.pt
best_weights = os.path.join(project_dir, "yolov8n_civet_phase2", "weights", "best.pt")
print(f"\nBest weights saved at: {best_weights}")
