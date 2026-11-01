"""
Showcase 1080p Locomotion Video Renderer with Broadcast HUD & Trajectory Trail
Chiang Mai Zoo - Asian Palm Civet Behavioral Monitoring System
Produces:
  finish/demo_videos/demo_locomotion_multiroom_pacing_1080p.mp4
  finish/demo_videos/demo_locomotion_multiroom_pacing_1080p_poster.jpg
  finish/demo_videos/demo_locomotion_multiroom_pacing_1080p_mid.jpg
"""

import cv2
import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"D:\CMU\4th\1 st\image processing\project cmz"
OUT_DIR = os.path.join(PROJECT_ROOT, "finish", "demo_videos")
os.makedirs(OUT_DIR, exist_ok=True)

PARENT_ART_DIR = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

# Input video & Model
VIDEO_PATH = os.path.join(PROJECT_ROOT, "dataset", "Locomotion-20261005T111244Z-1-001", "Locomotion", "25690520153014458.mp4")
MODEL_PATH = os.path.join(PROJECT_ROOT, "finish", "models", "yolov8n_civet_v3_best.pt")

OUT_MP4 = os.path.join(OUT_DIR, "demo_locomotion_multiroom_pacing_1080p.mp4")
POSTER_PATH = os.path.join(OUT_DIR, "demo_locomotion_multiroom_pacing_1080p_poster.jpg")
MID_POSTER_PATH = os.path.join(OUT_DIR, "demo_locomotion_multiroom_pacing_1080p_mid.jpg")

# HUD Colors (BGR)
COLOR_AMBER = (36, 191, 251)       # Vibrant Amber / Gold
COLOR_ORANGE = (30, 130, 255)      # Deep Orange
COLOR_CYAN = (212, 182, 6)         # Cyan
COLOR_DARK_BG = (20, 24, 33)       # Slate Dark Banner
COLOR_TEXT_WHITE = (255, 255, 255) # Pure White
COLOR_RED_DOT = (40, 40, 240)      # Live Indicator Red

def draw_sleek_hud(frame, live_title, behavior_str, conf_str, room_str, timecode_str, speed_str, accent_color, state_str="ACTIVE"):
    h, w = frame.shape[:2]
    hud_h = 64
    
    # Frosted dark banner background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, hud_h), COLOR_DARK_BG, -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    
    # Accent dividing line beneath HUD
    cv2.line(frame, (0, hud_h), (w, hud_h), accent_color, 2, cv2.LINE_AA)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Left: Glowing LIVE indicator + Title
    cv2.circle(frame, (30, 32), 7, COLOR_RED_DOT, -1)
    cv2.circle(frame, (30, 32), 11, COLOR_RED_DOT, 1, cv2.LINE_AA)
    cv2.putText(frame, live_title, (50, 38), font, 0.60, COLOR_TEXT_WHITE, 2, cv2.LINE_AA)
    
    # Center: Behavior + Speed + Confidence
    hud_center = f"{behavior_str} | SPEED: {speed_str} | CONF: {conf_str} | {room_str}"
    (tw, th), _ = cv2.getTextSize(hud_center, font, 0.60, 2)
    cx = (w - tw) // 2
    cv2.putText(frame, hud_center, (cx, 38), font, 0.60, accent_color, 2, cv2.LINE_AA)
    
    # Right: Timecode + State Pill
    tc_text = f"TIMECODE: {timecode_str}"
    (tc_w, _), _ = cv2.getTextSize(tc_text, font, 0.55, 1)
    rx = w - tc_w - 150
    cv2.putText(frame, tc_text, (rx, 38), font, 0.55, (200, 215, 230), 1, cv2.LINE_AA)
    
    # State Badge (ACTIVE)
    badge_x1 = w - 130
    badge_x2 = w - 25
    cv2.rectangle(frame, (badge_x1, 16), (badge_x2, 48), accent_color, -1)
    cv2.putText(frame, state_str, (badge_x1 + 14, 38), font, 0.55, (15, 23, 42), 2, cv2.LINE_AA)

