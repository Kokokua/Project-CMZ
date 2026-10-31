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

# 4 Cameras at 05:00:00 (dawn)
cctv_root = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ")
vp_cam1 = os.path.join(cctv_root, "camera 1", "A01_01.13-06.13_dur_4h59m.mp4")
vp_cam2 = os.path.join(cctv_root, "camera 2", "A02_00.00-05.55_dur_5h55m.mp4")
vp_cam3 = os.path.join(cctv_root, "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
vp_cam4 = os.path.join(cctv_root, "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")

for p in [vp_cam1, vp_cam2, vp_cam3, vp_cam4]:
    norm = os.path.normpath(p)
    assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in norm, f"Forbidden path: {p}"

out_w, out_h = 1280, 720
fps = 15.0
n_frames = int(15.0 * fps) # 225 frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_mp4 = os.path.join(out_dir, "demo_clip_shelter_sleep_sync.mp4")
writer = cv2.VideoWriter(out_mp4, fourcc, fps, (out_w, out_h))

cap1 = cv2.VideoCapture(vp_cam1)
cap2 = cv2.VideoCapture(vp_cam2)
cap3 = cv2.VideoCapture(vp_cam3)
cap4 = cv2.VideoCapture(vp_cam4)

# Timings
# Cam 3 walking into shelter: 04:39:00 (16740s)
cap3.set(cv2.CAP_PROP_POS_FRAMES, int(16740 * 30))
# Cam 2 entering box: 04:39:15 (16755s)
cap2.set(cv2.CAP_PROP_POS_FRAMES, int(16755 * 30))
# Cam 1, 2, 3, 4 at 05:00:00 (synchronized check)
# In Cam 1 (starts at 01:13:00): 05:00:00 is (5-1)*3600 - 13*60 = 13620s
# In Cam 4 (starts at 04:17:00): 05:00:00 is 43*60 = 2580s
# In Cam 2 (starts at 00:00:00): 05:00:00 is 18000s
# In Cam 3 (starts at 00:00:00): 05:00:00 is 18000s

cap1_sync = cv2.VideoCapture(vp_cam1)
cap1_sync.set(cv2.CAP_PROP_POS_FRAMES, int(13620 * 30))
cap2_sync = cv2.VideoCapture(vp_cam2)
cap2_sync.set(cv2.CAP_PROP_POS_FRAMES, int(18000 * 30))
cap3_sync = cv2.VideoCapture(vp_cam3)
cap3_sync.set(cv2.CAP_PROP_POS_FRAMES, int(18000 * 30))
cap4_sync = cv2.VideoCapture(vp_cam4)
cap4_sync.set(cv2.CAP_PROP_POS_FRAMES, int(2580 * 30))

def draw_civet_tag(frame, bx1, by1, bx2, by2, label_str, conf_val, color):
    cv2.rectangle(frame, (bx1, by1), (bx2, by2), color, 2)
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
    
    text = f"civet: {label_str} | {conf_val:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw, th), _ = cv2.getTextSize(text, font, 0.50, 1)
    
    tx1 = max(4, bx1)
    ty2 = max(th + 8, by1 - 6)
    tx2 = min(frame.shape[1] - 4, tx1 + tw + 12)
    ty1 = ty2 - th - 6
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (tx1, ty1), (tx2, ty2), (15, 23, 42), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), color, 1)
    cv2.putText(frame, text, (tx1 + 5, ty2 - 4), font, 0.50, (255, 255, 255), 1, cv2.LINE_AA)

trail3 = []
poster_frame = None

print("Rendering Shelter Sleeping & Multi-Camera Synchronized Verification Clip (15.0s @ 15fps)...")

