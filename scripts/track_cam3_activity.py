import cv2, os
import sys

sys.stdout.reconfigure(encoding='utf-8')

vpath = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 3\A03_00.00-06.56_dur_6h56m.mp4"
cap = cv2.VideoCapture(vpath)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

out_dir = r"pic/inspections/cam3_follow_after_cam2"
os.makedirs(out_dir, exist_ok=True)

# The civet walked into Room 3 around 37m40s (2260s)
# Let's inspect minutes 37, 38, 39, 40, 45, 50, 60, 75, 90, 120
for m in [37, 38, 39, 40, 42, 45, 50, 60, 75, 90, 120, 150, 180]:
    sec = m * 60
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(os.path.join(out_dir, f"cam3_min_{m:03d}.jpg"), frame)
        print(f"Saved cam3 at min {m}")
cap.release()