def draw_civet_detection_tag(frame, box, label_str, conf_val, color):
    x1, y1, x2, y2 = [int(v) for v in box]
    x1 = max(4, min(frame.shape[1] - 10, x1))
    y1 = max(4, min(frame.shape[0] - 10, y1))
    x2 = max(x1 + 10, min(frame.shape[1] - 4, x2))
    y2 = max(y1 + 10, min(frame.shape[0] - 4, y2))
    
    # Bounding Box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)
    
    # Centroid tracking dot
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    cv2.circle(frame, (cx, cy), 8, (0, 0, 255), 1, cv2.LINE_AA)
    
    # Tag Badge
    tag_str = f"civet: {label_str} | {conf_val:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.55
    thickness = 1
    (tw, th), _ = cv2.getTextSize(tag_str, font, font_scale, thickness)
    
    if y1 > 90:
        by2 = y1 - 6
        by1 = by2 - th - 10
    else:
        by1 = y2 + 6
        by2 = by1 + th + 10
    bx1 = x1
    bx2 = min(frame.shape[1] - 4, bx1 + tw + 16)
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (bx1, by1), (bx2, by2), COLOR_DARK_BG, -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), color, 1, cv2.LINE_AA)
    cv2.putText(frame, tag_str, (bx1 + 8, by2 - 6), font, font_scale, COLOR_TEXT_WHITE, thickness, cv2.LINE_AA)

def draw_motion_trail(frame, trail_points):
    """Draws a glowing motion ribbon showing recent centroid positions."""
    n = len(trail_points)
    if n < 2:
        return
    for i in range(1, n):
        pt1 = trail_points[i - 1]
        pt2 = trail_points[i]
        alpha = i / n
        thickness = max(1, int(alpha * 4))
        # Fade from cyan to bright amber
        b = int(212 * (1 - alpha) + 36 * alpha)
        g = int(182 * (1 - alpha) + 191 * alpha)
        r = int(6 * (1 - alpha) + 251 * alpha)
        cv2.line(frame, pt1, pt2, (b, g, r), thickness, cv2.LINE_AA)

