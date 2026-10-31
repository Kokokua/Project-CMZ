import cv2
import os
import sys
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz"
art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"
model_path = os.path.join(base_dir, "models", "yolov8n_civet_phase2", "weights", "best.pt")
model = YOLO(model_path)

vpath3 = os.path.join(base_dir, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
cap3 = cv2.VideoCapture(vpath3)

left_w, out_h = 820, 720
scale_x = left_w / 1920.0
scale_y = out_h / 1080.0

# Test seconds 16757 to 16764 (04:39:17 to 04:39:24)
print("Testing Cam 3 detection + scaling for left pane (820x720):")
for s in range(16757, 16765):
    cap3.set(cv2.CAP_PROP_POS_FRAMES, int(s * 30))
    ret, frame = cap3.read()
    if not ret: continue
    
    res = model.predict(frame, conf=0.20, verbose=False)[0]
    boxes = res.boxes.xyxy.cpu().numpy()
    confs = res.boxes.conf.cpu().numpy()
    
    # Filter for civet (exclude static background plant box [755, 607, 1040, 777])
    civet_boxes = []
    for b, c in zip(boxes, confs):
        x1, y1, x2, y2 = b
        # Check if it's the moving civet
        if y2 < 760 and not (x1 > 740 and x2 < 1060 and y1 > 590):
            civet_boxes.append((b, c))
            
    time_str = f"04:39:{s - 16757 + 17:02d}"
    print(f"Second {s} ({time_str}): {len(civet_boxes)} civet boxes")
    for b, c in civet_boxes:
        # Scale to 820x720
        sx1 = int(b[0] * scale_x)
        sy1 = int(b[1] * scale_y)
        sx2 = int(b[2] * scale_x)
        sy2 = int(b[3] * scale_y)
        print(f"   Raw 1920x1080: {list(map(int, b))}, Conf: {c:.2f} -> Scaled (820x720): [{sx1}, {sy1}, {sx2}, {sy2}]")

cap3.release()
