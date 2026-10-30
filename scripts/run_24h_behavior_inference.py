import cv2
import os
import glob
import sys
import json
import csv
import numpy as np
from datetime import datetime, timedelta
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

# Paths
model_path = r"D:\CMU\4th\1 st\image processing\project cmz\models\yolov8n_civet_phase2\weights\best.pt"
base_vids = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_csv = r"D:\CMU\4th\1 st\image processing\project cmz\finish\daily_behavior_log.csv"
os.makedirs(os.path.dirname(out_csv), exist_ok=True)

# Master Camera Files (Camera 03) across 00:00 to 24:00 of 05-Apr-2026
cam3_files = [
    ("A03_00.00-06.56_dur_6h56m.mp4", "00:00:00", "06:56:55"),
    ("A03_06.56-10.54_dur_3h57m.mp4", "06:56:55", "10:54:17"),
    ("A03_10.54-11.06_dur_0h11m.mp4", "10:54:17", "11:06:16"),
    ("A03_11.07-14.03_dur_2h56m.mp4", "11:07:05", "14:03:26"),
    ("A03_14.03-18.18_dur_4h14m.mp4", "14:03:27", "18:18:06"),
    ("A03_18.18-02.12_dur_7h54m.mp4", "18:18:06", "24:00:00"), # cut at 24:00:00
]

print("24-Hour Behavior Inference Pipeline configured.")
