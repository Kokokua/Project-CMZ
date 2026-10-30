import cv2
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ"
out_dir = r"D:\CMU\4th\1 st\image processing\project cmz\pic\sleeping_evidence\summary_cards"
os.makedirs(out_dir, exist_ok=True)

spots = [
    {
        "cam": 2,
        "file": "A02_00.00-05.55_dur_5h55m.mp4",
        "sec": 15 * 60, # 00:15:00
        "clock": "00:15:00",
        "title": "Spot 1: Room 2 Sleeping Box (Hidden Behind Plant)",
        "desc": "File: A02_00.00-05.55_dur_5h55m.mp4 | In-video: 00:00:00 - 00:35:40"
    },
    {
        "cam": 2,
        "file": "A02_00.00-05.55_dur_5h55m.mp4",
        "sec": int(36.5 * 60), # 00:36:30
        "clock": "00:36:30",
        "title": "Room 2: Waking up & emerging from box",
        "desc": "File: A02_00.00-05.55_dur_5h55m.mp4 | In-video: 00:35:45 - 00:37:40"
    },
    {
        "cam": 3,
        "file": "A03_00.00-06.56_dur_6h56m.mp4",
        "sec": int(88 * 60), # 01:28:00
        "clock": "01:28:00",
        "title": "Spot 4: Room 3 Center Sand Floor Rest",
        "desc": "File: A03_00.00-06.56_dur_6h56m.mp4 | In-video: 01:28:00 - 01:34:00"
    },
    {
        "cam": 3,
        "file": "A03_14.03-18.18_dur_4h14m.mp4",
        "sec": 120 * 60, # 16:03:27
        "clock": "16:03:27",
        "title": "Spot 2: Room 3 Straw Tire Bed",
        "desc": "File: A03_14.03-18.18_dur_4h14m.mp4 | In-video: 00:00:00 - 02:16:33"
    },
    {
        "cam": 3,
        "file": "A03_14.03-18.18_dur_4h14m.mp4",
        "sec": 150 * 60, # 16:33:27
        "clock": "16:33:27",
        "title": "Spot 3: Room 3 Under Log (Right Fence)",
        "desc": "File: A03_14.03-18.18_dur_4h14m.mp4 | In-video: 02:21:33 - 03:06:33"
    },
    {
        "cam": 2,
        "file": "A02_11.07-12.41_dur_1h34m.mp4",
        "sec": 45 * 60, # 11:52:05
        "clock": "11:52:05",
        "title": "Spot 5: Room 2 Ramp Post-Feeding Rest",
        "desc": "File: A02_11.07-12.41_dur_1h34m.mp4 | In-video: 00:38:00 - 00:58:00"
    }
]

for i, sp in enumerate(spots):
    vp = os.path.join(base, f"camera {sp['cam']}", sp["file"])
    cap = cv2.VideoCapture(vp)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(sp["sec"] * fps))
    ret, frame = cap.read()
    cap.release()
    if ret:
        vis = cv2.resize(frame, (960, 540))
        # Draw header banner
        cv2.rectangle(vis, (0, 0), (960, 60), (20, 20, 20), -1)
        cv2.putText(vis, sp["title"], (20, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(vis, f"Clock: {sp['clock']} | {sp['desc']}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1)
        out_name = f"spot_{i+1}_{sp['cam']}_{sp['file'][:7]}.jpg"
        cv2.imwrite(os.path.join(out_dir, out_name), vis)
        print(f"Generated {out_name}: {sp['title']}")

print("All summary cards generated successfully!")
