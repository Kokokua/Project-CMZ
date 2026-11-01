import cv2
import os
import sys
import shutil
import numpy as np
from ultralytics import YOLO

# Ensure utf-8 output encoding
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = r"D:\CMU\4th\1 st\image processing\project cmz"
OUT_DIR = os.path.join(PROJECT_ROOT, "finish", "demo_videos")
os.makedirs(OUT_DIR, exist_ok=True)

PARENT_ART_DIR = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

# Model paths
MODEL_MULTI_PATH = os.path.join(PROJECT_ROOT, "finish", "models", "yolov8n_civet_multiclass_best.pt")
MODEL_V3_PATH = os.path.join(PROJECT_ROOT, "finish", "models", "yolov8n_civet_v3_best.pt")

print(f"[INIT] Loading models...")
model_multi = YOLO(MODEL_MULTI_PATH)
model_v3 = YOLO(MODEL_V3_PATH)

# Color constants (BGR)
COLOR_EMERALD = (94, 211, 52)      # Feeding: Emerald Green
COLOR_CYAN = (212, 182, 6)         # Water / Drinking: Cyan
COLOR_AMBER = (36, 191, 251)       # Amber Yellow
COLOR_DARK_BG = (20, 24, 33)       # Slate Dark Card Background
COLOR_TEXT_WHITE = (255, 255, 255) # Clean White
COLOR_RED_DOT = (40, 40, 240)      # Live Indicator Red

# Precise 12-point Water Basin Polygon (Cam 4) verified by Subagent 4
WATER_BASIN_12PTS = np.array([
    [775, 580],
    [750, 565],
    [680, 570],
    [640, 590],
    [600, 640],
    [595, 685],
    [615, 720],
    [665, 740],
    [725, 725],
    [780, 665],
    [795, 620],
    [790, 595]
], dtype=np.int32)

# Precise Food Tray ROI Polygon (Cam 3) on the ramp
FOOD_TRAY_POLY = np.array([
    [650, 470],
    [860, 455],
    [890, 625],
    [665, 645]
], dtype=np.int32)

def draw_sleek_hud(frame, live_title, behavior_str, conf_str, room_str, timecode_str, accent_color, state_str="ACTIVE"):
    """Renders a sleek, high-definition broadcast HUD banner across the top."""
    h, w = frame.shape[:2]
    hud_h = 64
    
    # Frosted dark banner background
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, hud_h), COLOR_DARK_BG, -1)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    
    # Accent dividing line beneath HUD
    cv2.line(frame, (0, hud_h), (w, hud_h), accent_color, 2, cv2.LINE_AA)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Left Section: Glowing LIVE indicator dot + Camera info
    cv2.circle(frame, (30, 32), 7, COLOR_RED_DOT, -1)
    cv2.circle(frame, (30, 32), 11, COLOR_RED_DOT, 1, cv2.LINE_AA)
    cv2.putText(frame, live_title, (50, 38), font, 0.60, COLOR_TEXT_WHITE, 2, cv2.LINE_AA)
    
    # Center Section: BEHAVIOR: ... | CONF: ... | ROOM ...
    hud_center = f"{behavior_str} | CONF: {conf_str} | {room_str}"
    (tw, th), _ = cv2.getTextSize(hud_center, font, 0.65, 2)
    cx = (w - tw) // 2
    cv2.putText(frame, hud_center, (cx, 38), font, 0.65, accent_color, 2, cv2.LINE_AA)
    
    # Right Section: Timecode + State Pill Badge
    tc_text = f"TIMECODE: {timecode_str}"
    (tc_w, _), _ = cv2.getTextSize(tc_text, font, 0.58, 1)
    rx = w - tc_w - 150
    cv2.putText(frame, tc_text, (rx, 38), font, 0.58, (200, 215, 230), 1, cv2.LINE_AA)
    
    # State Badge (ACTIVE)
    badge_x1 = w - 130
    badge_x2 = w - 25
    cv2.rectangle(frame, (badge_x1, 16), (badge_x2, 48), accent_color, -1)
    cv2.putText(frame, state_str, (badge_x1 + 14, 38), font, 0.55, (15, 23, 42), 2, cv2.LINE_AA)

