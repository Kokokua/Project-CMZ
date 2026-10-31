import cv2
import os
import sys
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

model = YOLO('models/yolov8n_civet_phase2/weights/best.pt')
base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 3"

vids = [
    'A03_00.00-06.56_dur_6h56m.mp4',
    'A03_06.56-10.54_dur_3h57m.mp4',
    'A03_10.54-11.06_dur_0h11m.mp4',
    'A03_11.07-14.03_dur_2h56m.mp4',
    'A03_14.03-18.18_dur_4h14m.mp4',
    'A03_18.18-02.12_dur_7h54m.mp4',
]

for vname in vids:
    vp = os.path.join(base_dir, vname)
    if not os.path.exists(vp): continue
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = int((n_frames / fps) / 60.0)
    print(f"\n=================== Scanning {vname} ({dur_min} mins) ===================")
    
    # Step every 5 minutes
    for m in range(0, dur_min, 5):
        sec = m * 60
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if not ret: break
        
        res = model.predict(frame, conf=0.30, verbose=False)[0]
        if len(res.boxes) > 0:
            for b in res.boxes:
                conf = float(b.conf[0])
                box = [round(x, 1) for x in b.xyxy[0].tolist()]
                print(f"  [{vname}] Min {m:3d} ({sec}s): conf={conf:.3f}, box={box}")
    cap.release()
print("\nScan completed.")
