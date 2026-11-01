"""
Independent Camera Batch Feature Extractor
CMZ x CMU Civet Behavioral Monitoring Project
Author: Subagent 7 (Independent Camera Logger & Extractor)

Purpose:
  Runs YOLOv8 detection and camera-specific feature/ROI extraction independently
  on a single camera stream, producing standardized log_cam{N}.csv without
  requiring real-time lockstep synchronization between 4 cameras.
"""

import os
import sys
import cv2
import json
import argparse
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any

# ==============================================================================
# Camera-Specific Spatial Regions of Interest (ROIs)
# Standardized to 1920x1080 resolution (or scaled proportionally)
# ==============================================================================
CAMERA_ROIS = {
    "cam1": {
        "room_name": "Room 1",
        "description": "Corridor & Simulated Tree Stump",
        "stump_roi": [400, 200, 900, 700],        # [x1, y1, x2, y2]
        "doorway_1_2_roi": [1400, 300, 1920, 900],
        "ramp_corridor_roi": [200, 400, 1200, 1000]
    },
    "cam2": {
        "room_name": "Room 2",
        "description": "Dining Area & Indoor Wooden Sleeping Box",
        "sleeping_box_roi": [300, 60, 750, 350],   # Upper-right wooden box aperture
        "ramp_roi": [100, 350, 450, 700],          # Ramp leading from floor to box
        "food_tray_roi": [960, 740, 1340, 1060],   # Morning meat/feed tray area
        "doorway_2_3_roi": [50, 400, 250, 800]
    },
    "cam3": {
        "room_name": "Room 3",
        "description": "Enrichment Playground & Sand Floor",
        "food_tray_roi": [630, 440, 810, 610],     # Empirically verified by Subagent 3
        "tire_bed_roi": [820, 130, 1180, 420],     # Rubber tire bed filled with straw
        "climbing_log_roi": [500, 300, 1200, 650], # Center log
        "under_log_roi": [1380, 350, 1780, 650],   # Right fence log shelter
        "doorway_3_2_roi": [50, 300, 250, 600],
        "doorway_3_4_roi": [1650, 400, 1900, 800]
    },
    "cam4": {
        "room_name": "Room 4",
        "description": "Water Station & Perimeter Boundary",
        "water_basin_roi": [595, 565, 795, 740],   # Empirically verified concrete water basin by Subagent 4
        "doorway_4_3_roi": [1400, 400, 1920, 850],
        "perimeter_shelf_roi": [978, 100, 1252, 427]
    }
}


def point_in_bbox(px: float, py: float, box: List[int]) -> bool:
    """Checks if point (px, py) falls inside box [x1, y1, x2, y2]."""
    x1, y1, x2, y2 = box
    return x1 <= px <= x2 and y1 <= py <= y2


def bbox_overlap_ratio(boxA: List[float], boxB: List[int]) -> float:
    """Computes Intersection-over-Area of boxA with target ROI boxB."""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    inter_w = max(0, xB - xA)
    inter_h = max(0, yB - yA)
    inter_area = inter_w * inter_h
    boxA_area = max(1.0, (boxA[2] - boxA[0]) * (boxA[3] - boxA[1]))
    return inter_area / boxA_area


