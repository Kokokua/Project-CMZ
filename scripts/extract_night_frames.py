import cv2
import os

base_dir = r'D:\CMU\4th\1 st\image processing\project cmz'
vpath = os.path.join(base_dir, 'dataset', 'ชะมดแผงสันหางดำ', 'camera 3', 'A03_18.18-02.12_dur_7h54m.mp4')
cap = cv2.VideoCapture(vpath)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

times = [
    (13*60 + 30, '13m30s'),
    (20*60 + 0, '20m00s'),
    (22*60 + 30, '22m30s'),
    (24*60 + 30, '24m30s'),
    (47*60 + 30, '47m30s')
]

out_dir = os.path.join(base_dir, 'pic', 'inspections')
os.makedirs(out_dir, exist_ok=True)

for sec, label in times:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
    ret, frame = cap.read()
    if ret:
        out_p = os.path.join(out_dir, f'cam3_night_{label}.jpg')
        cv2.imwrite(out_p, frame)
        print('Saved:', out_p)
cap.release()