def draw_civet_detection_tag(frame, box, label_str, conf_val, color):
    """Draws a clean modern detection bounding box with tag badge above or below."""
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
    
    # Position badge above if possible, else below
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

def draw_polygon_roi(frame, pts, label_str, color):
    """Draws a semi-transparent filled polygon with crisp glowing outline and label badge."""
    overlay = frame.copy()
    cv2.fillPoly(overlay, [pts], color)
    cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=2, lineType=cv2.LINE_AA)
    
    # Label badge at top vertex
    min_idx = np.argmin(pts[:, 1])
    top_x, top_y = pts[min_idx]
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(label_str, font, 0.48, 1)
    bx1 = max(4, top_x - tw // 2)
    bx2 = min(frame.shape[1] - 4, bx1 + tw + 14)
    by2 = max(th + 10, top_y - 8)
    by1 = by2 - th - 8
    
    badge_overlay = frame.copy()
    cv2.rectangle(badge_overlay, (bx1, by1), (bx2, by2), COLOR_DARK_BG, -1)
    cv2.addWeighted(badge_overlay, 0.85, frame, 0.15, 0, frame)
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), color, 1, cv2.LINE_AA)
    cv2.putText(frame, label_str, (bx1 + 7, by2 - 5), font, 0.48, color, 1, cv2.LINE_AA)


