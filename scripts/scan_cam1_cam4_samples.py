import cv2, os, glob
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"pic/inspections/cam1_cam4_presence"
os.makedirs(out_dir, exist_ok=True)

# For each camera, let's scan a daytime video and a nighttime video
# Camera 1:
# A01_06.13-09.48_dur_3h35m.mp4 (morning daylight)
# A01_18.55-23.59_dur_5h03m.mp4 (night)
# Camera 4:
# A04_08.19-10.27_dur_2h08m.mp4 (morning daylight)
# A04_17.08-22.27_dur_5h19m.mp4 (night)

def scan_video_for_civet(vpath, cam_tag, sample_sec=30):
    cap = cv2.VideoCapture(vpath)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_min = (total_frames / fps) / 60.0
    
    # Empty background reference (first frame)
    ret, f0 = cap.read()
    if not ret: return
    bg = cv2.GaussianBlur(cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY), (21, 21), 0)
    
    print(f"\nScanning {cam_tag}: {os.path.basename(vpath)} ({dur_min:.1f} mins)")
    
    high_diff_moments = []
    
    for sec in range(0, int(dur_min * 60), sample_sec):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(sec * fps))
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
        diff = cv2.absdiff(bg, gray)
        # ignore top plant if any, just mean diff
        m_diff = np.mean(diff)
        if m_diff > 4.0: # threshold for animal presence / significant change
            m = sec // 60
            s = sec % 60
            high_diff_moments.append((sec, m, s, m_diff))
            # save sample
            if len(high_diff_moments) <= 5 or sec % 300 == 0:
                out_p = os.path.join(out_dir, f"{cam_tag}_{m:03d}m_{s:02d}s.jpg")
                cv2.imwrite(out_p, frame)
                print(f"  [{cam_tag}] Detected change at {m:02d}:{s:02d} (diff={m_diff:.1f}) -> saved {os.path.basename(out_p)}")
                
    cap.release()
    print(f"Total change samples in {cam_tag}: {len(high_diff_moments)}")

scan_video_for_civet(os.path.join(base_dir, "camera 1", "A01_06.13-09.48_dur_3h35m.mp4"), "CAM1_Day", sample_sec=60)
scan_video_for_civet(os.path.join(base_dir, "camera 4", "A04_08.19-10.27_dur_2h08m.mp4"), "CAM4_Day", sample_sec=60)
scan_video_for_civet(os.path.join(base_dir, "camera 4", "A04_17.08-22.27_dur_5h19m.mp4"), "CAM4_Night", sample_sec=60)
