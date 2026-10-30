import cv2
import os
import glob
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

# Empty cam3 reference from verify_c3_A03_00._m060 (or let's take min 10 from the same size)
# Actually, verify_c3_A03_00._m060 is (360, 640)
ref_img = cv2.imread(r"D:/CMU/4th/1 st/image processing/project cmz/pic/inspections/cam3_follow_after_cam2/cam3_min_037.jpg")
ref_img = cv2.resize(ref_img, (640, 360))
ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
ref_gray = cv2.GaussianBlur(ref_gray, (15, 15), 0)

print("--- DETAILED ANALYSIS OF ROOM 3 NIGHTTIME (A03_00.00-06.56) ---")
for m in [60, 80, 100, 120, 140, 160, 180, 200]:
    p = f"D:/CMU/4th/1 st/image processing/project cmz/pic/sleeping_evidence/verify_c3_A03_00._m{m:03d}.jpg"
    img = cv2.imread(p)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    diff = cv2.absdiff(ref_gray, gray)
    _, th = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large = [c for c in contours if cv2.contourArea(c) > 500]
    
    clock_h = (m * 60) // 3600
    clock_m = ((m * 60) % 3600) // 60
    
    locs = []
    for c in large:
        x, y, w, h = cv2.boundingRect(c)
        if y < 140 and 270 <= x <= 400:
            zone = "Tire Bed"
        elif 110 <= y <= 220 and x >= 450:
            zone = "Under Log (Right fence)"
        elif y >= 140 and 200 <= x <= 450:
            zone = "Center Sand Floor"
        else:
            zone = f"Coord({x},{y})"
        locs.append(f"{zone} (Area={cv2.contourArea(c):.0f})")
    print(f"Min {m:3d} (Clock {clock_h:02d}:{clock_m:02d}): {', '.join(locs) if locs else 'No large object'}")

print("\n--- DETAILED ANALYSIS OF ROOM 3 AFTERNOON (A03_14.03-18.18) ---")
for m in [110, 120, 130, 140, 150, 160, 170]:
    p = f"D:/CMU/4th/1 st/image processing/project cmz/pic/sleeping_evidence/verify_c3_A03_14._m{m:03d}.jpg"
    img = cv2.imread(p)
    tire_crop = img[43:140, 273:393]
    log_crop = img[116:216, 466:583]
    
    sh, sm = 14, 3
    curr_min = sh * 60 + sm + m
    ch, cm = curr_min // 60, curr_min % 60
    print(f"Min {m:3d} (Clock {ch:02d}:{cm:02d}): Tire mean={np.mean(tire_crop):.1f}, Log mean={np.mean(log_crop):.1f}")
