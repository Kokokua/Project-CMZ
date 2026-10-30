import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

def run_quick_test():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    video_path = os.path.join(project_root, "dataset", "Locomotion-20261005T111244Z-1-001", "Locomotion", "25690518091012230.mp4")
    out_dir = os.path.join(project_root, "pic", "tracking_results")
    os.makedirs(out_dir, exist_ok=True)
    out_img_path = os.path.join(out_dir, "quick_test_locomotion_result.png")

    print(f"Loading video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    native_fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_s = total_frames / native_fps
    print(f"Native FPS: {native_fps:.1f}, Total Frames: {total_frames}, Duration: {duration_s:.2f}s")

    # Sample at 2 FPS (every 0.5s)
    sample_interval = max(1, int(round(native_fps / 2.0)))
    print(f"Sampling every {sample_interval} frames (effective ~2.0 FPS)")

    # Load YOLOv8 nano model (lightweight, fast)
    print("Loading YOLOv8n model...")
    model_path = os.path.join(project_root, "models", "yolov8n.pt")
    model = YOLO(model_path)

    sampled_frames = []
    timestamps = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % sample_interval == 0:
            sampled_frames.append(frame.copy())
            timestamps.append(frame_idx / native_fps)
        frame_idx += 1

    cap.release()
    print(f"Total sampled frames at 2 FPS: {len(sampled_frames)}")

    # Run detection on sampled frames
    results_data = []
    centroids = []

    print("\n--- Running YOLOv8 Detection ---")
    print(f"{'Idx':<4} | {'Time (s)':<8} | {'Detection':<12} | {'Conf':<6} | {'Centroid (X,Y)':<16} | {'Displacement (px)':<18} | {'Status'}")
    print("-" * 80)

    for i, (frame, t) in enumerate(zip(sampled_frames, timestamps)):
        # Run inference
        pred = model(frame, verbose=False)[0]
        
        # Look for animals or highest confidence detection
        best_box = None
        best_conf = 0.0
        best_cls_name = "None"

        # COCO animal class IDs: 15: cat, 16: dog, 17: horse, 18: sheep, 19: cow, 20: elephant, 21: bear, 22: zebra, 23: giraffe
        # Also check all detections if no animal
        animal_classes = {15, 16, 17, 18, 19, 20, 21, 22, 23}

        for box in pred.boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            cls_name = model.names[cls_id]

            if cls_id in animal_classes and conf > best_conf:
                best_conf = conf
                best_box = box.xyxy[0].cpu().numpy()
                best_cls_name = cls_name
            elif best_box is None and conf > 0.35: # fallback to any salient object
                best_conf = conf
                best_box = box.xyxy[0].cpu().numpy()
                best_cls_name = cls_name

        displacement = 0.0
        status = "No Detect"

        if best_box is not None:
            x1, y1, x2, y2 = best_box
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            
            if len(centroids) > 0 and centroids[-1] is not None:
                prev_cx, prev_cy = centroids[-1]
                displacement = np.sqrt((cx - prev_cx)**2 + (cy - prev_cy)**2)
                # Moving threshold: > 15 pixels between 0.5s frames
                status = "LOCOMOTION" if displacement > 15.0 else "RESTING"
            else:
                status = "DETECTED"

            centroids.append((cx, cy))
            results_data.append({
                "frame_idx": i,
                "time": t,
                "box": best_box,
                "label": f"{best_cls_name} ({best_conf:.2f})",
                "conf": best_conf,
                "centroid": (cx, cy),
                "displacement": displacement,
                "status": status
            })
            print(f"{i:<4} | {t:<8.2f} | {best_cls_name:<12} | {best_conf:<6.2f} | ({cx:.0f}, {cy:.0f}){'':<5} | {displacement:<18.1f} | {status}")
        else:
            centroids.append(None)
            results_data.append({
                "frame_idx": i,
                "time": t,
                "box": None,
                "label": "None",
                "conf": 0.0,
                "centroid": None,
                "displacement": 0.0,
                "status": "No Detect"
            })
            print(f"{i:<4} | {t:<8.2f} | {'None':<12} | {'-':<6} | {'-':<16} | {'-':<18} | No Detect")

    # Create Visualization Image: 4-Panel Grid
    # Panel 1: Start of walk
    # Panel 2: Mid-walk with BBox
    # Panel 3: End of walk
    # Panel 4: Full Trajectory Map overlay on base frame
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), dpi=150)
    fig.patch.set_facecolor('#0F172A')

    # Find 3 representative frames with good detections
    valid_indices = [res["frame_idx"] for res in results_data if res["box"] is not None]
    if len(valid_indices) >= 3:
        f_start_idx = valid_indices[0]
        f_mid_idx = valid_indices[len(valid_indices) // 2]
        f_end_idx = valid_indices[-1]
    else:
        f_start_idx = 0
        f_mid_idx = len(sampled_frames) // 2
        f_end_idx = len(sampled_frames) - 1

    selected_indices = [f_start_idx, f_mid_idx, f_end_idx]
    titles = ["(A) Start of Locomotion (t ≈ {:.1f}s)", "(B) Mid-Walk Detection (t ≈ {:.1f}s)", "(C) End of Locomotion (t ≈ {:.1f}s)"]

    for ax, idx, title_fmt in zip(axes.flatten()[:3], selected_indices, titles):
        frame = sampled_frames[idx].copy()
        res = results_data[idx]
        title = title_fmt.format(res["time"])

        if res["box"] is not None:
            x1, y1, x2, y2 = map(int, res["box"])
            # Draw glowing BBox
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 128), 3)
            # Label
            cv2.putText(frame, f"Civet: {res['label']}", (x1, max(30, y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2)
            # Centroid
            cx, cy = map(int, res["centroid"])
            cv2.circle(frame, (cx, cy), 8, (0, 165, 255), -1)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ax.imshow(frame_rgb)
        ax.set_title(title, color='#38BDF8', fontsize=13, fontweight='bold', pad=8)
        ax.axis('off')

    # Panel 4: Full Trajectory Map
    ax_traj = axes[1, 1]
    base_frame = sampled_frames[f_start_idx].copy()
    valid_centroids = [c for c in centroids if c is not None]

    if len(valid_centroids) > 1:
        for j in range(1, len(valid_centroids)):
            pt1 = tuple(map(int, valid_centroids[j-1]))
            pt2 = tuple(map(int, valid_centroids[j]))
            cv2.line(base_frame, pt1, pt2, (255, 128, 0), 4) # Orange trajectory line
            cv2.circle(base_frame, pt2, 7, (0, 255, 255), -1) # Yellow nodes

        # Mark Start & Finish
        start_pt = tuple(map(int, valid_centroids[0]))
        end_pt = tuple(map(int, valid_centroids[-1]))
        cv2.circle(base_frame, start_pt, 12, (0, 255, 0), -1) # Green Start
        cv2.putText(base_frame, "START", (start_pt[0] + 15, start_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.circle(base_frame, end_pt, 12, (0, 0, 255), -1) # Red End
        cv2.putText(base_frame, "FINISH", (end_pt[0] + 15, end_pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    base_rgb = cv2.cvtColor(base_frame, cv2.COLOR_BGR2RGB)
    ax_traj.imshow(base_rgb)
    ax_traj.set_title("(D) Complete Motion Trajectory Map across Enclosure", color='#F59E0B', fontsize=13, fontweight='bold', pad=8)
    ax_traj.axis('off')

    plt.suptitle("Proof-of-Concept: YOLOv8 Civet Detection & Motion Trajectory Tracking (2.0 FPS)",
                 color='#F8FAFC', fontsize=17, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(out_img_path, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()

    print(f"\nResult visualization saved successfully to: {out_img_path}")

if __name__ == "__main__":
    run_quick_test()
