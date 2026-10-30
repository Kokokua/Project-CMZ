import cv2, glob, os
import numpy as np

imgs = sorted(glob.glob('pic/resting_samples/*.jpg'))
thumbs = []
for p in imgs:
    img = cv2.imread(p)
    # resize to 640x360
    th = cv2.resize(img, (640, 360))
    fname = os.path.basename(p).replace('.mp4.jpg', '')
    cv2.putText(th, fname, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    thumbs.append(th)

# 7 images: pad with a black image to make 8 (4x2 or 2x4)
thumbs.append(np.zeros_like(thumbs[0]))
row1 = np.hstack(thumbs[:4])
row2 = np.hstack(thumbs[4:8])
grid = np.vstack([row1, row2])

os.makedirs('pic/inspections', exist_ok=True)
cv2.imwrite('pic/inspections/phase1_resting_7clips.jpg', grid)
print('Saved pic/inspections/phase1_resting_7clips.jpg')
