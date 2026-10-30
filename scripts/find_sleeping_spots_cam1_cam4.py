import cv2, os, glob
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"pic/inspections/civet_visits_cam1_cam4"
os.makedirs(out_dir, exist_ok=True)

# Let's get empty references
ref_cam1 = cv2.imread('pic/camera_samples/cam1_110705_sample.jpg')
ref_cam4 = cv2.imread('pic/camera_samples/cam4_110705_sample.jpg')

def scan_camera_with_ref(cam_name, ref_img):
    cam_dir = os.path.join(base_dir, cam_name)
    files = sorted([f for f in os.listdir(cam_dir) if f.endswith('.mp4')])
    print(f"\n==================== Scanning Activity in {cam_name.upper()} ====================")
    
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.GaussianBlur(ref_gray, (21, 21), 0)
    
    # We want to check the daytime files specifically first (where lighting matches)
    for f in files:
        # check daytime vs night
        parts = f.split('_')[1].split('-')
        start_h = int(parts[0].split('.')[0])
        # only check daytime files 06:00 to 18:00 for reliable color matching
        if start_h < 6 or start_h >= 18:
            continue
            
        fp = os.path.join(cam_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        dur_min = (n_frames / fps) / 60.0
        
        # sample every 10 seconds
        step = int(10 * fps)
        
        civet_detections = []
        
        for f_idx in range(0, n_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
            ret, frame = cap.read()
            if not ret: break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            diff = cv2.absdiff(ref_gray, gray)
            
            # exclude plants area if cam 4
            if cam_name == 'camera 4':
                diff[350:600, 1300:1550] = 0 # plant
            elif cam_name == 'camera 1':
                diff[0:400, 0:300] = 0 # plant on left
                
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
            
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for c in contours:
                area = cv2.contourArea(c)
                if area > 3500: # large animal
                    x, y, w, h = cv2.boundingRect(c)
                    sec = f_idx / fps
                    m = int(sec // 60)
                    s = int(sec % 60)
                    civet_detections.append((sec, m, s, area, (x, y, w, h)))
                    if len(civet_detections) <= 3:
                        out_p = os.path.join(out_dir, f"{cam_name}_{f[:7]}_{m:03d}m_{s:02d}s.jpg")
                        vis = frame.copy()
                        cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.imwrite(out_p, vis)
                        print(f"  [FOUND] {cam_name} in {f} at {m:02d}:{s:02d} -> Area={area:.0f}, BBox=({x},{y},{w},{h})")
                    break
                    
        cap.release()
        print(f"{f} ({dur_min:5.1f} min): detected civet in {len(civet_detections)} sampled frames")

print("Checking Camera 1...")
scan_camera_with_ref("camera 1", ref_cam1)

print("\nChecking Camera 4...")
scan_camera_with_ref("camera 4", ref_cam4)
