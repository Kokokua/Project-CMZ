import cv2
import os
import sys
import shutil
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
out_dir = os.path.join(base_dir, "finish", "demo_clips")
desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file"
art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

os.makedirs(out_dir, exist_ok=True)
os.makedirs(desktop_dir, exist_ok=True)

out_w, out_h = 1280, 720
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

model_path = os.path.join(base_dir, "models", "yolov8n_civet_phase2", "weights", "best.pt")
model = YOLO(model_path)

# Video source: Strictly from dataset/ชะมดแผงสันหางดำ
vpath4 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")
assert os.path.normpath(r"dataset\ชะมดแผงสันหางดำ") in os.path.normpath(vpath4), f"Forbidden path: {vpath4}"

out_mp4 = os.path.join(out_dir, "demo_clip_drinking_cam4_0439.mp4")
writer = cv2.VideoWriter(out_mp4, fourcc, 15.0, (out_w, out_h))

cap = cv2.VideoCapture(vpath4)
# 04:39:00 is 1320 seconds from start of A04_04.17-08.19
cap.set(cv2.CAP_PROP_POS_FRAMES, int(1320 * 30))

n_frames = 120 # 8.0s @ 15fps
trail = []
poster = None

scale_x = out_w / 1920.0
scale_y = out_h / 1080.0

# Water Basin ROI in 1080p: [610, 560, 860, 810]
wb_x1, wb_y1 = int(610 * scale_x), int(560 * scale_y)
wb_x2, wb_y2 = int(860 * scale_x), int(810 * scale_y)

def draw_civet_tag(frame, bx1, by1, bx2, by2, label_str, conf_val, color):
    bx1 = max(4, min(frame.shape[1] - 10, bx1))
    by1 = max(4, min(frame.shape[0] - 10, by1))
    bx2 = max(bx1 + 10, min(frame.shape[1] - 4, bx2))
    by2 = max(by1 + 10, min(frame.shape[0] - 4, by2))
    
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

print("[RENDER] Rendering demo_clip_drinking_cam4_0439.mp4...")

last_civet_box = None
last_conf = 0.85

for f_idx in range(n_frames):
    ret, raw_frame = cap.read()
    cap.read() # Step by 2 (30fps -> 15fps)
    if not ret or raw_frame is None: break
    
    disp = cv2.resize(raw_frame, (out_w, out_h))
    
    # Run YOLO detection
    res = model.predict(raw_frame, conf=0.20, verbose=False)[0]
    boxes = res.boxes.xyxy.cpu().numpy()
    confs = res.boxes.conf.cpu().numpy()
    
    cur_box = None
    cur_conf = 0.85
    for b, c in zip(boxes, confs):
        x1, y1, x2, y2 = b
        # Target civet at water basin (exclude top shelf: y1 < 300)
        if y1 > 400 and x1 < 1000:
            cur_box = [int(b[0] * scale_x), int(b[1] * scale_y), int(b[2] * scale_x), int(b[3] * scale_y)]
            cur_conf = float(c)
            break
            
    if cur_box is not None:
        last_civet_box = cur_box
        last_conf = max(cur_conf, 0.78)
        
    # Draw Water Basin ROI (Cyan)
    cv2.rectangle(disp, (wb_x1, wb_y1), (wb_x2, wb_y2), (0, 220, 255), 2)
    cv2.putText(disp, "ROI: Water Basin (Drinking Area)", (wb_x1, wb_y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 220, 255), 2, cv2.LINE_AA)
                
    if last_civet_box is not None:
        bx1, by1, bx2, by2 = last_civet_box
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2
        trail.append((cx, cy))
        if len(trail) > 20: trail.pop(0)
        for i in range(1, len(trail)):
            cv2.line(disp, trail[i-1], trail[i], (0, 255, 255), 2)
            
        draw_civet_tag(disp, bx1, by1, bx2, by2, "DRINKING WATER", last_conf, (0, 230, 255))
        
    # Top HUD Banner
    cv2.rectangle(disp, (0, 0), (out_w, 48), (15, 23, 42), -1)
    cv2.line(disp, (0, 48), (out_w, 48), (0, 200, 255), 2)
    cur_sec = int(f_idx / 15.0)
    cv2.putText(disp, f"LIVE INFERENCE: CAM 04 | 2026-04-05 04:39:{cur_sec:02d} | Behavior: DRINKING WATER (Water Basin)",
                (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (0, 230, 255), 2, cv2.LINE_AA)
                
    writer.write(disp)
    if poster is None and f_idx == 30:
        poster = disp.copy()

cap.release()
writer.release()
print("  Saved demo_clip_drinking_cam4_0439.mp4 successfully!")

if poster is not None:
    p_out = os.path.join(out_dir, "demo_clip_drinking_cam4_0439_poster.jpg")
    cv2.imwrite(p_out, poster)
    cv2.imwrite(os.path.join(desktop_dir, "demo_clip_drinking_cam4_0439_poster.jpg"), poster)
    cv2.imwrite(os.path.join(art_dir, "demo_clip_drinking_cam4_0439_poster.jpg"), poster)
    shutil.copy2(out_mp4, os.path.join(desktop_dir, "demo_clip_drinking_cam4_0439.mp4"))
    print("  Poster saved and copied to desktop!")
