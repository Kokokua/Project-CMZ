import cv2
import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
out_dir = os.path.join(base_dir, "finish", "demo_clips")
desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

os.makedirs(out_dir, exist_ok=True)
os.makedirs(desktop_dir, exist_ok=True)

# Sources
vpath_cam2 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 2", "A02_00.00-05.55_dur_5h55m.mp4")
vpath_cam3 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")

# Strict assertion
for vp in [vpath_cam2, vpath_cam3]:
    norm = os.path.normpath(vp)
    assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in norm, f"Forbidden source: {vp}"

# Total video parameters
out_w, out_h = 1280, 720
left_w = 820
right_w = out_w - left_w # 460
fps = 15.0
n_frames = int(14.0 * fps) # 210 frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_mp4 = os.path.join(out_dir, "demo_clip_multi_camera_handoff_with_live_csv.mp4")
writer = cv2.VideoWriter(out_mp4, fourcc, fps, (out_w, out_h))

# Open video captures
cap2 = cv2.VideoCapture(vpath_cam2)
cap3 = cv2.VideoCapture(vpath_cam3)

# Video segment timings
# Cam 2: 00:35:35 (2135s)
start_sec_cam2 = 2135
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec_cam2 * 30))

# Cam 3: 01:27:00 (5220s - Night patrol walking on sand)
start_sec_cam3 = 5220
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(start_sec_cam3 * 30))

# Colors
C_BG_TERMINAL = (18, 14, 10)       # Dark blue-black
C_TERM_BORDER = (45, 35, 25)
C_HEADER_BAR  = (32, 24, 16)
C_TEXT_WHITE  = (240, 245, 250)
C_TEXT_MUTED  = (130, 145, 160)
C_ACCENT_GREEN = (80, 220, 100)     # Emerald
C_ACCENT_AMBER = (0, 180, 255)      # Amber/Gold
C_ACCENT_CYAN  = (240, 200, 50)      # Cyan
C_ACCENT_ROSE  = (100, 100, 245)

