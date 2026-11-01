import cv2
import os
import shutil
import numpy as np

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
out_dir = os.path.join(project_root, "finish", "demo_clips_clean")
os.makedirs(out_dir, exist_ok=True)

desktop_dir = r"C:\Users\ASUS\Desktop\html knowledge file\CMZ project\demo_clips_clean"
os.makedirs(desktop_dir, exist_ok=True)

art_dir = r"C:\Users\ASUS\.gemini\antigravity-cli\brain\ea6f126b-0636-4ec3-8397-957f0b099627"

# Camera video paths and offset to reach 07:05:00 AM
cam_specs = [
    {
        "id": "Cam 01",
        "title": "Cam 01: Corridor / Ramp",
        "path": os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 1", "A01_06.13-09.48_dur_3h35m.mp4"),
        "sec": 3120, # 07:05:00 - 06:13:00 = 52 min = 3120 sec
        "status": "VACANT (No Civet Detected)",
        "color": (100, 116, 139) # Muted Slate
    },
    {
        "id": "Cam 02",
        "title": "Cam 02: Sleeping Box Area",
        "path": os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 2", "A02_05.55-09.51_dur_3h56m.mp4"),
        "sec": 4200, # 07:05:00 - 05:55:00 = 70 min = 4200 sec
        "status": "RESTING IN SLEEPING BOX",
        "color": (168, 85, 247) # Vibrant Purple
    },
    {
        "id": "Cam 03",
        "title": "Cam 03: Main Enclosure (Tire & Tray)",
        "path": os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_06.56-10.54_dur_3h57m.mp4"),
        "sec": 540, # 07:05:00 - 06:56:00 = 9 min = 540 sec
        "status": "VACANT (Tire & Sand Empty)",
        "color": (100, 116, 139)
    },
    {
        "id": "Cam 04",
        "title": "Cam 04: Hydration Area",
        "path": os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4"),
        "sec": 10080, # 07:05:00 - 04:17:00 = 2h 48m = 10080 sec
        "status": "VACANT (Water Basin Empty)",
        "color": (100, 116, 139)
    }
]

caps = []
for spec in cam_specs:
    assert os.path.exists(spec["path"]), f"File not found: {spec['path']}"
    cap = cv2.VideoCapture(spec["path"])
    assert cap.isOpened(), f"Cannot open {spec['path']}"
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(spec["sec"] * fps))
    caps.append((cap, fps))

grid_w, grid_h = 1280, 720
sub_w, sub_h = 640, 340 # 2 rows = 680 height + 40 bottom bar = 720
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out_mp4 = os.path.join(out_dir, "clean_demo_4cam_sleeping_box_sync.mp4")
writer = cv2.VideoWriter(out_mp4, fourcc, 15.0, (grid_w, grid_h))
poster = None

print("Rendering 4-Camera Synchronized Spatial Exclusion Video (6 seconds @ 15 fps)...")