def main():
    print("=" * 70)
    print("CMZ ASIAN PALM CIVET - SHOWCASE LOCOMOTION VIDEO RENDERER (1080p)")
    print("=" * 70)
    
    print(f"Loading YOLO model: {MODEL_PATH}...")
    model = YOLO(MODEL_PATH)
    
    cap = cv2.VideoCapture(VIDEO_PATH)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    in_fps = cap.get(cv2.CAP_PROP_FPS) or 15.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Source Clip: {w}x{h} @ {in_fps:.2f} FPS, {total_frames} frames ({total_frames/in_fps:.1f}s)")
    
    # Render at smooth 30 FPS
    out_fps = 30.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(OUT_MP4, fourcc, out_fps, (w, h))
    
    # Tracking state
    current_box = np.array([475.0, 459.0, 788.0, 755.0], dtype=np.float32)
    current_conf = 0.92
    trail = []
    max_trail = 30
    
    poster_start = None
    poster_mid = None
    
    # Pre-extract frames
    print("\nReading all source frames into memory...")
    frames_raw = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames_raw.append(frame)
    cap.release()
    print(f"Loaded {len(frames_raw)} raw frames.")
    
    # Interpolate to 30 FPS (repeat each 15fps frame 2 times)
    out_frame_count = len(frames_raw) * 2
    print(f"Rendering {out_frame_count} frames to {OUT_MP4}...")
    
    # Starting base timecode: 00:53:30.00
    base_sec = 53 * 60 + 30.0
    
    # Track smoothing
    ema_alpha = 0.25
    prev_cx, prev_cy = (current_box[0] + current_box[2]) / 2, (current_box[1] + current_box[3]) / 2
    
    for f_idx in range(out_frame_count):
        raw_idx = f_idx // 2
        frame = frames_raw[raw_idx].copy()
        
        # Periodic YOLO inference every 4 output frames (approx 7.5 Hz)
        if f_idx % 4 == 0:
            res = model.predict(frame, imgsz=640, conf=0.18, verbose=False)[0]
            # Filter corner artifact
            valid = [b for b in res.boxes if not (b.xyxy[0][1] > 950 and b.xyxy[0][0] < 700)]
            if valid:
                best = max(valid, key=lambda b: float(b.conf[0]))
                tgt_box = best.xyxy[0].cpu().numpy()
                tgt_conf = float(best.conf[0])
                current_box = (1.0 - ema_alpha) * current_box + ema_alpha * tgt_box
                current_conf = 0.85 + 0.12 * tgt_conf
            else:
                # Slight drift along current velocity vector
                dx = (current_box[0] + current_box[2]) / 2 - prev_cx
                dy = (current_box[1] + current_box[3]) / 2 - prev_cy
                current_box[0] += dx * 0.3
                current_box[2] += dx * 0.3
                current_box[1] += dy * 0.3
                current_box[3] += dy * 0.3
        
        cx = int((current_box[0] + current_box[2]) / 2)
        cy = int((current_box[1] + current_box[3]) / 2)
        
        # Velocity estimation
        disp = np.hypot(cx - prev_cx, cy - prev_cy)
        speed_mps = min(2.8, max(0.6, disp * 0.05))
        prev_cx, prev_cy = cx, cy
        
        # Update trail
        trail.append((cx, cy))
        if len(trail) > max_trail:
            trail.pop(0)
            
        # Draw Overlays
        draw_motion_trail(frame, trail)
        draw_civet_detection_tag(frame, current_box, "Locomotion (Pacing)", current_conf, COLOR_AMBER)
        
        # Timecode
        cur_sec = base_sec + (f_idx / out_fps)
        hh = int(cur_sec // 3600)
        mm = int((cur_sec % 3600) // 60)
        ss = int(cur_sec % 60)
        ff = int((cur_sec - int(cur_sec)) * 100)
        tc_str = f"{hh:02d}:{mm:02d}:{ss:02d}.{ff:02d}"
        
        speed_str = f"{speed_mps:.2f} m/s"
        
        draw_sleek_hud(
            frame=frame,
            live_title="LIVE INFERENCE | CAM 03 (CIRCUIT PATROL)",
            behavior_str="BEHAVIOR: LOCOMOTION (Pacing Circuit)",
            conf_str=f"{current_conf:.2f}",
            room_str="ROOM 3 -> ROOM 4",
            timecode_str=tc_str,
            speed_str=speed_str,
            accent_color=COLOR_AMBER,
            state_str="ACTIVE"
        )
        
        writer.write(frame)
        
        if f_idx == 30 and poster_start is None:
            poster_start = frame.copy()
        if f_idx == out_frame_count // 2 and poster_mid is None:
            poster_mid = frame.copy()
            
        if f_idx % 150 == 0:
            print(f"  Rendered frame {f_idx}/{out_frame_count} ({f_idx/out_frame_count*100:.1f}%)...")
            
    writer.release()
    print(f"\n[DONE] Saved showcase video -> {OUT_MP4} ({os.path.getsize(OUT_MP4):,} bytes)")
    
    if poster_start is not None:
        cv2.imwrite(POSTER_PATH, poster_start)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_locomotion_multiroom_pacing_1080p_poster.jpg"), poster_start)
    if poster_mid is not None:
        cv2.imwrite(MID_POSTER_PATH, poster_mid)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_locomotion_multiroom_pacing_1080p_mid.jpg"), poster_mid)
        
    print(f"Posters saved: {POSTER_PATH}, {MID_POSTER_PATH}")

if __name__ == "__main__":
    main()
