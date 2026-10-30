import os
import glob
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset"
target_base = os.path.join(dataset_dir, "ชะมดแผงสันหางดำ")

parts = sorted(glob.glob(os.path.join(dataset_dir, "ชะมดแผงสันหางดำ-20261028T180512Z-1-*")))
parts = [p for p in parts if os.path.isdir(p)]

print(f"Found {len(parts)} part directories to reorganize.")

# Collect files to move
moves = []
for p in parts:
    part_name = os.path.basename(p)
    for root, dirs, files in os.walk(p):
        for f in files:
            full_src = os.path.join(root, f)
            rel = os.path.relpath(full_src, p)
            
            # Determine camera
            cam_name = None
            for item in rel.split(os.sep):
                if "camera" in item.lower():
                    # Standardize name: "camera 1", "camera 2", etc.
                    cam_name = item.strip().lower()
                    break
            
            if not cam_name:
                # check filename prefix
                if f.startswith("A01"): cam_name = "camera 1"
                elif f.startswith("A02"): cam_name = "camera 2"
                elif f.startswith("A03"): cam_name = "camera 3"
                elif f.startswith("A04"): cam_name = "camera 4"
                else: cam_name = "camera_unknown"
            
            dest_dir = os.path.join(target_base, cam_name)
            dest_file = os.path.join(dest_dir, f)
            moves.append((full_src, dest_file, cam_name, f))

print(f"Total files identified to move: {len(moves)}")

# Create destination directories
for _, dest_file, cam_name, _ in moves:
    os.makedirs(os.path.dirname(dest_file), exist_ok=True)

# Execute moves
moved_count = 0
for src, dst, cam, fname in moves:
    if os.path.exists(dst):
        print(f"Destination already exists: {dst}")
    else:
        # os.replace or shutil.move
        shutil.move(src, dst)
        moved_count += 1

print(f"Successfully moved {moved_count} files into '{target_base}'.")

# Clean up empty part directories
removed_dirs = 0
for p in parts:
    # Walk bottom up and remove empty dirs
    for root, dirs, files in os.walk(p, topdown=False):
        if not os.listdir(root):
            os.rmdir(root)
    if os.path.exists(p) and not os.listdir(p):
        os.rmdir(p)
        removed_dirs += 1
    elif os.path.exists(p):
        print(f"Notice: Part directory {p} is not empty, skipping removal.")

print(f"Cleaned up {removed_dirs} empty part directories.")

# Verify and print new structure
print("\n" + "=" * 60)
print(f"NEW ORGANIZED STRUCTURE IN: {target_base}")
print("=" * 60)

for cam in ["camera 1", "camera 2", "camera 3", "camera 4"]:
    cam_path = os.path.join(target_base, cam)
    if os.path.exists(cam_path):
        f_list = sorted(os.listdir(cam_path))
        print(f"\n📂 {cam.upper()} ({len(f_list)} files):")
        total_cam_mb = 0
        for f in f_list:
            fp = os.path.join(cam_path, f)
            sz = os.path.getsize(fp) / (1024 * 1024)
            total_cam_mb += sz
            print(f"   └─ {f}  ({sz:6.1f} MB)")
        print(f"   [Subtotal: {total_cam_mb/1024:.2f} GB]")

print("\nReorganization finished successfully.")
