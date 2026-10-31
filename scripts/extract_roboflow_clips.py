import cv2
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
raw_cctv_dir = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ")
out_dir = os.path.join(project_root, "dataset", "robo")

os.makedirs(out_dir, exist_ok=True)

clips_config = [
    {
        "id": "01_civet_eating_fruit_tray_day.mp4",
        "cam": "camera 3",
        "file": "A03_14.03-18.18_dur_4h14m.mp4",
        "start_sec": 5708,  # ~15:38:35 (fruit tray placed at 15:33:20, civet eats at 15:38:45)
        "duration_sec": 60,
        "description": "Afternoon Fruit Feeding (Cam 03 Day Color - 15:38)",
        "behavior": "EATING"
    },
    {
        "id": "02_civet_locomotion_night_ir.mp4",
        "cam": "camera 3",
        "file": "A03_00.00-06.56_dur_6h56m.mp4",
        "start_sec": 5100,  # ~01:25:00 (active prowling on sand floor & logs)
        "duration_sec": 60,
        "description": "Night Patrol & Sand Exploration (Cam 03 Night IR - 01:25)",
        "behavior": "LOCOMOTION"
    },
    {
        "id": "03_civet_resting_tire_bed_day.mp4",
        "cam": "camera 3",
        "file": "A03_14.03-18.18_dur_4h14m.mp4",
        "start_sec": 700,   # ~14:15:07 (curled up resting in straw tire bed)
        "duration_sec": 60,
        "description": "Afternoon Deep Sleep in Straw Tire Bed (Cam 03 Day Color - 14:15)",
        "behavior": "RESTING"
    },
    {
        "id": "04_civet_morning_feeding_cam2_day.mp4",
        "cam": "camera 2",
        "file": "A02_11.07-12.41_dur_1h34m.mp4",
        "start_sec": 10,    # ~11:07:15 (morning meal at food dish in Room 2)
        "duration_sec": 60,
        "description": "Morning Food Bowl Feeding (Cam 02 Day Color - 11:07)",
        "behavior": "EATING"
    }
]

print("==========================================================")
print(f"Starting Extraction of {len(clips_config)} Clean CCTV Clips for Roboflow")
print(f"Destination: {out_dir}")
print("==========================================================")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for idx, cfg in enumerate(clips_config, 1):
    src_path = os.path.join(raw_cctv_dir, cfg["cam"], cfg["file"])
    dst_path = os.path.join(out_dir, cfg["id"])
    
    print(f"\n[{idx}/{len(clips_config)}] Extracting: {cfg['id']}")
    print(f"  Behavior: {cfg['behavior']} | {cfg['description']}")
    print(f"  Source: {src_path}")
    print(f"  Start: {cfg['start_sec']}s | Duration: {cfg['duration_sec']}s")
    
    if not os.path.exists(src_path):
        print(f"  [ERROR] Source file not found: {src_path}")
        continue
        
    cap = cv2.VideoCapture(src_path)
    if not cap.isOpened():
        print(f"  [ERROR] Failed to open source video: {src_path}")
        continue
        
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    start_frame = int(cfg["start_sec"] * fps)
    frames_to_read = int(cfg["duration_sec"] * fps)
    
    print(f"  Seeking to frame {start_frame} ({fps} FPS, {width}x{height})...")
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    writer = cv2.VideoWriter(dst_path, fourcc, fps, (width, height))
    
    frames_written = 0
    t0 = time.time()
    
    for f in range(frames_to_read):
        ret, frame = cap.read()
        if not ret:
            print(f"  [WARN] Stream ended early at frame {f}/{frames_to_read}")
            break
        writer.write(frame)
        frames_written += 1
        
        if (f + 1) % 300 == 0:
            elapsed = time.time() - t0
            print(f"    Progress: {f + 1}/{frames_to_read} frames ({(f + 1)/frames_to_read*100:.1f}%) in {elapsed:.1f}s")
            
    cap.release()
    writer.release()
    
    file_size_mb = os.path.getsize(dst_path) / (1024 * 1024) if os.path.exists(dst_path) else 0
    print(f"  [SUCCESS] Written {frames_written} frames ({frames_written/fps:.1f}s) -> {file_size_mb:.2f} MB")

print("\n==========================================================")
print("All Roboflow clips extracted successfully!")
print("==========================================================")
