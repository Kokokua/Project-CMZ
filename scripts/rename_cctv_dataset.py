import cv2
import os
import sys
import json
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

mapping = []

print("=" * 80)
print("STARTING CCTV DATASET RENAMING PROCESS")
print("=" * 80)

for cam in ["camera 1", "camera 2", "camera 3", "camera 4"]:
    cam_dir = os.path.join(base_dir, cam)
    if not os.path.exists(cam_dir): continue
    files = sorted([f for f in os.listdir(cam_dir) if f.endswith('.mp4')])
    print(f"\n📂 Processing {cam.upper()} ({len(files)} files)...")
    
    for f in files:
        fp = os.path.join(cam_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration_sec = n_frames / fps
        cap.release()
        
        # parse original filename e.g. A01_20260405000000.mp4
        # or if already renamed, extract cam_code
        parts = f.replace('.mp4', '').split('_')
        cam_code = parts[0]
        
        # Try to parse start time from original filename or existing pattern
        if len(parts) >= 2 and len(parts[1]) == 14 and parts[1].isdigit():
            dt_str = parts[1]
            start_dt = datetime.strptime(dt_str, '%Y%m%d%H%M%S')
        else:
            # If already contains time or other format, fallback to parsing
            start_dt = datetime(2026, 4, 5, 0, 0, 0)
            print(f"Warning: Unexpected format in {f}")
            
        end_dt = start_dt + timedelta(seconds=duration_sec)
        
        dur_h = int(duration_sec // 3600)
        dur_m = int((duration_sec % 3600) // 60)
        dur_s = int(duration_sec % 60)
        hours = duration_sec / 3600.0
        
        start_hm = start_dt.strftime('%H.%M')
        end_hm = end_dt.strftime('%H.%M')
        dur_str = f"{dur_h}h{dur_m:02d}m"
        
        new_name = f"{cam_code}_{start_hm}-{end_hm}_dur_{dur_str}.mp4"
        new_fp = os.path.join(cam_dir, new_name)
        
        record = {
            'camera': cam,
            'cam_code': cam_code,
            'old_filename': f,
            'new_filename': new_name,
            'start_time': start_dt.strftime('%H:%M:%S'),
            'end_time': end_dt.strftime('%H:%M:%S'),
            'duration_formatted': f"{dur_h} ชม. {dur_m} นาที {dur_s} วินาที",
            'duration_hours': round(hours, 2),
            'duration_seconds': round(duration_sec, 1),
            'filesize_mb': round(os.path.getsize(fp) / (1024 * 1024), 1)
        }
        mapping.append(record)
        
        # Perform rename
        if f != new_name:
            os.rename(fp, new_fp)
            print(f"  ✓ {f} ➔ {new_name}")
        else:
            print(f"  - Already named {new_name}")

# Save JSON mapping
json_path = os.path.join(base_dir, "dataset_time_mapping.json")
with open(json_path, "w", encoding="utf-8") as jf:
    json.dump(mapping, jf, indent=2, ensure_ascii=False)

print(f"\nSaved mapping JSON to: {json_path}")
print(f"Total renamed files: {len(mapping)}")
