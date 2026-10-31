import os
import sys
import time
import zipfile
from roboflow import Roboflow

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
scratch_dir = os.path.join(project_root, "scratch")
extract_dir = os.path.join(scratch_dir, "expanded_dataset")
zip_path = os.path.join(project_root, "finish", "civet_yolo_dataset_phase2.zip")

os.makedirs(extract_dir, exist_ok=True)

# 1. Unzip dataset
print(f"Extracting {zip_path} to {extract_dir}...")
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)
print("Extraction complete.")

# 2. Connect to Roboflow
API_KEY = "Dbsq4wpnTVr9UkRb7YBj"
WORKSPACE = "mes-workspace-02uvi"
PROJECT_ID = "civet-monitoring"

print("==================================================================")
print(f"CONNECTING TO ROBOFLOW: {WORKSPACE}/{PROJECT_ID}")
print("==================================================================")

rf = Roboflow(api_key=API_KEY)
project = rf.workspace(WORKSPACE).project(PROJECT_ID)
print(f"Connected to project: '{project.name}'")

# 3. Gather all image and label pairs
items_to_upload = []

for split in ["train", "val"]:
    img_split_dir = os.path.join(extract_dir, "images", split)
    lbl_split_dir = os.path.join(extract_dir, "labels", split)
    
    if not os.path.exists(img_split_dir):
        continue
        
    for fname in sorted(os.listdir(img_split_dir)):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(img_split_dir, fname)
            base_name = os.path.splitext(fname)[0]
            lbl_path = os.path.join(lbl_split_dir, f"{base_name}.txt")
            
            # Map split name: 'val' -> 'valid'
            roboflow_split = "valid" if split == "val" else "train"
            
            items_to_upload.append({
                "img_path": img_path,
                "lbl_path": lbl_path if os.path.exists(lbl_path) else None,
                "split": roboflow_split,
                "filename": fname
            })

print(f"Found {len(items_to_upload)} image-label pairs ready for upload.")
train_c = sum(1 for it in items_to_upload if it["split"] == "train")
valid_c = sum(1 for it in items_to_upload if it["split"] == "valid")
print(f"Split breakdown: Train = {train_c}, Valid = {valid_c}")

# 4. Batch Upload to Roboflow
print("\n==================================================================")
print(f"STARTING BATCH UPLOAD TO ROBOFLOW ({len(items_to_upload)} images)...")
print("==================================================================")

t_start = time.time()
uploaded = 0
failed = 0

for idx, item in enumerate(items_to_upload, 1):
    img_p = item["img_path"]
    lbl_p = item["lbl_path"]
    spl = item["split"]
    
    try:
        project.upload(
            image_path=img_p,
            annotation_path=lbl_p,
            split=spl,
            num_retry_uploads=3
        )
        uploaded += 1
        if idx % 15 == 0 or idx == len(items_to_upload):
            pct = (idx / len(items_to_upload)) * 100.0
            elapsed = time.time() - t_start
            rate = idx / elapsed if elapsed > 0 else 0
            eta = (len(items_to_upload) - idx) / rate if rate > 0 else 0
            print(f"  Progress: {idx}/{len(items_to_upload)} ({pct:.1f}%) | Uploaded: {uploaded} | Elapsed: {elapsed:.1f}s | ETA: {eta:.0f}s")
    except Exception as e:
        print(f"  [ERROR] Upload failed for {item['filename']}: {e}")
        failed += 1

print("\n==================================================================")
print("UPLOAD PROCESS COMPLETED!")
print(f"Total Successfully Uploaded: {uploaded}/{len(items_to_upload)}")
print(f"Failed: {failed}")
print(f"Total Elapsed Time: {time.time() - t_start:.1f}s")
print(f"Verify on Roboflow: https://app.roboflow.com/{WORKSPACE}/{PROJECT_ID}")
print("==================================================================")
