import cv2, os, glob, sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

base = r'D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 3'
out_dir = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_timeline'
os.makedirs(out_dir, exist_ok=True)

vids = [
    ('A03_00.00-06.56_dur_6h56m.mp4', '00:00:00', [10, 60, 180, 300, 360]),
    ('A03_06.56-10.54_dur_3h57m.mp4', '06:56:55', [10, 60, 120, 180, 220]),
    ('A03_10.54-11.06_dur_0h11m.mp4', '10:54:17', [1, 5, 10]),
    ('A03_11.07-14.03_dur_2h56m.mp4', '11:07:05', [1, 5, 15, 30, 60, 120, 160]),
    ('A03_14.03-18.18_dur_4h14m.mp4', '14:03:27', [1, 30, 60, 80, 90, 95, 120]),
]

for vname, start_t, mins in vids:
    vp = os.path.join(base, vname)
    if not os.path.exists(vp): continue
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    sh, sm, ss = [int(x) for x in start_t.split(':')]
    
    for m in mins:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(m * 60 * fps))
        ret, frame = cap.read()
        if not ret: break
        
        tot_s = sh*3600 + sm*60 + ss + m*60
        ch = (tot_s // 3600) % 24
        cm = (tot_s % 3600) // 60
        cs = tot_s % 60
        
        # Tray ROI: Y 480..600, X 680..840
        tray = frame[480:600, 680:840]
        # Calculate saturation or red intensity
        hsv = cv2.cvtColor(tray, cv2.COLOR_BGR2HSV)
        sat = hsv[:, :, 1].mean()
        val = hsv[:, :, 2].mean()
        
        fname = f"{ch:02d}{cm:02d}_{vname[:7]}_m{m:03d}.jpg"
        cv2.imwrite(os.path.join(out_dir, fname), tray)
        print(f"Clock {ch:02d}:{cm:02d}:{cs:02d} ({vname[:7]} min {m:3d}): Sat={sat:.1f}, Val={val:.1f}")
        
    cap.release()

print('Timeline check complete!')
