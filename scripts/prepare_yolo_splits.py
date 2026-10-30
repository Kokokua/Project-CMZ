import os
import glob
import shutil
import random
import sys

sys.stdout.reconfigure(encoding='utf-8')
random.seed(42)

src_img_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\images"
src_lbl_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_phase2_dataset\labels"

out_base = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\yolo_civet_dataset"
os.makedirs(os.path.join(out_base, "images", "train"), exist_ok=True)
os.makedirs(os.path.join(out_base, "images", "val"), exist_ok=True)
os.makedirs(os.path.join(out_base, "labels", "train"), exist_ok=True)
os.makedirs(os.path.join(out_base, "labels", "val"), exist_ok=True)

images = sorted(glob.glob(os.path.join(src_img_dir, "*.jpg")))
random.shuffle(images)

n_total = len(images)
n_train = int(n_total * 0.8)

train_imgs = images[:n_train]
val_imgs = images[n_train:]

print(f"Total: {n_total} images -> Train: {len(train_imgs)}, Val: {len(val_imgs)}")

for p in train_imgs:
    fname = os.path.basename(p)
    base = os.path.splitext(fname)[0]
    shutil.copy2(p, os.path.join(out_base, "images", "train", fname))
    lbl_src = os.path.join(src_lbl_dir, f"{base}.txt")
    if os.path.exists(lbl_src):
        shutil.copy2(lbl_src, os.path.join(out_base, "labels", "train", f"{base}.txt"))

for p in val_imgs:
    fname = os.path.basename(p)
    base = os.path.splitext(fname)[0]
    shutil.copy2(p, os.path.join(out_base, "images", "val", fname))
    lbl_src = os.path.join(src_lbl_dir, f"{base}.txt")
    if os.path.exists(lbl_src):
        shutil.copy2(lbl_src, os.path.join(out_base, "labels", "val", f"{base}.txt"))

yaml_content = f"""path: {out_base.replace('\\\\', '/')}
train: images/train
val: images/val

names:
  0: civet
"""

with open(os.path.join(out_base, "data.yaml"), "w", encoding="utf-8") as f:
    f.write(yaml_content)

print(f"Dataset splits and data.yaml generated successfully in: {out_base}")
