import cv2
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
raw_cctv_dir = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ")
out_dir = os.path.join(project_root, "dataset", "robo")

os.makedirs(out_dir, exist_ok=True)

# 1. Remove faulty clips
faulty = [
    "03_civet_resting_tire_bed_day.mp4",
    "04_civet_morning_feeding_cam2_day.mp4"
]
for f in faulty:
    p = os.path.join(out_dir, f)
    if os.path.exists(p):
        os.remove(p)
        print(f"Deleted faulty file: {f}")

# 2. Extract new verified clips
new_clips = [
    {
        "id": "03_civet_resting_shelf_day.mp4",
        "cam": "camera 2",
        "file": "A02_05.55-09.51_dur_3h56m.mp4",
        "start_sec": 900,  # 06:10:00 (curled up sleeping peacefully on platform shelf)
        "duration_sec": 45,
        "description": "Civet sleeping on wooden shelf (Camera 02 Day Color - 06:10)",
        "behavior": "RESTING"
    },
    {
        "id": "03_civet_resting_sand_nap_night_ir.mp4",
        "cam": "camera 3",
        "file": "A03_00.00-06.56_dur_6h56m.mp4",
        "start_sec": 5380,  # 01:29:40 (lying flat and motionless on sand floor)
        "duration_sec": 45,
        "description": "Civet sleeping flat on sand bed (Camera 03 Night IR - 01:29)",
        "behavior": "RESTING"
    },
    {
        "id": "04_civet_eating_fruit_tray_peak_day.mp4",
        "cam": "camera 3",
        "file": "A03_14.03-18.18_dur_4h14m.mp4",
        "start_sec": 5760,  # 15:39:20 (peak active feeding chewing fruit chunks)
        "duration_sec": 50,
        "description": "Civet peak fruit feeding inside tray (Camera 03 Day Color - 15:39)",
        "behavior": "EATING"
    }
]

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for cfg in new_clips:
    src_path = os.path.join(raw_cctv_dir, cfg["cam"], cfg["file"])
    dst_path = os.path.join(out_dir, cfg["id"])
    
    print(f"\nExtracting: {cfg['id']}")
    print(f"  Source: {src_path}")
    print(f"  Start: {cfg['start_sec']}s | Duration: {cfg['duration_sec']}s")
    
    if not os.path.exists(src_path):
        print(f"  [ERROR] Source not found: {src_path}")
        continue
        
    cap = cv2.VideoCapture(src_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    start_f = int(cfg["start_sec"] * fps)
    total_f = int(cfg["duration_sec"] * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_f)
    writer = cv2.VideoWriter(dst_path, fourcc, fps, (w, h))
    
    written = 0
    t0 = time.time()
    for i in range(total_f):
        ret, frame = cap.read()
        if not ret:
            print(f"  [WARN] Stream ended at frame {i}")
            break
        writer.write(frame)
        written += 1
        
        if (i + 1) % 250 == 0:
            print(f"    Progress: {i + 1}/{total_f} frames ({(i + 1)/total_f*100:.1f}%) in {time.time() - t0:.1f}s")
            
    cap.release()
    writer.release()
    
    sz_mb = os.path.getsize(dst_path) / (1024 * 1024)
    print(f"  [SUCCESS] Written {written} frames ({written/fps:.1f}s) -> {sz_mb:.2f} MB")

print("\nAll replacement Roboflow clips extracted successfully!")