def seconds_to_timestamp(sec: float) -> str:
    """Converts seconds from midnight into HH:MM:SS.sss."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


class CameraBatchExtractor:
    def __init__(
        self,
        camera_id: int,
        weights_path: str,
        output_csv: str,
        sampling_fps: float = 2.0,
        conf_threshold: float = 0.35,
        device: str = "cpu"
    ):
        self.camera_id = camera_id
        self.cam_key = f"cam{camera_id}"
        self.rois = CAMERA_ROIS.get(self.cam_key, {})
        self.weights_path = weights_path
        self.output_csv = output_csv
        self.sampling_fps = sampling_fps
        self.sample_stride_sec = 1.0 / sampling_fps
        self.conf_threshold = conf_threshold
        self.device = device
        
        self.model = None
        self._init_model()

    def _init_model(self):
        """Loads fine-tuned YOLOv8 model."""
        if os.path.exists(self.weights_path):
            from ultralytics import YOLO
            print(f"[Cam {self.camera_id}] Loading YOLO model from {self.weights_path} on {self.device}...")
            self.model = YOLO(self.weights_path)
        else:
            print(f"[Cam {self.camera_id}] WARNING: Weights not found at {self.weights_path}. Running mock extraction.")
            self.model = None

    def process_video_stream(self, video_files_with_offsets: List[Tuple[str, float]]):
        """
        Processes an ordered sequence of video files for this camera.
        video_files_with_offsets: list of (video_filepath, start_second_of_day)
        """
        os.makedirs(os.path.dirname(os.path.abspath(self.output_csv)), exist_ok=True)
        
        headers = self._get_csv_headers()
        import csv
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(headers)
            
            prev_centroid = None
            prev_sec = None
            
            for vpath, start_offset_sec in video_files_with_offsets:
                if not os.path.exists(vpath):
                    print(f"[Cam {self.camera_id}] Video file not found: {vpath}, skipping.")
                    continue
                    
                cap = cv2.VideoCapture(vpath)
                native_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                dur_sec = total_frames / native_fps
                
                print(f"[Cam {self.camera_id}] Ingesting {os.path.basename(vpath)}: {dur_sec:.1f}s at {native_fps:.2f} FPS...")
                
                frame_step = max(1, int(native_fps * self.sample_stride_sec))
                current_frame_idx = 0
                
                while current_frame_idx < total_frames:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_idx)
                    ret, frame = cap.read()
                    if not ret:
                        break
                        
                    current_rel_sec = current_frame_idx / native_fps
                    current_global_sec = start_offset_sec + current_rel_sec
                    
                    # Inference
                    civet_found = False
                    best_conf = 0.0
                    best_bbox = [0, 0, 0, 0]
                    centroid = (0.0, 0.0)
                    velocity = 0.0
                    
                    if self.model is not None:
                        results = self.model.predict(
                            source=frame,
                            conf=self.conf_threshold,
                            device=self.device,
                            verbose=False
                        )
                        for r in results:
                            boxes = r.boxes
                            if len(boxes) > 0:
                                # Find highest confidence civet
                                for b in boxes:
                                    conf_val = float(b.conf[0])
                                    if conf_val > best_conf:
                                        best_conf = conf_val
                                        best_bbox = [float(x) for x in b.xyxy[0]]
                                        civet_found = True
                    
                    if civet_found:
                        cx = (best_bbox[0] + best_bbox[2]) / 2.0
                        cy = (best_bbox[1] + best_bbox[3]) / 2.0
                        centroid = (cx, cy)
                        
                        # Velocity calculation (Euclidean displacement / dt)
                        if prev_centroid is not None and prev_sec is not None:
                            dt = max(1e-3, current_global_sec - prev_sec)
                            dist = np.sqrt((cx - prev_centroid[0])**2 + (cy - prev_centroid[1])**2)
                            velocity = dist / dt
                        
                        prev_centroid = centroid
                        prev_sec = current_global_sec
                    else:
                        prev_centroid = None
                        prev_sec = None
                    
                    # Build camera-specific log row
                    row = self._build_camera_row(
                        global_sec=current_global_sec,
                        frame_idx=current_frame_idx,
                        civet_found=civet_found,
                        conf=best_conf,
                        bbox=best_bbox,
                        centroid=centroid,
                        velocity=velocity
                    )
                    writer.writerow(row)
                    
                    current_frame_idx += frame_step
                    
                cap.release()
                
        print(f"[Cam {self.camera_id}] Extraction complete. Saved to: {self.output_csv}")

    def _get_csv_headers(self) -> List[str]:
        base = [
            "timestamp", "global_sec", "frame_idx", "civet_present",
            "confidence", "x1", "y1", "x2", "y2", "cx", "cy", "velocity_px_s"
        ]
        if self.camera_id == 1:
            return base + ["in_stump_roi", "in_corridor_roi", "in_doorway1_2", "motion_state"]
        elif self.camera_id == 2:
            return base + ["in_box_roi", "in_ramp_roi", "in_food_tray_roi", "in_doorway2_3", "room2_state"]
        elif self.camera_id == 3:
            return base + ["in_food_tray_roi", "in_tire_bed_roi", "in_climbing_log_roi", "in_under_log_roi", "room3_state"]
        elif self.camera_id == 4:
            return base + ["in_water_basin_roi", "in_perimeter_roi", "in_doorway4_3", "room4_state"]
        return base

    def _build_camera_row(
        self, global_sec: float, frame_idx: int, civet_found: bool,
        conf: float, bbox: List[float], centroid: Tuple[float, float], velocity: float
    ) -> List[Any]:
        t_str = seconds_to_timestamp(global_sec)
        cx, cy = centroid
        base = [
            t_str, f"{global_sec:.2f}", frame_idx, 1 if civet_found else 0,
            f"{conf:.3f}", f"{bbox[0]:.1f}", f"{bbox[1]:.1f}", f"{bbox[2]:.1f}", f"{bbox[3]:.1f}",
            f"{cx:.1f}", f"{cy:.1f}", f"{velocity:.2f}"
        ]
        
        if not civet_found:
            extras = [0] * (len(self._get_csv_headers()) - len(base) - 1) + ["ABSENT"]
            return base + extras

        # Specific Camera Logic
        if self.camera_id == 1:
            in_stump = 1 if point_in_bbox(cx, cy, self.rois["stump_roi"]) else 0
            in_corr = 1 if point_in_bbox(cx, cy, self.rois["ramp_corridor_roi"]) else 0
            in_door = 1 if point_in_bbox(cx, cy, self.rois["doorway_1_2_roi"]) else 0
            m_state = "LOCOMOTION" if velocity >= 20.0 else "PAUSE"
            return base + [in_stump, in_corr, in_door, m_state]

        elif self.camera_id == 2:
            in_box = 1 if point_in_bbox(cx, cy, self.rois["sleeping_box_roi"]) else 0
            in_ramp = 1 if point_in_bbox(cx, cy, self.rois["ramp_roi"]) else 0
            in_food = 1 if point_in_bbox(cx, cy, self.rois["food_tray_roi"]) else 0
            in_door = 1 if point_in_bbox(cx, cy, self.rois["doorway_2_3_roi"]) else 0
            
            r2_state = "LOCOMOTION"
            if in_food and velocity < 15.0:
                r2_state = "FEEDING_CANDIDATE"
            elif in_box:
                r2_state = "BOX_REST_CANDIDATE"
            elif in_ramp and velocity < 15.0:
                r2_state = "RAMP_REST_CANDIDATE"
            return base + [in_box, in_ramp, in_food, in_door, r2_state]

        elif self.camera_id == 3:
            in_food = 1 if point_in_bbox(cx, cy, self.rois["food_tray_roi"]) else 0
            in_tire = 1 if point_in_bbox(cx, cy, self.rois["tire_bed_roi"]) else 0
            in_log = 1 if point_in_bbox(cx, cy, self.rois["climbing_log_roi"]) else 0
            in_under = 1 if point_in_bbox(cx, cy, self.rois["under_log_roi"]) else 0
            
            r3_state = "LOCOMOTION"
            if in_food and velocity < 15.0:
                r3_state = "FEEDING_FRUIT_CANDIDATE"
            elif in_tire and velocity < 15.0:
                r3_state = "TIRE_SLEEP_CANDIDATE"
            elif in_under and velocity < 15.0:
                r3_state = "UNDER_LOG_REST_CANDIDATE"
            elif velocity < 10.0:
                r3_state = "SAND_NAP_CANDIDATE"
            return base + [in_food, in_tire, in_log, in_under, r3_state]

        elif self.camera_id == 4:
            in_water = 1 if point_in_bbox(cx, cy, self.rois["water_basin_roi"]) else 0
            in_perim = 1 if point_in_bbox(cx, cy, self.rois["perimeter_shelf_roi"]) else 0
            in_door = 1 if point_in_bbox(cx, cy, self.rois["doorway_4_3_roi"]) else 0
            
            r4_state = "LOCOMOTION"
            if in_water and velocity < 15.0:
                r4_state = "DRINKING_CANDIDATE"
            return base + [in_water, in_perim, in_door, r4_state]

        return base


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run independent camera batch extractor")
    parser.add_argument("--cam", type=int, required=True, choices=[1, 2, 3, 4], help="Camera ID (1 to 4)")
    parser.add_argument("--weights", type=str, default="models/yolov8n_civet_phase2/weights/best.pt")
    parser.add_argument("--fps", type=float, default=2.0, help="Sampling FPS (1.0 or 2.0 recommended)")
    parser.add_argument("--out", type=str, default=None, help="Output CSV path")
    args = parser.parse_args()

    out_csv = args.out or f"finish/log_cam{args.cam}.csv"
    extractor = CameraBatchExtractor(
        camera_id=args.cam,
        weights_path=args.weights,
        output_csv=out_csv,
        sampling_fps=args.fps
    )
    print(f"Extractor initialized for Camera {args.cam} at {args.fps} FPS -> {out_csv}")
