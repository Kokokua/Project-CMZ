import cv2
import os
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

records = []

for cam in ["camera 1", "camera 2", "camera 3", "camera 4"]:
    cam_dir = os.path.join(base_dir, cam)
    if not os.path.exists(cam_dir): continue
    files = sorted([f for f in os.listdir(cam_dir) if f.endswith('.mp4')])
    print(f"\n==================== {cam.upper()} ({len(files)} files) ====================")
    for f in files:
        fp = os.path.join(cam_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration_sec = n_frames / fps
        cap.release()
        
        # parse filename e.g. A01_20260405000000.mp4
        parts = f.replace('.mp4', '').split('_')
        cam_code = parts[0]
        dt_str = parts[1]
        start_dt = datetime.strptime(dt_str, '%Y%m%d%H%M%S')
        end_dt = start_dt + timedelta(seconds=duration_sec)
        
        hours = duration_sec / 3600.0
        dur_h = int(duration_sec // 3600)
        dur_m = int((duration_sec % 3600) // 60)
        dur_s = int(duration_sec % 60)
        
        # Format duration string
        if dur_h > 0:
            dur_text = f"{dur_h}h{dur_m:02d}m"
        else:
            dur_text = f"{dur_m}m{dur_s:02d}s"
            
        start_time_str = start_dt.strftime('%H.%M.%S')
        end_time_str = end_dt.strftime('%H.%M.%S')
        start_hm = start_dt.strftime('%H.%M')
        end_hm = end_dt.strftime('%H.%M')
        
        # Suggested name options
        name_option_A = f"{cam_code}_{start_hm}-{end_hm}_{dur_text}.mp4"
        name_option_B = f"{start_hm}-{end_hm}_({hours:.2f}hrs)_{cam_code}.mp4"
        name_option_C = f"{cam_code}_{start_time_str}_to_{end_time_str}_dur_{dur_h}h{dur_m:02d}m.mp4"
        
        records.append({
            'cam': cam,
            'cam_code': cam_code,
            'old_name': f,
            'full_path': fp,
            'start_dt': start_dt,
            'end_dt': end_dt,
            'duration_sec': duration_sec,
            'hours': hours,
            'dur_h': dur_h,
            'dur_m': dur_m,
            'dur_s': dur_s,
            'name_A': name_option_A,
            'name_B': name_option_B,
            'name_C': name_option_C
        })
        
        print(f"{f} -> {start_dt.strftime('%H:%M:%S')} ถึง {end_dt.strftime('%H:%M:%S')} (ความยาว: {dur_h} ชม. {dur_m} นาที / {hours:.2f} ชม.)")
