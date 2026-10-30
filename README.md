# 🐾 Automated Civet Behavior Monitoring System (Phase 2 Submission)
**Chiang Mai Zoo (CMZ) × Chiang Mai University (CMU) - Advanced Image Processing**

> **Target Subject**: Large Indian Civet (*Viverra zibetha* - "หอมป้อม")  
> **Monitoring Duration**: 24.0 Hours Continuous Synchronized Video (`2026-04-05 00:00:00 – 24:00:00`)  
> **Camera Coverage**: 4 Synchronized Enclosure Rooms (Camera 01 to Camera 04)  
> **Model Architecture**: Decoupled YOLOv8n Single-Class Detector + Multi-Camera Spatial Handoff FSM  

---

## 📌 Executive Summary & Zoological Findings

This project implements an automated, non-invasive 24-hour ethogram monitoring system for the captive Large Indian Civet at Chiang Mai Zoo.

### 📊 24-Hour Behavioral Budget (Ethogram)
- **Inactive (Sleeping & Resting)**: **12.34 Hours (51.4%)**
  - Deep Box Sleep (Room 2): `05:55 – 11:06` (5h 11m) & `00:00 – 00:35` (35m)
  - Sand Floor Naps (Room 3): `01:28 – 01:34` (6m)
  - Post-feeding Rest: `11:45 – 12:05` (20m) & Evening Rest `16:25 – 17:10` (45m)
- **Active (Locomotion, Feeding, Drinking, Transit)**: **11.66 Hours (48.6%)**
  - Afternoon Feeding (Fresh Fruit Tray, Room 3): `15:38:45 – 15:43:30` (4m 45s)
  - Morning Feeding (Meat, Room 2): `11:07 – 11:45` (38m)
  - Night Active Exploration & Log Climbing: Peak between `01:00 – 05:00`
  - Hydration (Water Station, Room 4): `19:40 – 19:43`

---

## 🧠 System Architecture: Decoupled YOLOv8 + Spatial Handoff FSM

Instead of naive single-frame multi-class classification (which flickers wildly when an animal pauses during walking), our system decouples **Visual Localization** from **Temporal Zoological Reasoning**:

```
[4 Synchronized CCTV Streams (2 FPS)]
                 │
                 ▼
[YOLOv8n Single-Class Localization (mAP@50 = 86.2%)]
                 │  (Bounding Box [x1, y1, x2, y2], Centroid, Confidence)
                 ▼
[Multi-Camera Spatial Handoff FSM (Rooms 1, 2, 3, 4)]
                 │  (Spatial ROIs: Food Tray, Tire Bed, Log, Water Basin, Box)
                 ▼
[Kinematic Velocity Engine (vt = Δdist / Δt)]
                 │  (Motion threshold: vt >= 20 px/s)
                 ▼
[Temporal Debounce & Zoological 1-Minute Rule]
                 │  (Smooths momentary pauses < 60s into Active Locomotion)
                 ▼
[Daily Behavior Log CSV + 24h Chronogram Telemetry Dashboard]
```

---

## 📈 Quantitative Validation Metrics

| Metric | Measured Value | Standard / Target | Status |
|---|:---:|:---:|:---:|
| **mAP@50** | **86.2%** | >= 70.0% | ✅ Exceeded |
| **mAP@50-95** | **74.7%** | >= 50.0% | ✅ Exceeded |
| **Detection Precision** | **75.0%** | >= 70.0% | ✅ Exceeded |
| **Detection Recall** | **80.5%** | >= 75.0% | ✅ Exceeded |
| **Inference Latency** | **31.4 ms/frame** | <= 50.0 ms | ✅ Real-time Ready (>60 FPS GPU / 32 FPS CPU) |
| **Parameter Footprint** | **3,006,038 (6.2 MB)** | <= 20 MB | ✅ Edge Embedded Ready |

---

## 📂 Project Directory Structure

```text
project cmz/
├── finish/
│   ├── daily_behavior_log.csv           # 30 Digital Events / Full 24.0 Hours Log
│   ├── vet_activity_report.png          # Macro Donut + Ethogram Bars + 24h Chronogram
│   ├── multi_camera_spatial_handoff_fsm.mmd # Master Architecture Flowchart (Mermaid)
│   ├── civet_yolo_dataset_phase2.zip    # Clean YOLOv8 Dataset Package (227 frames)
│   └── demo_clips/
│       ├── view_demo_clips.html         # Interactive Video Showcase Dashboard
│       ├── demo_clip_feeding_1538.mp4   # 15:38 Afternoon Feeding (Room 3)
│       ├── demo_clip_resting_sand_nap_0130.mp4 # 01:30 Night Sand Nap (Room 3)
│       └── demo_clip_night_patrol_0125.mp4     # 01:25 Night IR Patrol (Room 3)
├── models/
│   └── yolov8n_civet_phase2/
│       └── weights/best.pt              # Fine-tuned Weights (mAP 86.2%)
├── dataset/
│   └── ชะมดแผงสันหางดำ/                  # 24-Hour Raw CCTV Video Streams (4 Cameras)
└── Image Processing Presentation.pptx   # Final Presentation Slide Deck (13 Slides)
```

---

## 🚀 Quickstart & Reproduction

### 1. Run Live Inference Demo on Video
```powershell
python scripts/run_live_inference_demo.py --video "dataset/ชะมดแผงสันหางดำ/camera 3/A03_14.03-18.18_dur_4h14m.mp4" --weights models/yolov8n_civet_phase2/weights/best.pt
```

### 2. View Interactive Telemetry Reports
Open `finish/demo_clips/view_demo_clips.html` in Google Chrome or Microsoft Edge to inspect synchronized model inference demonstrations.
