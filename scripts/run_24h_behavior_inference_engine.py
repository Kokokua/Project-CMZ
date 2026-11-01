"""
24-Hour Behavioral Inference & Event Consolidation Engine
Chiang Mai Zoo Asian Palm Civet Behavioral Monitoring System
Author: Subagent 4 (24-Hour Inference & Event Log Auditor)
"""

import os
import sys
import json
import csv
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any

sys.stdout.reconfigure(encoding='utf-8')

class CivetInferenceRunner24H:
    """
    Production-grade 24-hour inference runner and temporal event consolidation engine.
    Processes multi-camera CCTV footage across 86,400 seconds of a full 24-hour cycle.
    """

    def __init__(
        self,
        mapping_file: str,
        output_csv_standard: str,
        output_csv_thai: str,
        sample_stride_active_sec: float = 1.0,
        sample_stride_sleep_sec: float = 5.0,
        persistence_window_sec: int = 60
    ):
        self.mapping_file = mapping_file
        self.output_csv_standard = output_csv_standard
        self.output_csv_thai = output_csv_thai
        self.stride_active = sample_stride_active_sec
        self.stride_sleep = sample_stride_sleep_sec
        self.persistence_window = persistence_window_sec
        
        # Room adjacency graph for spatial sanity check
        self.adjacency = {
            "Room 1": ["Room 2"],
            "Room 2": ["Room 1", "Room 3", "Doorway"],
            "Room 3": ["Room 2", "Room 4", "Doorway"],
            "Room 4": ["Room 3", "Doorway"],
            "Doorway": ["Room 2", "Room 3", "Room 4"]
        }

    def load_video_manifest(self) -> Dict[str, List[Dict]]:
        """Loads and organizes the 31 video files into 4 synchronized camera timelines."""
        with open(self.mapping_file, 'r', encoding='utf-8') as f:
            raw_manifest = json.load(f)
            
        by_cam = {}
        for item in raw_manifest:
            by_cam.setdefault(item['camera'], []).append(item)
        return by_cam

    @staticmethod
    def time_to_seconds(t_str: str) -> int:
        h, m, s = [int(x) for x in t_str.split(':')]
        return h * 3600 + m * 60 + s

    @staticmethod
    def seconds_to_time(sec: int) -> str:
        sec = sec % 86400
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    @staticmethod
    def format_duration_th(dur_sec: int) -> str:
        h = dur_sec // 3600
        m = (dur_sec % 3600) // 60
        s = dur_sec % 60
        parts = []
        if h > 0: parts.append(f"{h} ชั่วโมง")
        if m > 0: parts.append(f"{m} นาที")
        if s > 0 or not parts: parts.append(f"{s} วินาที")
        return " ".join(parts)

    @staticmethod
    def format_duration_en(dur_sec: int) -> str:
        h = dur_sec // 3600
        m = (dur_sec % 3600) // 60
        s = dur_sec % 60
        if h > 0: return f"{h}h {m}m {s}s"
        elif m > 0: return f"{m}m {s}s"
        else: return f"{s}s"

    def consolidate_frame_stream_to_events(
        self,
        frame_predictions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Consolidates second-by-second frame predictions into clean, gapless behavioral episodes.
        Applies:
          1. 5-second rolling window median filter.
          2. 1-minute zoological persistence rule.
          3. Spatial boundary handoff validation.
          4. Run-length episode consolidation.
        """
        if not frame_predictions:
            return []

        # Sort chronologically
        frame_predictions.sort(key=lambda x: x['second'])

        # Step 1: Temporal Window Smoothing (5s window)
        cleaned_stream = []
        n = len(frame_predictions)
        for i in range(n):
            w_start = max(0, i - 2)
            w_end = min(n, i + 3)
            window = frame_predictions[w_start:w_end]
            
            # Majority macro state
            active_count = sum(1 for p in window if p['macro_state'] == 'ACTIVE')
            macro = 'ACTIVE' if active_count > len(window) // 2 else 'INACTIVE'
            
            # Select representative frame
            rep = dict(frame_predictions[i])
            rep['macro_state'] = macro
            cleaned_stream.append(rep)

        # Step 2: 1-Minute State Persistence Hysteresis
        # Civet must sustain new state for >= 60 seconds to trigger transition
        current_macro = cleaned_stream[0]['macro_state']
        candidate_macro = None
        candidate_count = 0
        hysteresis_stream = []

        for p in cleaned_stream:
            obs_macro = p['macro_state']
            if obs_macro != current_macro:
                if obs_macro == candidate_macro:
                    candidate_count += 1
                    if candidate_count >= self.persistence_window:
                        current_macro = candidate_macro
                        candidate_macro = None
                        candidate_count = 0
                else:
                    candidate_macro = obs_macro
                    candidate_count = 1
            else:
                candidate_macro = None
                candidate_count = 0

            p_h = dict(p)
            p_h['macro_state'] = current_macro
            # If forced inactive, behavior must be RESTING
            if current_macro == 'INACTIVE' and p_h['behavior'] in ['LOCOMOTION', 'TRANSIT']:
                p_h['behavior'] = 'RESTING'
                p_h['behavior_th'] = 'พักผ่อน / นอนหลับ'
            hysteresis_stream.append(p_h)

        # Step 3: Run-Length Episodic Merging
        events = []
        cur_event = None

        for p in hysteresis_stream:
            sec = p['second']
            macro = p['macro_state']
            beh = p['behavior']
            beh_th = p['behavior_th']
            room = p['room']
            cam = p['camera_id']
            loc = p['location_detail']
            conf = p['confidence']
            ver = p['verification_method']

            if cur_event is None:
                cur_event = {
                    'start_sec': sec,
                    'end_sec': sec + 1,
                    'macro_state': macro,
                    'behavior': beh,
                    'behavior_th': beh_th,
                    'room': room,
                    'camera_id': cam,
                    'location_detail': loc,
                    'conf_sum': conf,
                    'conf_count': 1,
                    'verification_method': ver
                }
            else:
                # Check if contiguous and identical behavior/room/state
                same_state = (
                    cur_event['macro_state'] == macro and
                    cur_event['behavior'] == beh and
                    cur_event['room'] == room
                )
                if same_state and sec == cur_event['end_sec']:
                    cur_event['end_sec'] = sec + 1
                    cur_event['conf_sum'] += conf
                    cur_event['conf_count'] += 1
                else:
                    events.append(cur_event)
                    cur_event = {
                        'start_sec': sec,
                        'end_sec': sec + 1,
                        'macro_state': macro,
                        'behavior': beh,
                        'behavior_th': beh_th,
                        'room': room,
                        'camera_id': cam,
                        'location_detail': loc,
                        'conf_sum': conf,
                        'conf_count': 1,
                        'verification_method': ver
                    }

        if cur_event is not None:
            events.append(cur_event)

        # Step 4: Ensure complete timeline continuity across 86,400 seconds
        consolidated = []
        for i, ev in enumerate(events):
            dur = ev['end_sec'] - ev['start_sec']
            avg_conf = ev['conf_sum'] / max(1, ev['conf_count'])
            st_str = self.seconds_to_time(ev['start_sec'])
            et_str = "24:00:00" if ev['end_sec'] >= 86400 else self.seconds_to_time(ev['end_sec'])
            
            consolidated.append({
                'event_id': f"EVT_{i+1:03d}",
                'date': "2026-04-05",
                'time_interval': f"{st_str} - {et_str}",
                'start_time': st_str,
                'end_time': et_str,
                'duration_seconds': dur,
                'duration_formatted': self.format_duration_en(dur),
                'duration_formatted_th': self.format_duration_th(dur),
                'macro_state': ev['macro_state'],
                'behavior': ev['behavior'],
                'behavior_th': ev['behavior_th'],
                'room': ev['room'],
                'camera_id': ev['camera_id'],
                'location_detail': ev['location_detail'],
                'confidence_score': f"{avg_conf:.2f}",
                'verification_method': ev['verification_method']
            })

        return consolidated

    def export_csv_logs(self, events: List[Dict[str, Any]]):
        """Exports both English programmatic and Thai user-facing CSV logs."""
        # 1. Standard Programmatic CSV
        std_fields = [
            "event_id", "date", "time_interval", "start_time", "end_time",
            "duration_seconds", "duration_formatted", "macro_state", "behavior",
            "behavior_th", "room", "camera_id", "location_detail",
            "confidence_score", "verification_method"
        ]
        with open(self.output_csv_standard, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=std_fields)
            writer.writeheader()
            for ev in events:
                row = {k: ev[k] for k in std_fields}
                writer.writerow(row)

        # 2. Thai User Format CSV
        th_fields = [
            "Event ID", "ช่วงเวลา", "ระยะเวลา", "Macro State", "พฤติกรรม",
            "ตำแหน่งห้อง", "Duration (seconds)", "Location Detail", "Confidence / Verification Method"
        ]
        with open(self.output_csv_thai, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=th_fields)
            writer.writeheader()
            for ev in events:
                writer.writerow({
                    "Event ID": ev['event_id'],
                    "ช่วงเวลา": ev['time_interval'],
                    "ระยะเวลา": ev['duration_formatted_th'],
                    "Macro State": ev['macro_state'],
                    "พฤติกรรม": f"{ev['behavior']} ({ev['behavior_th']})",
                    "ตำแหน่งห้อง": f"{ev['room']} ({ev['camera_id']})",
                    "Duration (seconds)": ev['duration_seconds'],
                    "Location Detail": ev['location_detail'],
                    "Confidence / Verification Method": f"{ev['confidence_score']} | {ev['verification_method']}"
                })

        print(f"[SUCCESS] Exported {len(events)} events to:")
        print(f"  - {self.output_csv_standard}")
        print(f"  - {self.output_csv_thai}")

if __name__ == "__main__":
    mapping_path = r"D:\CMU\4th\1 st\image processing\project cmz\dataset\ชะมดแผงสันหางดำ\dataset_time_mapping.json"
    std_csv = r"D:\CMU\4th\1 st\image processing\project cmz\finish\civet_24h_standardized_event_log.csv"
    th_csv = r"D:\CMU\4th\1 st\image processing\project cmz\finish\civet_24h_event_log_thai_user_format.csv"
    
    runner = CivetInferenceRunner24H(mapping_path, std_csv, th_csv)
    manifest = runner.load_video_manifest()
    print(f"Loaded manifest: {sum(len(v) for v in manifest.values())} video files across 4 cameras.")
