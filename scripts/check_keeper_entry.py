import cv2, os, glob, sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

p_empty = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_check\A03_06._0856_food.jpg'
p_1115 = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_check\A03_11._1115_food.jpg'
p_1405 = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_check\A03_14._1405_food.jpg'
p_1535 = r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_check\A03_14._1535_food.jpg'

for p, label in [(p_empty, '08:56'), (p_1115, '11:15'), (p_1405, '14:05'), (p_1535, '15:35')]:
    img = cv2.imread(p)
    h, w = img.shape[:2]
    inner = img[h//4: 3*h//4, w//4: 3*w//4]
    lbl_clean = label.replace(':', '')
    print(f"{label}: inner tray shape {inner.shape}, mean BGR = {inner.mean(axis=(0,1))}")
    cv2.imwrite(f'D:/CMU/4th/1 st/image processing/project cmz/pic/inspections/cam3_food_check/inner_{lbl_clean}.jpg', inner)

v3 = r'D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\camera 3\A03_11.07-14.03_dur_2h56m.mp4'
cap = cv2.VideoCapture(v3)
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
for sec in range(0, 600, 30):
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
    ret, frame = cap.read()
    if ret:
        clock_s = 11*3600 + 7*60 + 5 + sec
        ch = (clock_s // 3600) % 24
        cm = (clock_s % 3600) // 60
        cs = clock_s % 60
        cv2.imwrite(f'D:/CMU/4th/1 st/image processing/project cmz/pic/inspections/cam3_food_check/keeper_{ch:02d}{cm:02d}{cs:02d}.jpg', cv2.resize(frame, (640, 360)))
cap.release()
print('Keeper frames extracted successfully!')
