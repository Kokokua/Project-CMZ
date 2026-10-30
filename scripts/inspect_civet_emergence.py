import cv2
import os
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

vpath = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 2\A02_00.00-05.55_dur_5h55m.mp4"
cap = cv2.VideoCapture(vpath)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

out_dir = r"pic\civet_cam2_box_inspection\emergence"
os.makedirs(out_dir, exist_ok=True)

# Reference background (empty room at min 10)
cap.set(cv2.CAP_PROP_POS_FRAMES, int(10 * 60 * fps))
ret, bg_frame = cap.read()
bg_gray = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)
bg_gray = cv2.GaussianBlur(bg_gray, (21, 21), 0)

# Check from 35:00 to 38:00 every 5 seconds
print("Scanning from 35:00 to 38:00...")
for sec in range(35 * 60, 38 * 60 + 5, 5):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    diff = cv2.absdiff(bg_gray, gray)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    
    # Exclude plant noise: plant is roughly Y: 100..580, X: 800..1150
    # But let's check the ledge: X: 450..800 (left ledge), X: 1150..1600 (right ledge)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    large_contours = [c for c in contours if cv2.contourArea(c) > 800]
    
    m = sec // 60
    s = sec % 60
    
    civet_info = []
    vis = frame.copy()
    for c in large_contours:
        x, y, w, h = cv2.boundingRect(c)
        cx, cy = x + w // 2, y + h // 2
        area = cv2.contourArea(c)
        cv2.rectangle(vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
        civet_info.append(f"Box at ({x},{y},{w},{h}), cx={cx}, cy={cy}, area={area:.0f}")
        
    out_img = os.path.join(out_dir, f"emerge_{m:02d}m_{s:02d}s.jpg")
    cv2.imwrite(out_img, vis)
    print(f"Time {m:02d}:{s:02d} | Contours: {len(large_contours)} | {'; '.join(civet_info[:2])}")

cap.release()
