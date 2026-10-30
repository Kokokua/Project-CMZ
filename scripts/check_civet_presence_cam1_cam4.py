import cv2, os, glob
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"

# We want to check:
# 1. Camera 1: all 9 files
# 2. Camera 4: all 9 files
# Does the civet ever stay motionless or occupy any specific spot for long periods in Camera 1 or Camera 4?
# Let's sample frames every 60 seconds (1 minute) from all files in Cam 1 and Cam 4!

def analyze_camera_presence(cam_name, sample_interval_sec=60):
    cam_dir = os.path.join(base_dir, cam_name)
    files = sorted([f for f in os.listdir(cam_dir) if f.endswith('.mp4')])
    print(f"\n==================== Scanning {cam_name.upper()} ({len(files)} files) ====================")
    
    total_samples = 0
    motion_events = []
    
    # We can also detect if anything different from an empty room reference frame exists
    # First, let's get an empty room reference from the first file
    ref_gray = None
    
    for f in files:
        fp = os.path.join(cam_dir, f)
        cap = cv2.VideoCapture(fp)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        dur_min = (n_frames / fps) / 60.0
        
        # Sample every 60 seconds
        step_frames = int(sample_interval_sec * fps)
        prev_f = None
        
        diffs = []
        for f_idx in range(0, n_frames, step_frames):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
            ret, frame = cap.read()
            if not ret: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (15, 15), 0)
            
            if ref_gray is None:
                ref_gray = gray
                
            # diff with ref_gray
            ref_diff = np.mean(cv2.absdiff(ref_gray, gray))
            
            # diff with previous frame (motion)
            if prev_f is not None:
                motion = np.mean(cv2.absdiff(prev_f, gray))
            else:
                motion = 0
            prev_f = gray
            
            sec_in_video = f_idx / fps
            diffs.append((sec_in_video, ref_diff, motion))
        
        cap.release()
        
        # Analyze diffs
        # High ref_diff might mean civet is present (or lighting changed)
        # Low motion while high ref_diff means motionless object present!
        max_motion = max([d[2] for d in diffs]) if diffs else 0
        avg_motion = np.mean([d[2] for d in diffs]) if diffs else 0
        print(f"File {f} ({dur_min:.1f} min): avg motion={avg_motion:.2f}, max motion={max_motion:.2f}")

print("Checking presence in Cam 1...")
analyze_camera_presence("camera 1", sample_interval_sec=120)

print("\nChecking presence in Cam 4...")
analyze_camera_presence("camera 4", sample_interval_sec=120)
