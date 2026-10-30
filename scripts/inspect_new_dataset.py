import os
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

dataset_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset"
parts = sorted(glob.glob(os.path.join(dataset_dir, "ชะมดแผงสันหางดำ-20261028T180512Z-1-*")))
parts = [p for p in parts if os.path.isdir(p)]

files_by_camera = {}

for p in parts:
    part_name = os.path.basename(p)
    for root, dirs, files in os.walk(p):
        for f in files:
            full_path = os.path.join(root, f)
            sz_mb = os.path.getsize(full_path) / (1024 * 1024)
            rel = os.path.relpath(full_path, p)
            # Find camera
            cam = "other"
            for item in rel.split(os.sep):
                if "camera" in item.lower():
                    cam = item.strip().lower()
                    break
            files_by_camera.setdefault(cam, []).append({
                "filename": f,
                "size_mb": sz_mb,
                "part": part_name,
                "full_path": full_path,
                "rel_inside_part": rel
            })

for cam in sorted(files_by_camera.keys()):
    print(f"\n==================== {cam.upper()} (Total {len(files_by_camera[cam])} files) ====================")
    for item in sorted(files_by_camera[cam], key=lambda x: x['filename']):
        print(f"[{item['part'][-3:]}] {item['size_mb']:6.1f} MB | {item['filename']} | {item['rel_inside_part']}")
