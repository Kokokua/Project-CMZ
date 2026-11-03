# YOLOv8n Civet Detection & Behavior Model 

A fine-tuned **Ultralytics YOLOv8n** model trained to detect and localize the Asian Palm Civet (*Paradoxurus hermaphroditus*) under challenging 24/7 zoo surveillance conditions (daylight color and night infrared).

---

## Model Specifications

| Parameter | Specification |
|---|---|
| **Architecture** | Ultralytics YOLOv8n (Decoupled Anchor-Free Detection Head) |
| **Model Size** | 3,011,043 parameters (~6.21 MB `.pt` weights) |
| **Input Resolution** | `640 x 640` pixels |
| **Inference Latency** | **78.6 ms/frame (12.7 FPS)** on CPU · **16.6 ms/frame (60+ FPS)** on GPU (RTX 3050) |
| **Operational FPS Requirement** | 2.0 FPS multi-camera sampling (~15% single-thread CPU load) |
| **Weights Path** | [`models/yolov8n_civet_v3/weights/best.pt`](models/yolov8n_civet_v3/weights/best.pt) |

---

## Performance & Validation Metrics

Evaluated on hold-out validation frames across all 4 enclosure camera angles (daylight & night IR):

| Metric | Score | Note |
|---|:---:|---|
| **mAP@50** | **86.2%** | Mean Average Precision at IoU 0.50 |
| **mAP@50-95** | **74.7%** | Strict COCO-standard Average Precision |
| **Precision** | **75.0%** | Peaks at **82.5%** under operational threshold ($c \ge 0.40$) |
| **Recall** | **80.5%** | Exceeds **93.5%** on feeding and resting postures |
| **Empty Enclosure Specificity** | **100% (0 FP)** | Hard Negative Mining suppresses swaying leaves, sand, and wood grain |

---

## Key Model Improvements (v3)

1. **Hard Negative Mining:** Trained with empty-room background keyframes to completely eliminate false detections on the Room 3 tire bed, hanging rope, potted plants, and Room 2 ramp grain.
2. **Night Infrared Robustness:** Balanced training distribution between daytime color frames and low-light / monochrome IR frames with high specular eye reflection.
3. **Decoupled Localization:** Decouples raw visual bounding-box localization from temporal behavior classification, preventing detection flicker during momentary pauses.

---

## Quickstart: Running Inference

### 1. Installation
```bash
git clone https://github.com/Kokokua/Project-CMZ.git
cd Project-CMZ
pip install -r requirements.txt
```

### 2. Standalone CLI Prediction
Run the provided `predict.py` script directly on any image, video, or folder:
```bash
# Run inference on validation dataset
python predict.py --source dataset_phase2/images/val/ --conf 0.35

# Run inference on a specific CCTV frame
python predict.py --source path/to/cctv_frame.jpg
```

### 3. Python API Snippet
```python
from ultralytics import YOLO
import cv2

# Load the fine-tuned v3 model
model = YOLO("models/yolov8n_civet_v3/weights/best.pt")

# Run inference on an image or video frame
results = model.predict(
    source="path/to/cctv_frame.jpg",
    conf=0.35,      # Recommended confidence threshold
    iou=0.45,       # NMS IoU threshold
    imgsz=640,
    verbose=False
)

# Extract detections
for box in results[0].boxes:
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    confidence = float(box.conf[0])
    print(f"Civet detected: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}], conf: {confidence:.2f}")
```

### 3. CLI Command
```bash
yolo predict model=models/yolov8n_civet_v3/weights/best.pt source=dataset_phase2/images/val/ conf=0.35 save=True
```

---

## Multi-Camera Behavior Rules

Behavioral states are resolved by combining YOLOv8 bounding boxes with spatial Regions of Interest (ROIs) and temporal debounce rules across 4 enclosure cameras:

```
[4 CCTV Feeds (2 FPS)] ──> [YOLOv8n Localization] ──> [Spatial ROI Filter] ──> [Temporal Debounce] ──> [Behavior State]
```

- **Eating:** Bounding box inside Room 3 fruit tray ROI + head dipping, sustained for $\ge 10\text{ s}$.
- **Drinking:** Muzzle inside Room 4 water basin ROI, sustained for $\ge 3\text{ s}$.
- **Sleeping (Tire Bed):** Motionless inside Room 3 hanging tire bed for $\ge 60\text{ s}$.
- **Sleeping (Roost Box):** Managed by **Proof-of-Ingress Finite State Machine (FSM)**. When the civet enters the aperture of the opaque wooden box in Room 2, the FSM latches the `Sleeping` state until egress is detected, solving 100% optical occlusion.
- **Locomotion:** Centroid displacement $> 15\text{ px/s}$ across open floor areas for $> 3\text{ s}$.

---

## Training Hyperparameters

- **Base Architecture:** `yolov8n.pt` (COCO pre-trained weights)
- **Input Size:** `640 x 640`
- **Batch Size:** `8`
- **Optimizer:** `AdamW` (initial lr = 0.001, final lrf = 0.01)
- **Loss Gains:** Box = 7.5 (CIoU), Class = 0.5 (BCE), DFL = 1.5
- **Augmentation:** HSV jitter (h=0.015, s=0.7, v=0.4), Horizontal Flip (0.5), Mosaic (1.0)
- **Training Dataset:** [`dataset_phase2/data.yaml`](dataset_phase2/data.yaml)