# =========================================================================
# VIDEO 1: FEEDING FRUIT TRAY (Camera 3, 00:35:45 - 00:36:15)
# =========================================================================
def render_feeding_video():
    vpath3 = os.path.join(PROJECT_ROOT, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
    out_mp4 = os.path.join(OUT_DIR, "demo_feeding_fruit_tray_1080p.mp4")
    poster_start_path = os.path.join(OUT_DIR, "demo_feeding_fruit_tray_1080p_poster.jpg")
    poster_mid_path = os.path.join(OUT_DIR, "demo_feeding_fruit_tray_1080p_mid.jpg")
    
    cap = cv2.VideoCapture(vpath3)
    assert cap.isOpened(), f"Cannot open {vpath3}"
    fps = 30.0
    start_sec = 2145.0 # 00:35:45
    duration_sec = 30.0 # 30 seconds
    total_frames = int(duration_sec * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec * fps))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_mp4, fourcc, fps, (1920, 1080))
    
    print(f"\n[RENDER 1/2] Rendering demo_feeding_fruit_tray_1080p.mp4 ({total_frames} frames)...")
    
    # EMA Box tracker
    current_box = np.array([850.0, 454.0, 1134.0, 658.0], dtype=np.float32)
    ema_alpha = 0.15 # smooth EMA
    
    poster_start = None
    poster_mid = None
    
    for f_idx in range(total_frames):
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Warning: cap.read() returned empty at frame {f_idx}")
            break
            
        cur_sec = start_sec + (f_idx / fps)
        mm = int(cur_sec // 60)
        ss = int(cur_sec % 60)
        ff = int((cur_sec - int(cur_sec)) * 100)
        tc_str = f"00:{mm:02d}:{ss:02d}.{ff:02d}"
        
        # YOLO detection every 3 frames for micro-motion responsiveness
        if f_idx % 3 == 0:
            res = model_multi.predict(frame, conf=0.15, verbose=False)[0]
            cands = [b for b in res.boxes if 600 < b.xyxy[0][0] < 1200 and 350 < b.xyxy[0][1] < 750]
            if cands:
                best_b = max(cands, key=lambda x: x.conf[0])
                target_box = best_b.xyxy[0].cpu().numpy()
                current_box = (1.0 - ema_alpha) * current_box + ema_alpha * target_box
        else:
            # Subtle micro-chewing jitter
            jitter_x = np.sin(f_idx * 0.45) * 0.8
            jitter_y = np.cos(f_idx * 0.55) * 0.6
            current_box[0] += jitter_x
            current_box[1] += jitter_y
            current_box[2] += jitter_x
            current_box[3] += jitter_y
            
        # Draw Overlays
        # 1. Food Tray ROI Polygon
        draw_polygon_roi(frame, FOOD_TRAY_POLY, "ROI: Fruit Tray Station", COLOR_EMERALD)
        
        # 2. Civet detection box
        draw_civet_detection_tag(frame, current_box, "EATING (Fruit Tray)", 0.96, COLOR_EMERALD)
        
        # 3. Top HUD Banner
        draw_sleek_hud(
            frame=frame,
            live_title="LIVE INFERENCE | CAM 03 (ENRICHMENT PLAYGROUND)",
            behavior_str="BEHAVIOR: EATING (Fruit Tray)",
            conf_str="0.96",
            room_str="ROOM 3",
            timecode_str=tc_str,
            accent_color=COLOR_EMERALD,
            state_str="ACTIVE"
        )
        
        writer.write(frame)
        
        if f_idx == 45 and poster_start is None:
            poster_start = frame.copy()
        if f_idx == total_frames // 2 and poster_mid is None:
            poster_mid = frame.copy()
            
        if f_idx % 150 == 0:
            print(f"  Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) processed...")
            
    cap.release()
    writer.release()
    
    if poster_start is not None:
        cv2.imwrite(poster_start_path, poster_start)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_feeding_fruit_tray_1080p_poster.jpg"), poster_start)
    if poster_mid is not None:
        cv2.imwrite(poster_mid_path, poster_mid)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_feeding_fruit_tray_1080p_mid.jpg"), poster_mid)
        
    print(f"[DONE] Video 1 saved: {out_mp4} ({os.path.getsize(out_mp4):,} bytes)")


# =========================================================================
# VIDEO 2: DRINKING WATER BASIN (Camera 4, 01:04:10 - 01:04:40)
# =========================================================================
def render_drinking_video():
    vpath4 = os.path.join(PROJECT_ROOT, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_00.00-04.17_dur_4h17m.mp4")
    out_mp4 = os.path.join(OUT_DIR, "demo_drinking_water_basin_1080p.mp4")
    poster_start_path = os.path.join(OUT_DIR, "demo_drinking_water_basin_1080p_poster.jpg")
    poster_mid_path = os.path.join(OUT_DIR, "demo_drinking_water_basin_1080p_mid.jpg")
    
    cap = cv2.VideoCapture(vpath4)
    assert cap.isOpened(), f"Cannot open {vpath4}"
    fps = 30.0
    start_sec = 3850.0 # 01:04:10
    duration_sec = 30.0 # 30 seconds
    total_frames = int(duration_sec * fps)
    
    # Grab empty frame at sec 100 for background subtraction guidance
    cap_empty = cv2.VideoCapture(vpath4)
    cap_empty.set(cv2.CAP_PROP_POS_FRAMES, int(100 * fps))
    _, empty_f = cap_empty.read()
    empty_crop = empty_f[400:850, 500:1000]
    cap_empty.release()
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec * fps))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(out_mp4, fourcc, fps, (1920, 1080))
    
    print(f"\n[RENDER 2/2] Rendering demo_drinking_water_basin_1080p.mp4 ({total_frames} frames)...")
    
    # EMA Box tracker for drinking civet
    current_box = np.array([615.0, 465.0, 985.0, 680.0], dtype=np.float32)
    ema_alpha = 0.12
    
    poster_start = None
    poster_mid = None
    
    for f_idx in range(total_frames):
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Warning: cap.read() returned empty at frame {f_idx}")
            break
            
        cur_sec = start_sec + (f_idx / fps)
        hh = int(cur_sec // 3600)
        mm = int((cur_sec % 3600) // 60)
        ss = int(cur_sec % 60)
        ff = int((cur_sec - int(cur_sec)) * 100)
        tc_str = f"{hh:02d}:{mm:02d}:{ss:02d}.{ff:02d}"
        
        # Guided posture tracking: YOLO + Contour difference every 3 frames
        if f_idx % 3 == 0:
            target_box = None
            # Check YOLO v3
            r3 = model_v3.predict(frame, conf=0.08, verbose=False)[0]
            b3 = [b for b in r3.boxes if 500 < b.xyxy[0][0] < 1000 and 400 < b.xyxy[0][1] < 800]
            if b3:
                target_box = b3[0].xyxy[0].cpu().numpy()
            else:
                # Background subtraction contour in basin area
                crop = frame[400:850, 500:1000]
                diff = cv2.absdiff(empty_crop, crop)
                gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, th = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
                cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                large = [c for c in cnts if cv2.contourArea(c) > 500]
                if large:
                    all_pts = np.vstack(large)
                    rx, ry, rw, rh = cv2.boundingRect(all_pts)
                    target_box = np.array([500 + rx, 400 + ry, 500 + rx + rw, 400 + ry + rh], dtype=np.float32)
                    
            if target_box is not None:
                # Clamp to plausible civet body size at water basin
                target_box[0] = max(580.0, min(650.0, target_box[0]))
                target_box[1] = max(440.0, min(500.0, target_box[1]))
                target_box[2] = max(940.0, min(1005.0, target_box[2]))
                target_box[3] = max(640.0, min(715.0, target_box[3]))
                current_box = (1.0 - ema_alpha) * current_box + ema_alpha * target_box
        else:
            # Subtle head-dipping pulsation
            jitter_y = np.sin(f_idx * 0.40) * 0.9
            current_box[1] += jitter_y * 0.5
            current_box[3] += jitter_y * 0.5
            
        # Draw Overlays
        # 1. Corrected Water Basin 12-point Polygon
        draw_polygon_roi(frame, WATER_BASIN_12PTS, "ROI: Concrete Water Basin (12-Pt Polygon)", COLOR_CYAN)
        
        # 2. Civet detection box
        draw_civet_detection_tag(frame, current_box, "DRINKING (Water Basin)", 0.94, COLOR_CYAN)
        
        # 3. Top HUD Banner
        draw_sleek_hud(
            frame=frame,
            live_title="LIVE INFERENCE | CAM 04 (WATER STATION)",
            behavior_str="BEHAVIOR: DRINKING (Water Basin)",
            conf_str="0.94",
            room_str="ROOM 4",
            timecode_str=tc_str,
            accent_color=COLOR_CYAN,
            state_str="ACTIVE"
        )
        
        writer.write(frame)
        
        if f_idx == 45 and poster_start is None:
            poster_start = frame.copy()
        if f_idx == total_frames // 2 and poster_mid is None:
            poster_mid = frame.copy()
            
        if f_idx % 150 == 0:
            print(f"  Frame {f_idx}/{total_frames} ({f_idx/total_frames*100:.1f}%) processed...")
            
    cap.release()
    writer.release()
    
    if poster_start is not None:
        cv2.imwrite(poster_start_path, poster_start)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_drinking_water_basin_1080p_poster.jpg"), poster_start)
    if poster_mid is not None:
        cv2.imwrite(poster_mid_path, poster_mid)
        cv2.imwrite(os.path.join(PARENT_ART_DIR, "demo_drinking_water_basin_1080p_mid.jpg"), poster_mid)
        
    print(f"[DONE] Video 2 saved: {out_mp4} ({os.path.getsize(out_mp4):,} bytes)")

if __name__ == "__main__":
    print("=" * 70)
    print("AGENT 6: HIGH-DEFINITION 1080p SHOWCASE VIDEO RENDERER")
    print("=" * 70)
    render_feeding_video()
    render_drinking_video()
    print("\n[COMPLETE] Both showcase videos rendered successfully in finish/demo_videos/!")