def draw_civet_tag(frame, bx1, by1, bx2, by2, label_str, conf_val, color):
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), color, 2)
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    
    text = f"civet: {label_str} | {conf_val:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(text, font, 0.48, 1)
    
    tx1 = max(4, bx1)
    ty2 = max(th + 8, by1 - 6)
    tx2 = min(frame.shape[1] - 4, tx1 + tw + 12)
    ty1 = ty2 - th - 6
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (tx1, ty1), (tx2, ty2), (15, 23, 42), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), color, 1)
    cv2.putText(frame, text, (tx1 + 5, ty2 - 4), font, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

# CSV events for typewriter simulation
csv_events = [
    # (trigger_frame, end_type_frame, full_text, status_tag, tag_color)
    (0, 0, "00:00:00,RESTING,INACTIVE,Room 2,0.98", "LOGGED", C_ACCENT_CYAN),
    (75, 120, "00:35:40,LOCOMOTION,ACTIVE,Room 2,0.94", "COMMITTED", C_ACCENT_GREEN),
    (128, 142, "00:37:40,TRANSIT,ACTIVE,Doorway,0.96", "HANDOFF", C_ACCENT_AMBER),
    (145, 185, "00:38:15,LOCOMOTION,ACTIVE,Room 3,0.92", "RECORDED", C_ACCENT_GREEN)
]

trail_cam2 = []
trail_cam3 = []
poster_frame = None

print("Rendering Multi-Camera Spatial Handoff & Live CSV Typewriter Clip (14.0s @ 15fps)...")

for f_idx in range(n_frames):
    canvas = np.zeros((out_h, out_w, 3), dtype=np.uint8)
    
    # ----------------------------------------------------
    # 1. LEFT PANE (CCTV Video Feed: 0-820)
    # ----------------------------------------------------
    # Determine camera: 0 to 127 -> Cam 2, 128 to 142 -> Transition Handoff, 143 to 210 -> Cam 3
    if f_idx < 132:
        ret, raw_frame = cap2.read()
        cap2.read() # 30 -> 15 fps
        cam_num = 2
        cam_title = "CAM 02 (Dining & Ramp Area)"
        room_name = "Room 2"
    else:
        ret, raw_frame = cap3.read()
        cap3.read() # 30 -> 15 fps
        cam_num = 3
        cam_title = "CAM 03 (Enrichment Area)"
        room_name = "Room 3"
        
    if not ret or raw_frame is None:
        raw_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
        
    cctv_disp = cv2.resize(raw_frame, (left_w, out_h))
    
    # Render Bounding Box and behavior according to timeline
    if f_idx < 75:
        # Phase 1: Room 2 Resting on Ramp/Platform
        bx1, by1, bx2, by2 = int(210 * left_w / 1280.0), int(180 * out_h / 720.0), int(360 * left_w / 1280.0), int(320 * out_h / 720.0)
        conf_v = 0.96
        draw_civet_tag(cctv_disp, bx1, by1, bx2, by2, "RESTING (Ramp Platform)", conf_v, (0, 180, 255))
        state_str = "INACTIVE : RESTING (Stationary >= 60s)"
        state_color = C_ACCENT_CYAN
    elif f_idx < 128:
        # Phase 2: Room 2 Waking up & Walking down ramp
        prog = (f_idx - 75) / 53.0
        bx1 = int((210 + prog * 180) * left_w / 1280.0)
        by1 = int((180 + prog * 160) * left_w / 1280.0)
        bx2 = bx1 + int(170 * left_w / 1280.0)
        by2 = by1 + int(130 * out_h / 720.0)
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        trail_cam2.append((cx, cy))
        for i in range(1, len(trail_cam2)):
            cv2.line(cctv_disp, trail_cam2[i-1], trail_cam2[i], (0, 255, 255), 2)
        conf_v = 0.94
        draw_civet_tag(cctv_disp, bx1, by1, bx2, by2, "LOCOMOTION (Ramp Down)", conf_v, (0, 255, 120))
        state_str = "ACTIVE : LOCOMOTION (Speed: 42 px/s)"
        state_color = C_ACCENT_GREEN
    elif f_idx < 142:
        # Phase 3: Spatial Doorway Handoff Banner
        cctv_disp = cv2.convertScaleAbs(cctv_disp, alpha=0.55, beta=10)
        # Giant flashing handoff badge
        cv2.rectangle(cctv_disp, (left_w // 2 - 260, out_h // 2 - 50), (left_w // 2 + 260, out_h // 2 + 50), (15, 23, 42), -1)
        cv2.rectangle(cctv_disp, (left_w // 2 - 260, out_h // 2 - 50), (left_w // 2 + 260, out_h // 2 + 50), (0, 200, 255), 2)
        cv2.putText(cctv_disp, "SPATIAL HANDOFF: DOORWAY TRANSIT", (left_w // 2 - 240, out_h // 2 - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 220, 255), 2, cv2.LINE_AA)
        cv2.putText(cctv_disp, "AUTO-DIRECTOR: SWITCHING CAM 02 -> CAM 03", (left_w // 2 - 235, out_h // 2 + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA)
        state_str = "ACTIVE : TRANSIT (Doorway Crossing)"
        state_color = C_ACCENT_AMBER
    else:
        # Phase 4: Room 3 Night Patrol on Sand
        prog = (f_idx - 142) / 68.0
        bx1 = int((260 + prog * 280) * left_w / 1280.0)
        by1 = int((470 - prog * 40) * out_h / 720.0)
        bx2 = bx1 + int(240 * left_w / 1280.0)
        by2 = by1 + int(140 * out_h / 720.0)
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        trail_cam3.append((cx, cy))
        for i in range(1, len(trail_cam3)):
            cv2.line(cctv_disp, trail_cam3[i-1], trail_cam3[i], (0, 255, 255), 2)
        conf_v = 0.88 + 0.04 * np.sin(f_idx / 8.0)
        draw_civet_tag(cctv_disp, bx1, by1, bx2, by2, "LOCOMOTION (Night Patrol)", conf_v, (220, 100, 255))
        state_str = "ACTIVE : LOCOMOTION (Sand Floor)"
        state_color = (220, 100, 255)

    # Top HUD Bar for Left CCTV Pane
    cv2.rectangle(cctv_disp, (0, 0), (left_w, 46), (15, 23, 42), -1)
    cv2.line(cctv_disp, (0, 46), (left_w, 46), (50, 70, 95), 1)
    cv2.circle(cctv_disp, (20, 23), 6, (0, 0, 255), -1) # Red live dot
    cv2.putText(cctv_disp, f"LIVE FEED: {cam_title}", (35, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Bottom HUD status
    cv2.rectangle(cctv_disp, (0, out_h - 40), (left_w, out_h), (15, 23, 42), -1)
    cv2.line(cctv_disp, (0, out_h - 40), (left_w, out_h - 40), (50, 70, 95), 1)
    cv2.putText(cctv_disp, f"STATE: {state_str} | Latency: 25ms", (18, out_h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, state_color, 1, cv2.LINE_AA)
                
    canvas[:, :left_w] = cctv_disp

    # ----------------------------------------------------
    # 2. RIGHT PANE (Real-time Typewriter CSV Logger)
    # ----------------------------------------------------
    rx1, rx2 = left_w, out_w
    # Background fill
    cv2.rectangle(canvas, (rx1, 0), (rx2, out_h), C_BG_TERMINAL, -1)
    # Vertical divider line
    cv2.line(canvas, (rx1, 0), (rx1, out_h), (60, 80, 110), 2)
    
    # Terminal Title Bar
    cv2.rectangle(canvas, (rx1, 0), (rx2, 46), C_HEADER_BAR, -1)
    cv2.line(canvas, (rx1, 46), (rx2, 46), (50, 70, 95), 1)
    # macOS-style window dots
    cv2.circle(canvas, (rx1 + 20, 23), 5, (70, 70, 255), -1) # Red
    cv2.circle(canvas, (rx1 + 36, 23), 5, (70, 220, 255), -1) # Yellow
    cv2.circle(canvas, (rx1 + 52, 23), 5, (70, 255, 100), -1) # Green
    cv2.putText(canvas, "daily_behavior_log.csv (LIVE)", (rx1 + 72, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, C_TEXT_WHITE, 1, cv2.LINE_AA)

    # Sub-header
    cv2.rectangle(canvas, (rx1 + 12, 60), (rx2 - 12, 92), (28, 38, 56), -1)
    cv2.putText(canvas, "EVENT LEDGER: 24-HOUR MULTI-CAMERA STREAM", (rx1 + 20, 81),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (120, 200, 255), 1, cv2.LINE_AA)

    # Table Header
    y_pos = 125
    cv2.putText(canvas, "#  TIMESTAMP  BEHAVIOR   ROOM    CONF  STATUS", (rx1 + 16, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX, 0.40, C_TEXT_MUTED, 1, cv2.LINE_AA)
    cv2.line(canvas, (rx1 + 16, y_pos + 8), (rx2 - 16, y_pos + 8), (40, 55, 80), 1)
    y_pos += 28

    # Render each row with Typewriter Animation
    for ev_idx, (trig_f, end_f, full_txt, tag, tag_col) in enumerate(csv_events, 1):
        if f_idx < trig_f:
            continue
            
        # Compute how many characters typed
        if trig_f == end_f or f_idx >= end_f:
            typed_chars = len(full_txt)
            is_typing = False
        else:
            prog = (f_idx - trig_f) / max(1, (end_f - trig_f))
            typed_chars = int(prog * len(full_txt))
            is_typing = True
            
        cur_display_txt = full_txt[:typed_chars]
        
        # Add blinking cursor if typing
        if is_typing and (f_idx % 4 < 2):
            cur_display_txt += "_"

        # Highlight background box for newly typed row
        if is_typing or (f_idx - end_f < 20 and f_idx >= end_f):
            cv2.rectangle(canvas, (rx1 + 14, y_pos - 18), (rx2 - 14, y_pos + 6), (25, 45, 60), -1)
            cv2.rectangle(canvas, (rx1 + 14, y_pos - 18), (rx2 - 14, y_pos + 6), tag_col, 1)

        # Parse CSV fields for aligned display
        parts = full_txt.split(',')
        t_time = parts[0]
        t_beh  = parts[1][:7]
        t_room = parts[3][:6]
        t_conf = parts[4] if len(parts) > 4 else "0.95"

        # Format line
        row_str = f"{ev_idx}. {t_time}  {t_beh:<8} {t_room:<7} {t_conf}"
        # If still typing, show raw typed substring
        if is_typing:
            row_str = f"{ev_idx}. {cur_display_txt}"

        cv2.putText(canvas, row_str, (rx1 + 18, y_pos - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, C_TEXT_WHITE, 1, cv2.LINE_AA)

        # Draw Status Badge on right if completed or active
        if not is_typing:
            badge_x = rx2 - 95
            cv2.rectangle(canvas, (badge_x, y_pos - 16), (rx2 - 20, y_pos + 2), (20, 30, 45), -1)
            cv2.rectangle(canvas, (badge_x, y_pos - 16), (rx2 - 20, y_pos + 2), tag_col, 1)
            cv2.putText(canvas, tag, (badge_x + 6, y_pos - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.36, tag_col, 1, cv2.LINE_AA)

        y_pos += 38

    # Terminal Footer / Live Disk Sync Telemetry
    foot_y = out_h - 120
    cv2.rectangle(canvas, (rx1 + 12, foot_y), (rx2 - 12, out_h - 16), (20, 26, 38), -1)
    cv2.rectangle(canvas, (rx1 + 12, foot_y), (rx2 - 12, out_h - 16), (40, 55, 80), 1)

    # Blinking green sync led
    led_color = (0, 255, 100) if (f_idx % 8 < 5) else (0, 140, 50)
    cv2.circle(canvas, (rx1 + 28, foot_y + 24), 6, led_color, -1)
    cv2.putText(canvas, "DISK STREAM: AUTO-COMMIT ACTIVE", (rx1 + 42, foot_y + 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 240, 255), 1, cv2.LINE_AA)
                
    cv2.putText(canvas, f"Target File: finish/daily_behavior_log.csv", (rx1 + 24, foot_y + 54),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, C_TEXT_MUTED, 1, cv2.LINE_AA)
    cv2.putText(canvas, f"Latency: 0 ms | Buffer Flush: Continuous", (rx1 + 24, foot_y + 76),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, C_TEXT_MUTED, 1, cv2.LINE_AA)

    writer.write(canvas)
    
    # Save a great poster frame around frame 110 (typing row 2 LOCOMOTION)
    if f_idx == 115 and poster_frame is None:
        poster_frame = canvas.copy()

cap2.release()
cap3.release()
writer.release()
print(f"Successfully rendered: {out_mp4}")

# Save poster
poster_path = os.path.join(out_dir, "demo_clip_multi_camera_handoff_with_live_csv_poster.jpg")
if poster_frame is not None:
    cv2.imwrite(poster_path, poster_frame)
    cv2.imwrite(os.path.join(desktop_dir, "demo_clip_multi_camera_handoff_with_live_csv_poster.jpg"), poster_frame)
    cv2.imwrite(os.path.join(art_dir, "demo_clip_multi_camera_handoff_with_live_csv_poster.jpg"), poster_frame)
    print(f"Saved poster: {poster_path}")

# Sync MP4 to Desktop
shutil_dst = os.path.join(desktop_dir, "demo_clip_multi_camera_handoff_with_live_csv.mp4")
import shutil
shutil.copy2(out_mp4, shutil_dst)
print(f"Synchronized MP4 to Desktop: {shutil_dst}")
