import cv2
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

for cam in ["camera 1", "camera 2", "camera 3", "camera 4"]:
    cam_dir = os.path.join(base_dir, cam)
    if not os.path.exists(cam_dir): continue
    print(f"\n--- {cam.upper()} ---")
    files = sorted(os.listdir(cam_dir))
    for f in files:
        fp = os.path.join(cam_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS)
        n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        dur_min = (n_frames / fps) / 60.0 if fps > 0 else 0
        sz_mb = os.path.getsize(fp) / (1024 * 1024)
        cap.release()
        print(f"{f} | {w}x{h} @ {fps:.1f}fps | {dur_min:5.1f} min | {sz_mb:6.1f} MB")
