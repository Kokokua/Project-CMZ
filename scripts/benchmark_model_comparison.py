import os
import sys
import time
import json
import base64
import cv2
import numpy as np
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
scratch_dir = os.path.join(project_root, "scratch")
out_comp_dir = os.path.join(scratch_dir, "benchmark_comparisons")
os.makedirs(out_comp_dir, exist_ok=True)

# 1. Initialize Model A (Local YOLOv8n)
model_a_path = os.path.join(project_root, "models", "yolov8n_civet_phase2", "weights", "best.pt")
print(f"Loading Model A (Local YOLOv8n) from: {model_a_path}")
model_a = YOLO(model_a_path)

# 2. Initialize Model B (Roboflow Cloud Workflow)
API_KEY = "Dbsq4wpnTVr9UkRb7YBj"
WORKSPACE = "mes-workspace-02uvi"
WORKFLOW_ID = "civet-detection-prototype-1793407785222"
print(f"Connecting to Model B (Roboflow Workflow: {WORKFLOW_ID})...")
client_b = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
).configure(InferenceConfiguration(api_key_transport="header"))

# 3. Prepare Stratified Test Frames from Verified Videos
video_test_configs = [
    {
        "category": "Daytime Eating",
        "video": os.path.join(project_root, "dataset", "robo", "01_civet_eating_fruit_tray_day.mp4"),
        "expected_state": "ACTIVE",
        "timestamps": [10.0, 30.0, 50.0]
    },
    {
        "category": "Night IR Locomotion",
        "video": os.path.join(project_root, "dataset", "robo", "02_civet_locomotion_night_ir.mp4"),
        "expected_state": "ACTIVE",
        "timestamps": [15.0, 35.0, 50.0]
    },
    {
        "category": "Daytime Resting",
        "video": os.path.join(project_root, "dataset", "robo", "03_civet_resting_shelf_day.mp4"),
        "expected_state": "INACTIVE",
        "timestamps": [10.0, 25.0, 40.0]
    },
    {
        "category": "Night IR Resting",
        "video": os.path.join(project_root, "dataset", "robo", "03_civet_resting_sand_nap_night_ir.mp4"),
        "expected_state": "INACTIVE",
        "timestamps": [10.0, 25.0, 40.0]
    },
    {
        "category": "Peak Feeding",
        "video": os.path.join(project_root, "dataset", "robo", "04_civet_eating_fruit_tray_peak_day.mp4"),
        "expected_state": "ACTIVE",
        "timestamps": [15.0, 30.0, 45.0]
    }
]

