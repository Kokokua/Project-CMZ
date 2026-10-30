import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

img_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\images"
lbl_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\labels"
vis_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\annotated_previews"
os.makedirs(lbl_dir, exist_ok=True)
os.makedirs(vis_dir, exist_ok=True)

# Load background references for Cam 3 (day & night) and Cam 2 (day & night)
bg_cam3_day = cv2.imread(os.path.join(img_dir, "cam3_empty_bg_day_000.jpg"))
bg_cam3_night = cv2.imread(os.path.join(img_dir, "cam3_empty_bg_night_000.jpg"))

bg_cam3_day_g = cv2.GaussianBlur(cv2.cvtColor(bg_cam3_day, cv2.COLOR_BGR2GRAY), (15, 15), 0)
bg_cam3_night_g = cv2.GaussianBlur(cv2.cvtColor(bg_cam3_night, cv2.COLOR_BGR2GRAY), (15, 15), 0)

# Also for Cam 2
bg_cam2_ref = cv2.imread(r"D:\CMU\4th\1 st\image processing\project cmz\pic\camera_samples\cam2_110705_sample.jpg")
if bg_cam2_ref is None:
    # grab from empty Cam 2
    bg_cam2_g = None
else:
    bg_cam2_g = cv2.GaussianBlur(cv2.cvtColor(bg_cam2_ref, cv2.COLOR_BGR2GRAY), (15, 15), 0)

images = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
print(f"Total images to annotate: {len(images)}")

labeled_count = 0
bg_count = 0

for p in images:
    fname = os.path.basename(p)
    base_name = os.path.splitext(fname)[0]
    img = cv2.imread(p)
    h, w = img.shape[:2]
    
    label_path = os.path.join(lbl_dir, f"{base_name}.txt")
    
    # 1. Negative / Background images -> write empty txt
    if "empty_bg" in fname:
        with open(label_path, "w") as f:
            pass
        bg_count += 1
        continue
        
    gray = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (15, 15), 0)
    
    bbox = None # (x, y, bw, bh)
    
    # 2. Heuristic guided by verified behavior zones
    if "cam3_day_eating" in fname:
        # Detect civet around food tray: ROI [Y: 420..680, X: 640..950]
        roi_mask = np.zeros((h, w), dtype=np.uint8)
        roi_mask[400:700, 620:980] = 255
        diff = cv2.absdiff(bg_cam3_day_g, gray)
        diff = cv2.bitwise_and(diff, diff, mask=roi_mask)
        _, th = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > 1500]
        if large:
            c = max(large, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            # expand slightly to ensure full tail coverage
            bbox = (max(0, bx - 20), max(0, by - 20), min(w - bx, bw + 40), min(h - by, bh + 40))
        else:
            bbox = (660, 430, 250, 220)
            
    elif "cam3_day_tire" in fname:
        # Civet sleeping in tire bed: ROI [Y: 130..420, X: 820..1180]
        diff = cv2.absdiff(bg_cam3_day_g, gray)
        roi_diff = diff[130:420, 820:1180]
        _, th = cv2.threshold(roi_diff, 18, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > 2000]
        if large:
            c = max(large, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            bbox = (820 + bx - 15, 130 + by - 15, bw + 30, bh + 30)
        else:
            bbox = (840, 160, 280, 220)
            
    elif "cam3_day_under_log" in fname:
        # Civet under log: ROI [Y: 350..650, X: 1380..1780]
        diff = cv2.absdiff(bg_cam3_day_g, gray)
        roi_diff = diff[350:650, 1380:1780]
        _, th = cv2.threshold(roi_diff, 18, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > 2000]
        if large:
            c = max(large, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            bbox = (1380 + bx - 15, 350 + by - 15, bw + 30, bh + 30)
        else:
            bbox = (1420, 420, 320, 190)
            
    elif "cam3_night_sand_nap" in fname:
        # Sleeping on sand floor at night
        diff = cv2.absdiff(bg_cam3_night_g, gray)
        _, th = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > 3000]
        if large:
            c = max(large, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            bbox = (max(0, bx - 15), max(0, by - 15), min(w - bx, bw + 30), min(h - by, bh + 30))
        else:
            bbox = (650, 520, 280, 180)
            
    elif "cam2_box_emerge" in fname:
        # Emerging in Cam 2
        bbox = (480, 160, 320, 340)
        
    elif "cam2_day_ramp_rest" in fname:
        # Ramp in Cam 2
        bbox = (120, 380, 340, 280)
        
    else:
        # General walking in Cam 3 (day or night)
        bg_ref = bg_cam3_night_g if "night" in fname else bg_cam3_day_g
        diff = cv2.absdiff(bg_ref, gray)
        # Exclude plant movements
        diff[160:550, 950:1300] = 0
        diff[0:150, 0:400] = 0 # timestamp
        _, th = cv2.threshold(diff, 22, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in contours if cv2.contourArea(c) > 2500]
        if large:
            c = max(large, key=cv2.contourArea)
            bx, by, bw, bh = cv2.boundingRect(c)
            bbox = (max(0, bx - 20), max(0, by - 20), min(w - bx, bw + 40), min(h - by, bh + 40))
        else:
            bbox = (750, 600, 280, 180) # default fallback
            
    # Write normalized YOLO label: class_id x_center y_center w h
    bx, by, bw, bh = bbox
    xc = (bx + bw / 2.0) / w
    yc = (by + bh / 2.0) / h
    nw = bw / float(w)
    nh = bh / float(h)
    
    # Clip to 0..1
    xc = min(max(xc, 0.0), 1.0)
    yc = min(max(yc, 0.0), 1.0)
    nw = min(max(nw, 0.01), 1.0)
    nh = min(max(nh, 0.01), 1.0)
    
    with open(label_path, "w") as f:
        f.write(f"0 {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}\n")
    labeled_count += 1
    
    # Save visual confirmation for the first 30 images
    if labeled_count <= 35 or labeled_count % 15 == 0:
        vis = img.copy()
        cv2.rectangle(vis, (int(bx), int(by)), (int(bx + bw), int(by + bh)), (0, 255, 0), 3)
        cv2.putText(vis, f"civet ({bw}x{bh})", (int(bx), max(30, int(by - 10))),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imwrite(os.path.join(vis_dir, f"vis_{fname}"), cv2.resize(vis, (960, 540)))

print(f"Annotation complete! Labeled: {labeled_count}, Backgrounds: {bg_count}")
