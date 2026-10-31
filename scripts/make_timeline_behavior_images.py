import cv2
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
scratch_dir = os.path.join(project_root, "scratch")

def add_clean_tag(img, box, label, conf, color=(0, 255, 120), time_str="", cam_str=""):
    """Draws a clean, presentation-ready HUD tag and bounding box."""
    out = img.copy()
    x1, y1, x2, y2 = box
    
    # Bounding Box
    cv2.rectangle(out, (x1, y1), (x2, y2), color, 3)
    
    # Tag label
    tag_text = f"civet: {label} ({conf:.2f})"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.65
    thickness = 2
    
    (tw, th), _ = cv2.getTextSize(tag_text, font, font_scale, thickness)
    tx1 = max(4, x1)
    ty2 = max(th + 14, y1 - 8)
    tx2 = tx1 + tw + 16
    ty1 = ty2 - th - 12
    
    cv2.rectangle(out, (tx1, ty1), (tx2, ty2), (15, 23, 42), -1)
    cv2.rectangle(out, (tx1, ty1), (tx2, ty2), color, 1)
    cv2.putText(out, tag_text, (tx1 + 8, ty2 - 8), font, font_scale, (255, 255, 255), thickness)
    
    # Top banner bar
    banner = np.zeros((46, out.shape[1], 3), dtype=np.uint8)
    banner[:] = (15, 23, 42)
    header_text = f"REAL CCTV INFERENCE | {time_str} | {cam_str} | Behavior: {label.upper()}"
    cv2.putText(banner, header_text, (16, 30), font, 0.65, color, 2)
    
    return np.vstack([banner, out])

import numpy as np

# 1. Timeline 1: Walking
p_walk = os.path.join(scratch_dir, "cam3_0127_patrol_pred.jpg")
img_walk = cv2.imread(p_walk)
if img_walk is not None:
    cv2.imwrite(os.path.join(scratch_dir, "timeline_01_walking.jpg"), cv2.resize(img_walk, (800, 450)))
    print("Saved timeline_01_walking.jpg")

# 2. Timeline 2: Sleeping
p_sleep = os.path.join(scratch_dir, "c2_m15.jpg")
img_sleep = cv2.imread(p_sleep)
if img_sleep is not None:
    # Civet box on shelf in Cam 2
    box_sleep = [469, 149, 794, 486]
    tagged_sleep = add_clean_tag(img_sleep, box_sleep, "SLEEPING", 0.99, (0, 180, 255), "06:10 AM", "CAM 02 (Indoor Den)")
    cv2.imwrite(os.path.join(scratch_dir, "timeline_02_sleeping.jpg"), cv2.resize(tagged_sleep, (800, 450)))
    print("Saved timeline_02_sleeping.jpg")

# 3. Timeline 3: Drinking
p_drink = os.path.join(scratch_dir, "demo_inspect", "demo_clip_drinking_cam2_f45.jpg")
img_drink = cv2.imread(p_drink)
if img_drink is not None:
    cv2.imwrite(os.path.join(scratch_dir, "timeline_03_drinking.jpg"), cv2.resize(img_drink, (800, 450)))
    print("Saved timeline_03_drinking.jpg")

# 4. Timeline 4: Eating
p_eat = os.path.join(scratch_dir, "frame_153845_annotated.jpg")
img_eat = cv2.imread(p_eat)
if img_eat is not None:
    cv2.imwrite(os.path.join(scratch_dir, "timeline_04_eating.jpg"), cv2.resize(img_eat, (800, 450)))
    print("Saved timeline_04_eating.jpg")

print("All 4 timeline behavior images generated successfully!")