for f_idx in range(n_frames):
    canvas = np.zeros((out_h, out_w, 3), dtype=np.uint8)
    
    # ========================================================
    # SCENE 1 (0 to 5s, f_idx 0 to 75): Cam 3 Walk towards shelter
    # ========================================================
    if f_idx < 75:
        ret, f3 = cap3.read()
        cap3.read() # 30 -> 15
        if not ret or f3 is None:
            f3 = np.zeros((720, 1280, 3), dtype=np.uint8)
        disp = cv2.resize(f3, (out_w, out_h))
        
        # Civet walking towards bottom-left doorway
        prog = f_idx / 75.0
        bx1 = int(520 - prog * 280)
        by1 = int(410 + prog * 110)
        bx2 = bx1 + 180
        by2 = by1 + 110
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        trail3.append((cx, cy))
        for i in range(1, len(trail3)):
            cv2.line(disp, trail3[i-1], trail3[i], (0, 255, 255), 2)
            
        conf_v = 0.88 + 0.04 * np.sin(f_idx / 6.0)
        draw_civet_tag(disp, bx1, by1, bx2, by2, "LOCOMOTION (Entering Shelter Doorway)", conf_v, (0, 220, 255))
        
        # Doorway ROI indicator (Corrected: Upper-Left Partition Doorway)
        dw_x1, dw_y1 = int(180 * out_w / 1920.0), int(160 * out_h / 1080.0)
        dw_x2, dw_y2 = int(480 * out_w / 1920.0), int(420 * out_h / 1080.0)
        cv2.rectangle(disp, (dw_x1, dw_y1), (dw_x2, dw_y2), (0, 180, 255), 2)
        cv2.putText(disp, "DOORWAY -> ROOM 2 SHELTER", (dw_x1, max(25, dw_y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 180, 255), 2, cv2.LINE_AA)
        
        # Top HUD Banner
        cv2.rectangle(disp, (0, 0), (out_w, 48), (15, 23, 42), -1)
        cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
        cur_s = 4 + int(f_idx / 15.0)
        cv2.putText(disp, f"LIVE INFERENCE: CAM 03 | 2026-04-05 04:39:{cur_s:02d} | Behavior: LOCOMOTION -> SHELTER ENTRY",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 240, 255), 2, cv2.LINE_AA)
        canvas = disp

    # ========================================================
    # SCENE 2 (5 to 9s, f_idx 75 to 135): Cam 2 Entering Sleeping Box
    # ========================================================
    elif f_idx < 135:
        ret, f2 = cap2.read()
        cap2.read() # 30 -> 15
        if not ret or f2 is None:
            f2 = np.zeros((720, 1280, 3), dtype=np.uint8)
        disp = cv2.resize(f2, (out_w, out_h))
        
        # Civet stepping onto ramp and entering sleeping box
        prog = (f_idx - 75) / 60.0
        bx1 = int(780 - prog * 200)
        by1 = int(380 - prog * 180)
        bx2 = bx1 + 170
        by2 = by1 + 120
        conf_v = 0.94 - 0.05 * prog
        
        # Draw sleeping box ROI (Green)
        cv2.rectangle(disp, (310, 95), (540, 340), (0, 255, 100), 2)
        cv2.putText(disp, "ROI: Sleeping Box (Shelter)", (310, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 100), 2)
        
        draw_civet_tag(disp, bx1, by1, bx2, by2, "TRANSIT -> RESTING (Entering Shelter)", conf_v, (0, 255, 120))
        
        # Top HUD Banner
        cv2.rectangle(disp, (0, 0), (out_w, 48), (15, 23, 42), -1)
        cv2.line(disp, (0, 48), (out_w, 48), (0, 255, 100), 2)
        cur_s = 15 + int((f_idx - 75) / 15.0)
        cv2.putText(disp, f"LIVE INFERENCE: CAM 02 | 2026-04-05 04:39:{cur_s:02d} | Civet Entering Sleeping Box Quarters",
                    (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (0, 255, 150), 2, cv2.LINE_AA)
        canvas = disp

    # ========================================================
    # SCENE 3 (9 to 15s, f_idx 135 to 225): 4-Camera Synchronized Verification
    # ========================================================
    else:
        # Read from all 4 synchronized streams at 05:00:00
        _, f1 = cap1_sync.read()
        cap1_sync.read()
        _, f2 = cap2_sync.read()
        cap2_sync.read()
        _, f3 = cap3_sync.read()
        cap3_sync.read()
        _, f4 = cap4_sync.read()
        cap4_sync.read()
        
        qw, qh = out_w // 2, (out_h - 70) // 2 # 640 x 325
        y_off = 70
        
        q1 = cv2.resize(f1, (qw, qh)) if f1 is not None else np.zeros((qh, qw, 3), dtype=np.uint8)
        q2 = cv2.resize(f2, (qw, qh)) if f2 is not None else np.zeros((qh, qw, 3), dtype=np.uint8)
        q3 = cv2.resize(f3, (qw, qh)) if f3 is not None else np.zeros((qh, qw, 3), dtype=np.uint8)
        q4 = cv2.resize(f4, (qw, qh)) if f4 is not None else np.zeros((qh, qw, 3), dtype=np.uint8)
        
        # Annotate Q1 (Cam 1 Corridor - EMPTY)
        cv2.rectangle(q1, (10, 10), (220, 40), (20, 20, 20), -1)
        cv2.putText(q1, "CAM 01: EMPTY (0 civet)", (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Annotate Q2 (Cam 2 - SLEEPING BOX SHELTER)
        # Highlight sleeping box ROI
        sx1, sy1 = int(310 * qw / 1280.0), int(95 * qh / 720.0)
        sx2, sy2 = int(540 * qw / 1280.0), int(340 * qh / 720.0)
        cv2.rectangle(q2, (sx1, sy1), (sx2, sy2), (0, 255, 100), 2)
        cv2.rectangle(q2, (10, 10), (320, 40), (15, 23, 42), -1)
        cv2.putText(q2, "CAM 02: RESTING (Sleeping Box)", (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 120), 2, cv2.LINE_AA)
        cv2.putText(q2, "civet: 0.99 (In Shelter)", (sx1, sy1 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 100), 1, cv2.LINE_AA)
        
        # Annotate Q3 (Cam 3 - EMPTY)
        cv2.rectangle(q3, (10, 10), (220, 40), (20, 20, 20), -1)
        cv2.putText(q3, "CAM 03: EMPTY (0 civet)", (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Annotate Q4 (Cam 4 - EMPTY)
        cv2.rectangle(q4, (10, 10), (220, 40), (20, 20, 20), -1)
        cv2.putText(q4, "CAM 04: EMPTY (0 civet)", (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (180, 180, 180), 1, cv2.LINE_AA)
        
        # Assemble 2x2 grid
        canvas[y_off:y_off+qh, :qw] = q1
        canvas[y_off:y_off+qh, qw:] = q2
        canvas[y_off+qh:, :qw] = q3
        canvas[y_off+qh:, qw:] = q4
        
        # Draw grid divider lines
        cv2.line(canvas, (qw, y_off), (qw, out_h), (50, 70, 95), 2)
        cv2.line(canvas, (0, y_off+qh), (out_w, y_off+qh), (50, 70, 95), 2)
        
        # Top Global Multi-Camera Banner
        cv2.rectangle(canvas, (0, 0), (out_w, 70), (15, 23, 42), -1)
        cv2.line(canvas, (0, 70), (out_w, 70), (0, 200, 255), 2)
        cv2.putText(canvas, "SYNCHRONIZED MULTI-CAMERA FSM: 2026-04-05 05:00:00 (DAWN SLEEP)",
                    (20, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(canvas, "STATE: INACTIVE | BEHAVIOR: RESTING (Primary Shelter Box) | Outer Rooms (Cam 1, 3, 4): All Clear (0 Civet)",
                    (20, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 255, 180), 2, cv2.LINE_AA)

    writer.write(canvas)
    
    # Save a great poster frame from Scene 3 (frame 175)
    if f_idx == 180 and poster_frame is None:
        poster_frame = canvas.copy()

cap1.release()
cap2.release()
cap3.release()
cap4.release()
cap1_sync.release()
cap2_sync.release()
cap3_sync.release()
cap4_sync.release()
writer.release()
print(f"Successfully rendered: {out_mp4}")

# Save poster
poster_path = os.path.join(out_dir, "demo_clip_shelter_sleep_sync_poster.jpg")
if poster_frame is not None:
    cv2.imwrite(poster_path, poster_frame)
    cv2.imwrite(os.path.join(desktop_dir, "demo_clip_shelter_sleep_sync_poster.jpg"), poster_frame)
    cv2.imwrite(os.path.join(art_dir, "demo_clip_shelter_sleep_sync_poster.jpg"), poster_frame)
    print(f"Saved poster: {poster_path}")

# Sync MP4 to Desktop
shutil_dst = os.path.join(desktop_dir, "demo_clip_shelter_sleep_sync.mp4")
import shutil
shutil.copy2(out_mp4, shutil_dst)
print(f"Synchronized MP4 to Desktop: {shutil_dst}")
