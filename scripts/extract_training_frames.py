import cv2
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
dataset_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\images"
os.makedirs(dataset_dir, exist_ok=True)

# List of sampling targets across key events to ensure high variety
# (camera, filename, start_sec, end_sec, step_sec, prefix)
targets = [
    # 1. Day Eating at Food Tray (Cam 3) - 15:38 to 15:43
    # A03_14.03-18.18 starts 14:03:27
    # 15:38 is offset 5673s, 15:43 is 5973s
    (3, "A03_14.03-18.18_dur_4h14m.mp4", 5670, 5970, 10, "cam3_day_eating"), # ~31 frames
    
    # 2. Day Sleeping in Tire Bed (Cam 3) - 12:15 to 14:00 & 14:10 to 15:00
    # A03_11.07-14.03 starts 11:07:05. 12:15 is offset 4075s. 13:45 is offset 9475s.
    (3, "A03_11.07-14.03_dur_2h56m.mp4", 4100, 8900, 200, "cam3_day_tire_sleep1"), # ~25 frames
    # A03_14.03-18.18 starts 14:03:27. 14:15 is offset 693s. 15:00 is offset 3393s.
    (3, "A03_14.03-18.18_dur_4h14m.mp4", 700, 3100, 120, "cam3_day_tire_sleep2"), # ~21 frames
    
    # 3. Day Resting Under Log on Right Fence (Cam 3) - 16:25 to 17:10
    # A03_14.03-18.18 starts 14:03:27. 16:25 is offset 8493s. 17:10 is offset 11193s.
    (3, "A03_14.03-18.18_dur_4h14m.mp4", 8500, 11100, 100, "cam3_day_under_log"), # ~27 frames
    
    # 4. Day Locomotion / Walking on Sand (Cam 3) - 17:40 to 18:15
    # A03_14.03-18.18 starts 14:03:27. 17:40 is offset 12993s. 18:15 is offset 15093s.
    (3, "A03_14.03-18.18_dur_4h14m.mp4", 13000, 15000, 80, "cam3_day_walk"), # ~26 frames
    
    # 5. Night Locomotion & Center Sand Resting (Cam 3 IR) - 00:38 to 03:00
    # A03_00.00-06.56 starts 00:00:00. 00:38 is offset 2280s. 01:35 is offset 5700s.
    (3, "A03_00.00-06.56_dur_6h56m.mp4", 2300, 6000, 150, "cam3_night_ir_activity"), # ~25 frames
    # Night floor nap (01:28 to 01:34 = 5280s to 5640s)
    (3, "A03_00.00-06.56_dur_6h56m.mp4", 5300, 5600, 20, "cam3_night_sand_nap"), # ~16 frames
    
    # 6. Room 2 Emergence & Post-feeding Ramp Rest (Cam 2)
    # A02_00.00-05.55 emergence around 35m-38m (2100s to 2280s)
    (2, "A02_00.00-05.55_dur_5h55m.mp4", 2130, 2260, 10, "cam2_box_emerge"), # ~14 frames
    # A02_11.07-12.41 ramp rest around 40m-55m (2400s to 3300s)
    (2, "A02_11.07-12.41_dur_1h34m.mp4", 2400, 3300, 90, "cam2_day_ramp_rest"), # ~11 frames
    
    # 7. Empty Background Frames (Negative samples)
    # Room 3 empty during morning (08:00 to 10:30)
    # A03_06.56-10.54 starts 06:56:55. 08:00 is offset 3785s. 10:30 is offset 12785s.
    (3, "A03_06.56-10.54_dur_3h57m.mp4", 3800, 12600, 600, "cam3_empty_bg_day"), # ~15 frames
    # Room 3 empty at night before civet enters (00:05 to 00:35)
    (3, "A03_00.00-06.56_dur_6h56m.mp4", 300, 2100, 300, "cam3_empty_bg_night"), # ~7 frames
]

print("Starting extraction of representative training frames...")
total_extracted = 0

for cam, vname, s_sec, e_sec, step, prefix in targets:
    vp = os.path.join(base_dir, f"camera {cam}", vname)
    if not os.path.exists(vp):
        print(f"Warning: File not found: {vp}")
        continue
        
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    count = 0
    for cur_sec in range(s_sec, e_sec + 1, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(cur_sec * fps))
        ret, frame = cap.read()
        if not ret: break
        
        out_name = f"{prefix}_{count:03d}.jpg"
        out_path = os.path.join(dataset_dir, out_name)
        cv2.imwrite(out_path, frame)
        count += 1
        total_extracted += 1
        
    cap.release()
    print(f"  [{prefix}] Extracted {count} frames from {vname}")

print(f"\nExtraction complete! Total extracted frames: {total_extracted}")
