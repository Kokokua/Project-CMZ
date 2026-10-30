import os
import sys
import shutil
from ultralytics import YOLO
import torch

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
yaml_path = os.path.join(project_root, "dataset_phase2", "data.yaml")
pretrained_weights = os.path.join(project_root, "models", "yolov8n.pt")
output_project = os.path.join(project_root, "models", "phase2")
os.makedirs(output_project, exist_ok=True)

print(f"=== Starting YOLOv8 Phase 2 Training ===")
print(f"Dataset YAML: {yaml_path}")
print(f"Base Weights: {pretrained_weights}")
print(f"PyTorch Version: {torch.__version__}, CUDA Available: {torch.cuda.is_available()}")

# Load model
model = YOLO(pretrained_weights)

# Train
results = model.train(
    data=yaml_path,
    epochs=25,
    imgsz=640,
    batch=8,
    workers=2,
    project=output_project,
    name="civet_dual_class",
    exist_ok=True,
    pretrained=True,
    optimizer="AdamW",
    lr0=0.001,
    patience=10,
    save=True,
    plots=True,
    verbose=True
)

print("\n=== Training Completed ===")
# Evaluate on validation set
metrics = model.val()
print(f"mAP@50: {metrics.box.map50:.4f}")
print(f"mAP@50-95: {metrics.box.map:.4f}")
print(f"Precision: {metrics.box.mp:.4f}")
print(f"Recall: {metrics.box.mr:.4f}")

# Copy best weights to models/phase2/best.pt for easy access
best_src = os.path.join(output_project, "civet_dual_class", "weights", "best.pt")
best_dest = os.path.join(output_project, "best.pt")
if os.path.exists(best_src):
    shutil.copy2(best_src, best_dest)
    print(f"Best model weights saved at: {best_dest}")

# Copy key plots to pic/tracking_results
res_plot = os.path.join(output_project, "civet_dual_class", "results.png")
conf_plot = os.path.join(output_project, "civet_dual_class", "confusion_matrix.png")
val_plot = os.path.join(output_project, "civet_dual_class", "val_batch0_pred.jpg")

pic_dest_dir = os.path.join(project_root, "pic", "tracking_results")
os.makedirs(pic_dest_dir, exist_ok=True)

for p, name in [(res_plot, "phase2_training_curves.png"),
                (conf_plot, "phase2_confusion_matrix.png"),
                (val_plot, "phase2_validation_sample.jpg")]:
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(pic_dest_dir, name))
        print(f"Copied {name} to {pic_dest_dir}")

print("=== Phase 2 Training Pipeline Finished Successfully ===")
