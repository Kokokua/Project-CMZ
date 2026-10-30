import os, glob, json, sys
import cv2

sys.stdout.reconfigure(encoding='utf-8')

# 1. Timeline of cameras
p = r'D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\dataset_time_mapping.json'
with open(p, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== CAMERA TIMELINE BOUNDARIES ===')
cams = {}
for item in data:
    c = item['camera']
    if c not in cams:
        cams[c] = []
    cams[c].append(item)

for c in sorted(cams.keys()):
    first = cams[c][0]
    last = cams[c][-1]
    print(f"{c}:")
    print(f"  First: {first['new_filename']} (Start: {first['start_time']})")
    print(f"  Last:  {last['new_filename']} (End: {last['end_time']})")
    print(f"  Total files: {len(cams[c])}")

# 2. Check food placement in Cam 3
print('\n=== CHECKING WHEN FOOD WAS PLACED IN ROOM 3 ===')
food_imgs = sorted(glob.glob(r'D:\CMU\4th\1 st\image processing\project cmz\pic\inspections\cam3_food_check\*_food.jpg'))
for img_p in food_imgs:
    img = cv2.imread(img_p)
    fname = os.path.basename(img_p)
    print(f"{fname}: mean color = {img.mean(axis=(0,1))}")
