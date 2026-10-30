import cv2
import os
import glob
import sys
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

model_path = r'D:\CMU\4th\1 st\image processing\project cmz\models\yolov8n_civet_phase2\weights\best.pt'
model = YOLO(model_path)

# Let's inspect eating_1938_s15.jpg
img_path = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\eating_1938_s15.jpg'
if os.path.exists(img_path):
    img = cv2.imread(img_path)
    res = model.predict(img, conf=0.1, verbose=False)[0]
    print(f"Prediction on eating_1938_s15: {len(res.boxes)} boxes")
    for b in res.boxes:
        print(f"  Box: {b.xyxy.tolist()} conf: {float(b.conf):.3f}")

# Also let's check what is in Camera 4 files (which is the room with water basin)
cam4_dir = r'D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 4'
print("\nChecking Camera 4 videos for civet presence...")
for f in sorted(glob.glob(os.path.join(cam4_dir, '*.mp4'))):
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"File: {os.path.basename(f)} ({total/fps/60:.1f} mins)")
    # Sample every 60 seconds
    found_in_file = 0
    for sec in range(0, int(total/fps), 60):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if not ret: break
        res = model.predict(frame, conf=0.3, verbose=False)[0]
        if len(res.boxes) > 0:
            found_in_file += 1
            print(f"  Civet found at {sec//60}m:{sec%60}s in {os.path.basename(f)}, Conf: {float(res.boxes[0].conf):.2f}")
            out_name = f"pic/inspections/cam4_civet_{os.path.basename(f)[:3]}_{sec//60}m.jpg"
            cv2.imwrite(out_name, frame)
            if found_in_file >= 3:
                break
    cap.release()
