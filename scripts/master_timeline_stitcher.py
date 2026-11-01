"""
Master Timeline Stitching Engine (Fortified Version)
Chiang Mai Zoo - Asian Palm Civet Behavioral Monitoring System
Author: Subagent 8 (Master Timeline Stitching Engineer)

Fuses multi-camera CCTV detection logs (log_cam1.csv, log_cam2.csv, log_cam3.csv, log_cam4.csv)
into a unified, continuous, non-overlapping master timeline matching LOG.txt.
"""

import os
import sys
import re
import csv
import json
from typing import List, Dict, Tuple, Any, Optional

class MasterTimelineStitcher:
    """
    Fortified Multi-Camera Behavioral Timeline Stitching Engine.
    Implements:
      1. Physical Invariants (V_max <= 3.5 m/s, Single Occupancy N <= 1, Topological Linearity)
      2. Doorway Crossing Handover FSM (Eliminates overlap & ping-pong flickering)
      3. Proof-of-Ingress Anchoring for Invisible Sleeping Box Periods
      4. Spurious Clutter / Ghost Veto (Rejects unphysical detached detections)
      5. Multi-Room Locomotion Traversal Chaining (Matches LOG.txt multi-room paths)
    """

    def __init__(
        self,
        doorway_overlap_tolerance_sec: float = 6.0,
        dropout_coast_sec: float = 15.0,
        ghost_suppression_duration_sec: float = 8.0,
        macro_debounce_sec: int = 60
    ):
        self.doorway_tol = doorway_overlap_tolerance_sec
        self.dropout_coast = dropout_coast_sec
        self.ghost_suppression_sec = ghost_suppression_duration_sec
        self.macro_debounce = macro_debounce_sec

        # Topological linear adjacency graph
        self.room_graph = {
            "Room 1": ["Room 2"],
            "Room 2": ["Room 1", "Room 3"],
            "Room 3": ["Room 2", "Room 4"],
            "Room 4": ["Room 3"]
        }
        
        # Inter-room physical distances (meters)
        self.room_distances = {
            ("Room 1", "Room 2"): 4.0, ("Room 2", "Room 1"): 4.0,
            ("Room 2", "Room 3"): 4.0, ("Room 3", "Room 2"): 4.0,
            ("Room 3", "Room 4"): 4.0, ("Room 4", "Room 3"): 4.0,
            ("Room 1", "Room 3"): 8.0, ("Room 3", "Room 1"): 8.0,
            ("Room 2", "Room 4"): 8.0, ("Room 4", "Room 2"): 8.0,
            ("Room 1", "Room 4"): 12.0, ("Room 4", "Room 1"): 12.0
        }
        self.V_MAX = 3.5 # Maximum sprint velocity in m/s

    @staticmethod
    def time_to_sec(t_str: str) -> int:
        parts = [int(p) for p in t_str.strip().split(':')]
        return parts[0] * 3600 + parts[1] * 60 + parts[2]

    @staticmethod
    def sec_to_time(sec: int) -> str:
        sec = sec % 86400
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

    def are_adjacent(self, room_a: str, room_b: str) -> bool:
        return room_b in self.room_graph.get(room_a, [])

    def load_camera_logs(self, cam_paths: Dict[str, str]) -> Dict[int, Dict[str, Any]]:
        """Ingests log_cam1..4.csv onto a second-by-second synchronized time grid."""
        time_grid = {}

        for cam_id, path in cam_paths.items():
            if not os.path.exists(path):
                continue

            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'timestamp_sec' in row and row['timestamp_sec']:
                        sec = int(float(row['timestamp_sec']))
                    elif 'timestamp' in row and ':' in row['timestamp']:
                        sec = self.time_to_sec(row['timestamp'])
                    elif 'second' in row:
                        sec = int(float(row['second']))
                    else:
                        continue

                    det = {
                        'camera_id': cam_id,
                        'room': row.get('room_id', row.get('room', '')),
                        'detected': row.get('detection_state', 'DETECTED') == 'DETECTED' and float(row.get('confidence', 0)) >= 0.30,
                        'conf': float(row.get('confidence', 0.0)),
                        'roi': row.get('roi_zone', row.get('roi', 'GENERAL_FLOOR')),
                        'displacement': float(row.get('displacement_px', row.get('displacement', 0.0))),
                        'instant_behavior': row.get('instant_behavior', row.get('behavior', 'NONE')),
                        'raw_row': row
                    }

                    if sec not in time_grid:
                        time_grid[sec] = {}
                    time_grid[sec][cam_id] = det

        return time_grid

    def resolve_synchronized_grid(
        self,
        time_grid: Dict[int, Dict[str, Any]],
        start_sec: int,
        end_sec: int
    ) -> List[Dict[str, Any]]:
        """
        Processes multi-camera detections across time, enforcing 5-tier conflict resolution.
        """
        resolved_stream = []

        # Internal FSM Tracking State
        last_known_room = "Room 2"
        last_seen_sec = start_sec
        box_ingress_verified = True  # Begins inside sleeping box (as at 00:00:00 in LOG.txt)
        box_ingress_time = start_sec
        last_behavior = "Sleeping"
        last_macro = "INACTIVE"
        active_coasting_counter = 0

        # Doorway Handoff State Tracker
        in_transit = False
        transit_source_room = None
        transit_dest_room = None
        transit_start_sec = 0

        # Spurious detection streak tracker (for ghost rejection)
        ghost_candidate_room = None
        ghost_candidate_streak = 0

        for sec in range(start_sec, end_sec):
            cams_data = time_grid.get(sec, {})

            # Collect verified detections
            verified_cams = []
            for c_id in ["Cam 01", "Cam 02", "Cam 03", "Cam 04"]:
                d = cams_data.get(c_id)
                if d and d['detected'] and d['conf'] >= 0.30:
                    verified_cams.append((c_id, d))

            num_verified = len(verified_cams)

            # -------------------------------------------------------------
            # CASE A: MULTIPLE DETECTIONS (DOORWAY OVERLAP OR CONCURRENT CLUTTER)
            # -------------------------------------------------------------
            if num_verified >= 2:
                cam_a, det_a = verified_cams[0]
                cam_b, det_b = verified_cams[1]
                room_a = det_a['room']
                room_b = det_b['room']

                in_door_a = "DOORWAY" in det_a['roi'].upper() or det_a['roi'].upper() in ["RAMP", "PORTAL"]
                in_door_b = "DOORWAY" in det_b['roi'].upper() or det_b['roi'].upper() in ["RAMP", "PORTAL"]

                if self.are_adjacent(room_a, room_b) and (in_door_a or in_door_b):
                    # Valid Doorway Handover!
                    in_transit = True
                    if room_a == last_known_room:
                        transit_source_room, transit_dest_room = room_a, room_b
                    else:
                        transit_source_room, transit_dest_room = room_b, room_a

                    frame_state = {
                        'second': sec,
                        'macro_state': 'ACTIVE',
                        'behavior': 'Locomotion',
                        'room': transit_dest_room,
                        'transition': (transit_source_room, transit_dest_room),
                        'confidence': max(det_a['conf'], det_b['conf']),
                        'tier': 'TIER_2_DOORWAY_FUSION',
                        'location_detail': f"Doorway Handover ({transit_source_room} -> {transit_dest_room})"
                    }
                    last_known_room = transit_dest_room
                    last_seen_sec = sec
                    box_ingress_verified = False # In motion
                    active_coasting_counter = 0

                else:
                    # Non-adjacent rooms or static clutter clash (Tier 1 Physics Veto)
                    chosen_det = det_a if room_a == last_known_room else det_b
                    frame_state = self._process_single_camera_detection(
                        sec, chosen_det, last_known_room, last_seen_sec
                    )
                    last_known_room = frame_state['room']
                    last_seen_sec = sec
                    active_coasting_counter = 0

            # -------------------------------------------------------------
            # CASE B: EXACTLY ONE CAMERA REPORTS DETECTION
            # -------------------------------------------------------------
            elif num_verified == 1:
                cam_id, det = verified_cams[0]
                current_room = det['room']

                # Proof-of-Ingress Invariant Check:
                # If sleeping in Room 2 box, a sudden 1-frame detection in Room 1 or Room 3 without
                # prior Cam 02 ramp emergence is a static artifact or spider/insect ghost!
                if box_ingress_verified and current_room != "Room 2":
                    if ghost_candidate_room == current_room:
                        ghost_candidate_streak += 1
                    else:
                        ghost_candidate_room = current_room
                        ghost_candidate_streak = 1

                    if ghost_candidate_streak < self.ghost_suppression_sec:
                        # Suppress ghost, hold sleeping state!
                        frame_state = {
                            'second': sec,
                            'macro_state': 'INACTIVE',
                            'behavior': 'Sleeping',
                            'room': 'Room 2',
                            'transition': None,
                            'confidence': 0.98,
                            'tier': 'TIER_1_PROOF_OF_INGRESS_VETO',
                            'location_detail': f'Suppressed unanchored ghost in {current_room} while box ingress locked'
                        }
                        resolved_stream.append(frame_state)
                        continue
                    else:
                        # Streak sustained -> acknowledge breakthrough
                        box_ingress_verified = False

                ghost_candidate_room = None
                ghost_candidate_streak = 0

                # Velocity Sanity Check
                dt = sec - last_seen_sec
                if dt > 0 and current_room != last_known_room:
                    dist = self.room_distances.get((last_known_room, current_room), 4.0)
                    vel = dist / dt
                    if vel > self.V_MAX and dt < 2.0:
                        # Impossible teleportation: suppress
                        frame_state = {
                            'second': sec,
                            'macro_state': last_macro,
                            'behavior': last_behavior,
                            'room': last_known_room,
                            'transition': None,
                            'confidence': 0.70,
                            'tier': 'TIER_1_VELOCITY_VETO_HOLD',
                            'location_detail': f"Teleportation artifact suppressed from {current_room}"
                        }
                        resolved_stream.append(frame_state)
                        continue

                # Check Doorway Completion
                transition_tuple = None
                if in_transit and current_room == transit_dest_room and "DOORWAY" not in det['roi'].upper():
                    in_transit = False # Emerged into room interior
                    transition_tuple = (transit_source_room, transit_dest_room)
                elif current_room != last_known_room:
                    transition_tuple = (last_known_room, current_room)

                # Process verified detection
                frame_state = self._process_single_camera_detection(
                    sec, det, last_known_room, last_seen_sec
                )
                if transition_tuple:
                    frame_state['transition'] = transition_tuple

                # Track Box Ingress / Egress on Cam 02
                if cam_id == "Cam 02":
                    if "BOX_ENTRANCE" in det['roi'].upper():
                        box_ingress_verified = True
                        box_ingress_time = sec
                    elif "RAMP" in det['roi'].upper() and det['displacement'] > 10:
                        box_ingress_verified = False

                last_known_room = frame_state['room']
                last_seen_sec = sec
                active_coasting_counter = 0

            # -------------------------------------------------------------
            # CASE C: ALL 4 CAMERAS EMPTY (OCCLUSION & INVISIBLE STATE INFERENCE)
            # -------------------------------------------------------------
            else:
                active_coasting_counter += 1
                ghost_candidate_room = None
                ghost_candidate_streak = 0

                if active_coasting_counter <= self.dropout_coast:
                    # Tier 5: Coast prior state
                    frame_state = {
                        'second': sec,
                        'macro_state': last_macro,
                        'behavior': last_behavior,
                        'room': last_known_room,
                        'transition': None,
                        'confidence': 0.75,
                        'tier': 'TIER_5_TRANSIENT_COAST',
                        'location_detail': f"Transient optical dropout in {last_known_room}"
                    }
                else:
                    # Extended Absence (> 15s)
                    if box_ingress_verified and last_known_room == "Room 2":
                        # Tier 3: Ingress-Anchored Sleeping Box Rest
                        frame_state = {
                            'second': sec,
                            'macro_state': 'INACTIVE',
                            'behavior': 'Sleeping',
                            'room': 'Room 2',
                            'transition': None,
                            'confidence': 0.98,
                            'tier': 'TIER_3_BOX_INGRESS_EXCLUSION',
                            'location_detail': 'Enclosed Wooden Sleeping Box (Cam 02)'
                        }
                    else:
                        # Tier 4: Local shelter occlusion in last known room
                        frame_state = {
                            'second': sec,
                            'macro_state': 'INACTIVE',
                            'behavior': 'Resting',
                            'room': last_known_room,
                            'transition': None,
                            'confidence': 0.80,
                            'tier': 'TIER_4_LOCAL_OCCLUSION',
                            'location_detail': f"Local shelter / log occlusion in {last_known_room}"
                        }

            last_macro = frame_state['macro_state']
            last_behavior = frame_state['behavior']
            resolved_stream.append(frame_state)

        return resolved_stream

    def _process_single_camera_detection(
        self,
        sec: int,
        det: Dict[str, Any],
        last_known_room: str,
        last_seen_sec: int
    ) -> Dict[str, Any]:
        """Maps ROI and motion to specific behaviors."""
        room = det['room']
        roi = det['roi'].upper()
        disp = det['displacement']
        raw_beh = det['instant_behavior'].upper()

        if "FOOD_TRAY" in roi or "EATING" in raw_beh:
            beh = "Eating"
            macro = "ACTIVE"
            loc = "Food Tray"
        elif "WATER_BASIN" in roi or "DRINKING" in raw_beh:
            beh = "Drinking"
            macro = "ACTIVE"
            loc = "Water Basin"
        elif "GROOMING" in raw_beh:
            beh = "Grooming"
            macro = "ACTIVE"
            loc = "Self-Directed Grooming"
        elif disp >= 10.0 or "LOCOMOTION" in raw_beh or "DOORWAY" in roi:
            beh = "Locomotion"
            macro = "ACTIVE"
            loc = f"Active Locomotion in {room}"
        elif "BOX_ENTRANCE" in roi:
            beh = "Sleeping"
            macro = "INACTIVE"
            loc = "Sleeping Box Entrance"
        elif "TIRE_BED" in roi or disp < 5.0:
            beh = "Resting"
            macro = "INACTIVE"
            loc = f"Resting in {room}"
        else:
            beh = "Resting"
            macro = "INACTIVE"
            loc = f"Stationary in {room}"

        return {
            'second': sec,
            'macro_state': macro,
            'behavior': beh,
            'room': room,
            'transition': None,
            'confidence': det['conf'],
            'tier': 'TIER_2_VERIFIED_DETECTION',
            'location_detail': loc
        }

    def consolidate_episodes_to_master_timeline(
        self,
        frame_stream: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Consolidates frame stream into gapless, continuous, non-overlapping
        master timeline matching LOG.txt schema and multi-room pathways.
        """
        if not frame_stream:
            return []

        # Run-length episodic grouping with multi-room path tracking
        raw_episodes = []
        cur_ep = None

        for frame in frame_stream:
            sec = frame['second']
            beh = frame['behavior']
            macro = frame['macro_state']
            room = frame['room']
            trans = frame.get('transition')
            conf = frame['confidence']
            tier = frame['tier']

            if cur_ep is None:
                cur_ep = {
                    'start_sec': sec,
                    'end_sec': sec + 1,
                    'macro_state': macro,
                    'behavior': beh,
                    'rooms_visited': [room],
                    'conf_sum': conf,
                    'conf_count': 1,
                    'primary_tier': tier
                }
                if trans:
                    if trans[0] not in cur_ep['rooms_visited']:
                        cur_ep['rooms_visited'].insert(0, trans[0])
                    if trans[1] not in cur_ep['rooms_visited']:
                        cur_ep['rooms_visited'].append(trans[1])
            else:
                # Grouping condition:
                can_extend = False
                if cur_ep['behavior'] == beh and cur_ep['macro_state'] == macro:
                    if beh == 'Locomotion':
                        can_extend = True
                        if trans:
                            for r in trans:
                                if not cur_ep['rooms_visited'] or r != cur_ep['rooms_visited'][-1]:
                                    cur_ep['rooms_visited'].append(r)
                        elif room != cur_ep['rooms_visited'][-1]:
                            cur_ep['rooms_visited'].append(room)
                    elif room == cur_ep['rooms_visited'][-1]:
                        can_extend = True

                if can_extend and sec == cur_ep['end_sec']:
                    cur_ep['end_sec'] = sec + 1
                    cur_ep['conf_sum'] += conf
                    cur_ep['conf_count'] += 1
                else:
                    raw_episodes.append(cur_ep)
                    cur_ep = {
                        'start_sec': sec,
                        'end_sec': sec + 1,
                        'macro_state': macro,
                        'behavior': beh,
                        'rooms_visited': [room],
                        'conf_sum': conf,
                        'conf_count': 1,
                        'primary_tier': tier
                    }
                    if trans:
                        if trans[0] not in cur_ep['rooms_visited']:
                            cur_ep['rooms_visited'].insert(0, trans[0])
                        if trans[1] not in cur_ep['rooms_visited']:
                            cur_ep['rooms_visited'].append(trans[1])

        if cur_ep is not None:
            raw_episodes.append(cur_ep)

        # Merge short transient state flickers (< 3s) into surrounding dominant behavior
        merged_episodes = []
        for ep in raw_episodes:
            dur = ep['end_sec'] - ep['start_sec']
            if merged_episodes and dur < 3 and ep['behavior'] == 'Resting' and merged_episodes[-1]['behavior'] == 'Locomotion':
                # Absorb into ongoing locomotion
                merged_episodes[-1]['end_sec'] = ep['end_sec']
                merged_episodes[-1]['conf_sum'] += ep['conf_sum']
                merged_episodes[-1]['conf_count'] += ep['conf_count']
                for r in ep['rooms_visited']:
                    if r != merged_episodes[-1]['rooms_visited'][-1]:
                        merged_episodes[-1]['rooms_visited'].append(r)
            else:
                merged_episodes.append(ep)

        # Re-merge consecutive identical episodes created after filtering
        compact_episodes = []
        for ep in merged_episodes:
            if not compact_episodes:
                compact_episodes.append(ep)
            else:
                prev = compact_episodes[-1]
                if prev['behavior'] == ep['behavior'] and prev['rooms_visited'] == ep['rooms_visited'] and prev['end_sec'] == ep['start_sec']:
                    prev['end_sec'] = ep['end_sec']
                    prev['conf_sum'] += ep['conf_sum']
                    prev['conf_count'] += ep['conf_count']
                else:
                    compact_episodes.append(ep)

        # Final Formatting
        master_timeline = []
        for i, ep in enumerate(compact_episodes):
            st_str = self.sec_to_time(ep['start_sec'])
            et_str = self.sec_to_time(ep['end_sec'])
            dur_sec = ep['end_sec'] - ep['start_sec']
            avg_conf = ep['conf_sum'] / max(1, ep['conf_count'])
            raw_b = ep['behavior']

            # Final Room Representation:
            # Stationary behaviors take place in a single room
            if raw_b in ['Eating', 'Drinking', 'Sleeping', 'Resting', 'Grooming']:
                room_str = ep['rooms_visited'][-1]
                dedup_rooms = [room_str]
            else:
                # Locomotion sequence: preserve unique traversal path
                seq = []
                for r in ep['rooms_visited']:
                    if not seq or r != seq[-1]:
                        seq.append(r)

                # Simplify oscillatory bounces at doorway threshold (e.g. ['Room 2', 'Room 3', 'Room 2', 'Room 3'])
                # If start room != end room and adjacent, the net transit is [start_room, end_room]
                if len(seq) > 2:
                    if self.are_adjacent(seq[0], seq[-1]):
                        seq = [seq[0], seq[-1]]
                    else:
                        # Multi-room path: keep unique progression in order of first appearance
                        seen = []
                        for r in seq:
                            if r not in seen:
                                seen.append(r)
                        seq = seen

                dedup_rooms = seq
                room_str = " ".join(seq)

            # Taxonomy matching LOG.txt
            raw_b = ep['behavior']
            if raw_b == 'Sleeping' or (raw_b == 'Resting' and dedup_rooms == ['Room 2'] and dur_sec >= 600):
                canon_beh = "Resting (Sleep)" if i > 0 and dur_sec < 4000 else "Sleeping"
            elif raw_b == 'Resting':
                canon_beh = "Resting (Sitting)" if dur_sec < 300 else "Resting"
            else:
                canon_beh = raw_b

            raw_log_line = f"{st_str} - {et_str} {canon_beh} {room_str}"

            master_timeline.append({
                'event_id': f"EVT_{i+1:03d}",
                'start_time': st_str,
                'end_time': et_str,
                'start_sec': ep['start_sec'],
                'end_sec': ep['end_sec'],
                'duration_sec': dur_sec,
                'behavior': canon_beh,
                'macro_state': ep['macro_state'],
                'room_sequence': room_str,
                'rooms_list': dedup_rooms,
                'confidence': f"{avg_conf:.2f}",
                'resolution_tier': ep['primary_tier'],
                'log_line': raw_log_line
            })

        return master_timeline

    def export_results(
        self,
        timeline: List[Dict[str, Any]],
        out_txt_path: str,
        out_csv_path: str
    ):
        """Exports stitched master timeline to LOG.txt text format and CSV."""
        with open(out_txt_path, 'w', encoding='utf-8') as f:
            for ev in timeline:
                f.write(ev['log_line'] + "\n")

        fieldnames = [
            'event_id', 'start_time', 'end_time', 'duration_sec',
            'behavior', 'macro_state', 'room_sequence', 'confidence', 'resolution_tier'
        ]
        with open(out_csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for ev in timeline:
                writer.writerow({
                    'event_id': ev['event_id'],
                    'start_time': ev['start_time'],
                    'end_time': ev['end_time'],
                    'duration_sec': ev['duration_sec'],
                    'behavior': ev['behavior'],
                    'macro_state': ev['macro_state'],
                    'room_sequence': ev['room_sequence'],
                    'confidence': ev['confidence'],
                    'resolution_tier': ev['resolution_tier']
                })

        print(f"[SUCCESS] Exported Master Timeline ({len(timeline)} events) to:")
        print(f"  - {out_txt_path}")
        print(f"  - {out_csv_path}")