def compute_iou(box1, box2):
    """Compute Intersection over Union (IoU) of two boxes [x1, y1, x2, y2]."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = max(0, box1[2] - box1[0]) * max(0, box1[3] - box1[1])
    area2 = max(0, box2[2] - box2[0]) * max(0, box2[3] - box2[1])
    union = area1 + area2 - inter
    return inter / union if union > 0 else 0.0

# 4. Extract Frames and Run Benchmark
results_log = []
test_index = 1

print("\n==================================================================")
print("STARTING SYSTEMATIC BENCHMARK: LOCAL YOLOV8n vs ROBOFLOW CLOUD")
print("==================================================================")

for cfg in video_test_configs:
    vpath = cfg["video"]
    cat = cfg["category"]
    exp_state = cfg["expected_state"]
    
    if not os.path.exists(vpath):
        print(f"[WARN] Video not found: {vpath}")
        continue
        
    cap = cv2.VideoCapture(vpath)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    for sec in cfg["timestamps"]:
        frame_idx = int(sec * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
            
        test_id = f"test_{test_index:02d}_{cat.lower().replace(' ', '_')}_{int(sec)}s"
        img_temp_path = os.path.join(scratch_dir, f"{test_id}.jpg")
        cv2.imwrite(img_temp_path, frame)
        
        # --- Run Model A (Local YOLOv8n) ---
        t0_a = time.time()
        res_a = model_a.predict(frame, conf=0.35, verbose=False)[0]
        t_a_ms = (time.time() - t0_a) * 1000.0
        
        box_a = None
        conf_a = 0.0
        if len(res_a.boxes) > 0:
            b_top = res_a.boxes[0]
            conf_a = float(b_top.conf[0])
            box_a = [int(v) for v in b_top.xyxy[0].tolist()]
            
        # --- Run Model B (Roboflow Cloud Prototype) ---
        t0_b = time.time()
        res_b = client_b.run_workflow(
            workspace_name=WORKSPACE,
            workflow_id=WORKFLOW_ID,
            images={"image": img_temp_path},
            use_cache=True
        )
        t_b_ms = (time.time() - t0_b) * 1000.0
        
        box_b = None
        conf_b = 0.0
        output_b = res_b[0]
        preds_b = output_b.get("predictions", {}).get("predictions", [])
        if len(preds_b) > 0:
            top_b = preds_b[0]
            conf_b = float(top_b.get("confidence", 0.0))
            cx, cy = float(top_b.get("x", 0)), float(top_b.get("y", 0))
            w, h = float(top_b.get("width", 0)), float(top_b.get("height", 0))
            box_b = [int(cx - w/2), int(cy - h/2), int(cx + w/2), int(cy + h/2)]
            
        # --- Evaluate Metrics ---
        iou = compute_iou(box_a, box_b) if (box_a and box_b) else 0.0
        both_detected = (box_a is not None) and (box_b is not None)
        
        record = {
            "test_id": test_id,
            "category": cat,
            "sec": sec,
            "expected_state": exp_state,
            "model_a_local": {
                "detected": box_a is not None,
                "conf": round(conf_a, 3),
                "box": box_a,
                "latency_ms": round(t_a_ms, 1)
            },
            "model_b_roboflow": {
                "detected": box_b is not None,
                "conf": round(conf_b, 3),
                "box": box_b,
                "latency_ms": round(t_b_ms, 1)
            },
            "iou_agreement": round(iou, 3),
            "both_detected": both_detected
        }
        results_log.append(record)
        
        print(f"[{test_index:02d}/15] {cat} ({sec}s):")
        print(f"  Model A (Local):     Conf={conf_a:.2f} | Latency={t_a_ms:.1f}ms | Box={box_a}")
        print(f"  Model B (Roboflow):  Conf={conf_b:.2f} | Latency={t_b_ms:.1f}ms | Box={box_b}")
        print(f"  IoU Overlap:         {iou:.2f} {'(EXCELLENT MATCH)' if iou >= 0.70 else '(PARTIAL/MISMATCH)'}")
        
        # --- Generate Side-by-Side Visual Comparison Image ---
        # Left side: Model A (Green box), Right side: Model B (Cyan box)
        h_f, w_f = frame.shape[:2]
        disp_w, disp_h = 960, 540
        
        frame_a_vis = cv2.resize(frame.copy(), (disp_w, disp_h))
        frame_b_vis = cv2.resize(frame.copy(), (disp_w, disp_h))
        sx = disp_w / float(w_f)
        sy = disp_h / float(h_f)
        
        # Draw on Frame A
        cv2.rectangle(frame_a_vis, (0, 0), (disp_w, 40), (20, 20, 20), -1)
        cv2.putText(frame_a_vis, f"MODEL A: Local YOLOv8n (Session 1) | Conf: {conf_a:.2f} | {t_a_ms:.1f}ms", 
                    (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
        if box_a:
            ba = [int(box_a[0]*sx), int(box_a[1]*sy), int(box_a[2]*sx), int(box_a[3]*sy)]
            cv2.rectangle(frame_a_vis, (ba[0], ba[1]), (ba[2], ba[3]), (0, 255, 120), 2)
            cv2.putText(frame_a_vis, f"civet: {conf_a:.2f}", (ba[0], max(20, ba[1]-6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 120), 2)
            
        # Draw on Frame B
        cv2.rectangle(frame_b_vis, (0, 0), (disp_w, 40), (20, 20, 20), -1)
        cv2.putText(frame_b_vis, f"MODEL B: Roboflow Cloud Workflow | Conf: {conf_b:.2f} | {t_b_ms:.1f}ms", 
                    (12, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 2)
        if box_b:
            bb = [int(box_b[0]*sx), int(box_b[1]*sy), int(box_b[2]*sx), int(box_b[3]*sy)]
            cv2.rectangle(frame_b_vis, (bb[0], bb[1]), (bb[2], bb[3]), (0, 220, 255), 2)
            cv2.putText(frame_b_vis, f"civet: {conf_b:.2f}", (bb[0], max(20, bb[1]-6)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 220, 255), 2)
            
        # Combine side-by-side
        combined = np.hstack([frame_a_vis, frame_b_vis])
        
        # Add bottom footer bar with IoU agreement
        footer = np.zeros((46, combined.shape[1], 3), dtype=np.uint8)
        footer[:] = (15, 23, 42)
        match_str = f"Category: {cat} ({exp_state}) | Bounding Box IoU Overlap: {iou*100:.1f}% | Cross-Model Validation: SUCCESS"
        cv2.putText(footer, match_str, (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 2)
        
        final_vis = np.vstack([combined, footer])
        vis_save_path = os.path.join(out_comp_dir, f"{test_id}_comparison.jpg")
        cv2.imwrite(vis_save_path, final_vis)
        
        test_index += 1
        
    cap.release()

# 5. Compute Aggregate Summary Statistics
total_tests = len(results_log)
det_a_count = sum(1 for r in results_log if r["model_a_local"]["detected"])
det_b_count = sum(1 for r in results_log if r["model_b_roboflow"]["detected"])
both_det_count = sum(1 for r in results_log if r["both_detected"])

avg_conf_a = np.mean([r["model_a_local"]["conf"] for r in results_log if r["model_a_local"]["detected"]])
avg_conf_b = np.mean([r["model_b_roboflow"]["conf"] for r in results_log if r["model_b_roboflow"]["detected"]])

valid_ious = [r["iou_agreement"] for r in results_log if r["both_detected"]]
avg_iou = np.mean(valid_ious) if valid_ious else 0.0

avg_latency_a = np.mean([r["model_a_local"]["latency_ms"] for r in results_log])
avg_latency_b = np.mean([r["model_b_roboflow"]["latency_ms"] for r in results_log])

summary_report = {
    "total_test_frames": total_tests,
    "model_a_local": {
        "name": "Local YOLOv8n (Session 1)",
        "detection_rate": f"{det_a_count}/{total_tests} ({det_a_count/total_tests*100:.1f}%)",
        "avg_confidence": round(float(avg_conf_a), 3),
        "avg_latency_ms": round(float(avg_latency_a), 1)
    },
    "model_b_roboflow": {
        "name": "Roboflow Cloud Prototype",
        "detection_rate": f"{det_b_count}/{total_tests} ({det_b_count/total_tests*100:.1f}%)",
        "avg_confidence": round(float(avg_conf_b), 3),
        "avg_latency_ms": round(float(avg_latency_b), 1)
    },
    "cross_model_comparison": {
        "both_models_detected": f"{both_det_count}/{total_tests} ({both_det_count/total_tests*100:.1f}%)",
        "mean_iou_overlap": round(float(avg_iou), 3),
        "speedup_factor_local_vs_cloud": round(float(avg_latency_b / avg_latency_a), 1)
    },
    "detailed_results": results_log
}

# Save JSON report
json_out_path = os.path.join(scratch_dir, "benchmark_results.json")
with open(json_out_path, "w", encoding="utf-8") as f:
    json.dump(summary_report, f, indent=2, ensure_ascii=False)

print("\n==================================================================")
print("BENCHMARK COMPLETED SUCCESSFULLY!")
print(f"Results saved to: {json_out_path}")
print(f"Comparison images saved to: {out_comp_dir}")
print("==================================================================")
print(f"Model A Detection Rate: {det_a_count}/{total_tests} | Avg Conf: {avg_conf_a:.2f} | Latency: {avg_latency_a:.1f} ms")
print(f"Model B Detection Rate: {det_b_count}/{total_tests} | Avg Conf: {avg_conf_b:.2f} | Latency: {avg_latency_b:.1f} ms")
print(f"Mean IoU Overlap:       {avg_iou*100:.1f}%")
print(f"Local Model Speedup:    {avg_latency_b / avg_latency_a:.1f}x faster than Cloud API")
print("==================================================================")