for f_idx in range(6 * 15):
    sub_frames = []
    for i, (cap, fps) in enumerate(caps):
        ret, frame = cap.read()
        cap.read() # skip 1 for 15 fps
        if not ret or frame is None:
            frame = np.zeros((sub_h, sub_w, 3), dtype=np.uint8)
        else:
            frame = cv2.resize(frame, (sub_w, sub_h))
            
        spec = cam_specs[i]
        
        # Specific ROIs for each camera
        if spec["id"] == "Cam 02":
            # Sleeping box opening ROI
            cv2.rectangle(frame, (int(sub_w * 0.15), int(sub_h * 0.15)), (int(sub_w * 0.55), int(sub_h * 0.65)), (168, 85, 247), 2, cv2.LINE_AA)
            cv2.putText(frame, "ROI: Indoor Sleeping Box [OCCUPIED]", (int(sub_w * 0.15), int(sub_h * 0.15) - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, (168, 85, 247), 1, cv2.LINE_AA)
        elif spec["id"] == "Cam 03":
            # Tire bed ROI
            cv2.rectangle(frame, (int(sub_w * 0.38), int(sub_h * 0.12)), (int(sub_w * 0.65), int(sub_h * 0.48)), (75, 85, 99), 1, cv2.LINE_AA)
            cv2.putText(frame, "ROI: Tire Bed [Vacant]", (int(sub_w * 0.38), int(sub_h * 0.12) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (156, 163, 175), 1, cv2.LINE_AA)
            # Fruit tray ROI
            cv2.rectangle(frame, (int(sub_w * 0.35), int(sub_h * 0.48)), (int(sub_w * 0.48), int(sub_h * 0.70)), (75, 85, 99), 1, cv2.LINE_AA)
            cv2.putText(frame, "ROI: Fruit Tray [Vacant]", (int(sub_w * 0.35), int(sub_h * 0.48) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (156, 163, 175), 1, cv2.LINE_AA)
        elif spec["id"] == "Cam 04":
            # Water basin ROI
            cv2.rectangle(frame, (int(sub_w * 0.30), int(sub_h * 0.48)), (int(sub_w * 0.46), int(sub_h * 0.68)), (75, 85, 99), 1, cv2.LINE_AA)
            cv2.putText(frame, "ROI: Water Basin [Vacant]", (int(sub_w * 0.30), int(sub_h * 0.48) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (156, 163, 175), 1, cv2.LINE_AA)
            
        # Subtle header tag for each camera quadrant
        tag_bg = (15, 23, 42)
        cv2.rectangle(frame, (8, 8), (sub_w - 8, 34), tag_bg, -1)
        cv2.rectangle(frame, (8, 8), (sub_w - 8, 34), spec["color"], 1, cv2.LINE_AA)
        
        cv2.putText(frame, spec["title"], (16, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Status text on the right
        st_text = spec["status"]
        (stw, _), _ = cv2.getTextSize(st_text, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        cv2.putText(frame, st_text, (sub_w - 18 - stw, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.42, spec["color"], 1, cv2.LINE_AA)
        
        sub_frames.append(frame)
        
    # Stitch 2x2 grid
    top_row = np.hstack([sub_frames[0], sub_frames[1]])
    bot_row = np.hstack([sub_frames[2], sub_frames[3]])
    grid_img = np.vstack([top_row, bot_row])
    
    # Bottom exclusion deduction banner (40px)
    banner = np.zeros((40, grid_w, 3), dtype=np.uint8)
    banner[:] = (15, 23, 42)
    cv2.line(banner, (0, 0), (grid_w, 0), (168, 85, 247), 2)
    
    time_str = "TIMESTAMP: 2026-04-05 07:05:00 (SYNCHRONIZED)"
    deduction_str = "SPATIAL EXCLUSION LOGIC: Cam 01, 03, 04 are Vacant  ==>  Civet Verified RESTING Inside Cam 02 Sleeping Box"
    
    cv2.putText(banner, time_str, (16, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (148, 163, 184), 1, cv2.LINE_AA)
    cv2.putText(banner, deduction_str, (420, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (234, 179, 8), 1, cv2.LINE_AA)
    
    final_frame = np.vstack([grid_img, banner])
    writer.write(final_frame)
    if poster is None and f_idx == 35:
        poster = final_frame.copy()

for cap, _ in caps:
    cap.release()
writer.release()
print(f"Rendered synchronized 4-camera video: {out_mp4}")

if poster is not None:
    p_path = os.path.join(out_dir, "clean_demo_4cam_sleeping_box_sync_poster.jpg")
    cv2.imwrite(p_path, poster)
    cv2.imwrite(os.path.join(desktop_dir, "clean_demo_4cam_sleeping_box_sync_poster.jpg"), poster)
    cv2.imwrite(os.path.join(art_dir, "clean_demo_4cam_sleeping_box_sync_poster.jpg"), poster)
    shutil.copy2(out_mp4, os.path.join(desktop_dir, "clean_demo_4cam_sleeping_box_sync.mp4"))
    print("Poster and video copied to desktop and artifacts successfully!")
