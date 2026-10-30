import cv2
import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect Camera 2 images
# When is civet visible on floor vs when is civet on ramp vs when is civet in box?
cam2_dir = r"D:\CMU\4th\1 st\image processing\project cmz\pic\sleeping_evidence"
cam2_imgs = sorted(glob.glob(os.path.join(cam2_dir, "A02_*.jpg")))

print(f"Total Cam 2 images: {len(cam2_imgs)}")

# Let's write an analysis script to check presence on ramp [Y: 150..300, X: 50..200 in 640x360]
# and floor [Y: 200..360, X: 200..500 in 640x360]
# and ledge behind plant [Y: 50..150, X: 150..400 in 640x360]

# Let's also check Camera 3 images:
cam3_imgs = sorted(glob.glob(os.path.join(cam2_dir, "cam3_*.jpg")))
print(f"Total Cam 3 images: {len(cam3_imgs)}")

for img_p in cam3_imgs:
    fname = os.path.basename(img_p)
    # read image
    img = cv2.imread(img_p)
    # Check tire bed (in 640x360: Y: 43..140, X: 273..393)
    tire_crop = img[43:140, 273:393]
    # Check under log (in 640x360: Y: 116..216, X: 466..583)
    log_crop = img[116:216, 466:583]
    
    # print summary of what's where
