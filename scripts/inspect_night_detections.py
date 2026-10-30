import cv2
import os
import glob
from ultralytics import YOLO

base_dir = r'D:\CMU\4th\1 st\image processing\project cmz'
model = YOLO(os.path.join(base_dir, 'models', 'yolov8n_civet_phase2', 'weights', 'best.pt'))

for p in sorted(glob.glob(os.path.join(base_dir, 'pic', 'inspections', 'cam3_night_*.jpg'))):
    name = os.path.basename(p)
    img = cv2.imread(p)
    res = model.predict(img, conf=0.25, verbose=False)[0]
    print(f'=== {name} ({len(res.boxes)} boxes) ===')
    for b in res.boxes:
        print('  Box:', [round(x, 1) for x in b.xyxy[0].tolist()], 'Conf:', round(float(b.conf[0]), 3))
        # Draw box
        xy = [int(v) for v in b.xyxy[0].tolist()]
        cv2.rectangle(img, (xy[0], xy[1]), (xy[2], xy[3]), (0, 255, 0), 2)
        cv2.putText(img, f'civet: {float(b.conf[0]):.2f}', (xy[0], xy[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(base_dir, 'pic', 'inspections', f'annotated_{name}'), img)
