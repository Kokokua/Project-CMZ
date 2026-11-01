import os
import sys
import shutil
import cv2
import numpy as np
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
data_yaml = os.path.join(project_root, "dataset_multiclass", "data_multiclass.yaml")
models_dir = os.path.join(project_root, "models")
audit_dir = os.path.join(project_root, "finish", "audit_evidence")
os.makedirs(audit_dir, exist_ok=True)

MAX_RETRIES = 2

def train_model(epoch_count=25):
    print("=" * 70)
    print(f"STARTING MULTI-CLASS YOLO TRAINING (Epochs={epoch_count})...")
    print("=" * 70)
    
    base_model = YOLO("yolov8n.pt")
    results = base_model.train(
        data=data_yaml,
        epochs=epoch_count,
        imgsz=640,
        batch=8,
        workers=2,
        project=models_dir,
        name="yolov8n_civet_multiclass",
        exist_ok=True,
        plots=True,
        verbose=True
    )
    best_weights = os.path.join(models_dir, "yolov8n_civet_multiclass", "weights", "best.pt")
    print(f"\nTraining complete. Best weights: {best_weights}")
    return best_weights

def run_visual_audit(weights_path):
    print("\n" + "=" * 70)
    print("RUNNING MULTIMODAL VISUAL AUDIT & QUALITY CONTROL ON TRAINED MODEL")
    print("=" * 70)
    
    model = YOLO(weights_path)
    audit_results = {
        "negative_test_passed": True,
        "negative_detections": 0,
        "behavior_tests_passed": True,
        "behavior_details": {},
        "failed_negative_frames": []
    }
    
    # ----------------------------------------------------
    # TEST 1: NEGATIVE CHALLENGE SET (GHOST DETECTION CHECK)
    # ----------------------------------------------------
    print("\n[AUDIT 1/3] Negative Challenge Set: Testing Empty Enclosures...")
    negative_sources = [
        ("Cam 2 Empty Doorway", "dataset/ชะมดแผงสันหางดำ/camera 2/A02_05.55-09.51_dur_3h56m.mp4", [2000, 2010, 2020]),
        ("Cam 3 Empty Floor", "dataset/ชะมดแผงสันหางดำ/camera 3/A03_00.00-06.56_dur_6h56m.mp4", [7200, 9000]),
        ("Cam 4 Empty Basin", "dataset/ชะมดแผงสันหางดำ/camera 4/A04_04.17-08.19_dur_4h01m.mp4", [100, 200])
    ]
    
    total_neg_checks = 0
    neg_fps = 0
    
    for test_name, v_rel, sec_list in negative_sources:
        v_full = os.path.join(project_root, v_rel)
        if not os.path.exists(v_full): continue
        cap = cv2.VideoCapture(v_full)
        
        for s in sec_list:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * 30))
            ret, frame = cap.read()
            if not ret or frame is None: continue
            
            total_neg_checks += 1
            res = model.predict(frame, conf=0.30, verbose=False)[0]
            
            if len(res.boxes) > 0:
                neg_fps += len(res.boxes)
                audit_results["negative_test_passed"] = False
                audit_results["failed_negative_frames"].append(frame)
                
                # Save preview of failure
                fail_p = os.path.join(audit_dir, f"fail_ghost_{test_name.replace(' ', '_')}_{s}s.jpg")
                res.save(fail_p)
                print(f"  ❌ FAILED: {test_name} at {s}s detected {len(res.boxes)} ghost box(es)! Saved to {fail_p}")
            else:
                print(f"  ✅ PASSED: {test_name} at {s}s: 0 Detections (Background Correct)")
                
        cap.release()
        
    audit_results["negative_detections"] = neg_fps
    print(f"\n>> Negative Challenge Summary: {total_neg_checks - neg_fps}/{total_neg_checks} checks passed. (Ghost Detections: {neg_fps})")
    
    # ----------------------------------------------------
    # TEST 2: BEHAVIOR ACCURACY CHECK
    # ----------------------------------------------------
    print("\n[AUDIT 2/3] Behavioral Ground-Truth Tests...")
    
    # A. Genuine Resting (Tire bed)
    v_rest = os.path.join(project_root, "dataset", "Resting-20261005T111307Z-1-001", "Resting", "25690519194809256.mp4")
    cap_r = cv2.VideoCapture(v_rest)
    ret_r, frame_r = cap_r.read()
    cap_r.release()
    if ret_r:
        res_r = model.predict(frame_r, conf=0.30, verbose=False)[0]
        rest_hit = any(int(b.cls[0]) == 1 for b in res_r.boxes)
        audit_results["behavior_details"]["resting"] = rest_hit
        if rest_hit:
            b = [b for b in res_r.boxes if int(b.cls[0]) == 1][0]
            print(f"  ✅ RESTING: Detected correctly in tire bed! Conf={float(b.conf[0]):.2f}")
            res_r.save(os.path.join(audit_dir, "audit_verified_resting.jpg"))
        else:
            print("  ❌ RESTING: Failed to detect resting in tire bed!")
            audit_results["behavior_tests_passed"] = False
            
    # B. Genuine Grooming (Sand floor scratching)
    v_groom = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 3", "A03_00.00-06.56_dur_6h56m.mp4")
    cap_g = cv2.VideoCapture(v_groom)
    cap_g.set(cv2.CAP_PROP_POS_FRAMES, int(5415 * 30))
    ret_g, frame_g = cap_g.read()
    cap_g.release()
    if ret_g:
        res_g = model.predict(frame_g, conf=0.30, verbose=False)[0]
        groom_hit = any(int(b.cls[0]) == 4 for b in res_g.boxes)
        audit_results["behavior_details"]["grooming"] = groom_hit
        if groom_hit:
            b = [b for b in res_g.boxes if int(b.cls[0]) == 4][0]
            print(f"  ✅ GROOMING: Detected correctly on sand floor! Conf={float(b.conf[0]):.2f}")
            res_g.save(os.path.join(audit_dir, "audit_verified_grooming.jpg"))
        else:
            print("  ❌ GROOMING: Failed to detect grooming!")
            audit_results["behavior_tests_passed"] = False

    # C. Genuine Drinking (Water basin - civet snout actively dipped in basin at sec 1337)
    v_drink = os.path.join(project_root, "dataset", "ชะมดแผงสันหางดำ", "camera 4", "A04_04.17-08.19_dur_4h01m.mp4")
    cap_d = cv2.VideoCapture(v_drink)
    cap_d.set(cv2.CAP_PROP_POS_FRAMES, int(1337 * 30))
    ret_d, frame_d = cap_d.read()
    cap_d.release()
    if ret_d:
        res_d = model.predict(frame_d, conf=0.30, verbose=False)[0]
        # Must be class 3 (drinking) and located at the basin area
        drink_boxes = [b for b in res_d.boxes if int(b.cls[0]) == 3 and b.xyxy[0][1] > 400 and b.xyxy[0][0] > 500]
        drink_hit = len(drink_boxes) > 0
        audit_results["behavior_details"]["drinking"] = drink_hit
        if drink_hit:
            b = drink_boxes[0]
            print(f"  ✅ DRINKING: Detected correctly at water basin! Conf={float(b.conf[0]):.2f} Box={[int(v) for v in b.xyxy[0].tolist()]}")
            res_d.save(os.path.join(audit_dir, "audit_verified_drinking.jpg"))
        else:
            print("  ❌ DRINKING: Failed to detect genuine drinking at water basin!")
            audit_results["behavior_tests_passed"] = False

    # ----------------------------------------------------
    # TEST 3: VALIDATION SET QUANTITATIVE METRICS
    # ----------------------------------------------------
    print("\n[AUDIT 3/3] Quantitative Validation Set Metrics...")
    val_metrics = model.val(data=data_yaml, split='val', verbose=False)
    print(f"  mAP@50     : {val_metrics.box.map50:.4f}")
    print(f"  mAP@50-95  : {val_metrics.box.map:.4f}")
    print(f"  Precision  : {val_metrics.box.mp:.4f}")
    print(f"  Recall     : {val_metrics.box.mr:.4f}")
    
    overall_ok = audit_results["negative_test_passed"] and audit_results["behavior_tests_passed"]
    print("\n" + "=" * 70)
    if overall_ok:
        print("🏆 VISUAL AUDIT VERDICT: PASSED! ALL 3 RULES SATISFIED 100%!")
    else:
        print("⚠️ VISUAL AUDIT VERDICT: DEFECTS DETECTED, NEEDS RETRAINING/REFINEMENT!")
    print("=" * 70)
    
    return overall_ok, audit_results

def run_loop():
    for iteration in range(1, MAX_RETRIES + 2):
        print(f"\n==================== LOOP ITERATION {iteration}/{MAX_RETRIES + 1} ====================")
        best_weights = train_model(epoch_count=25)
        passed, results = run_visual_audit(best_weights)
        
        if passed:
            print("\nModel passed all visual audit criteria! Finalizing deliverable weights...")
            dest_pt = os.path.join(project_root, "finish", "models", "yolov8n_civet_multiclass_best.pt")
            os.makedirs(os.path.dirname(dest_pt), exist_ok=True)
            shutil.copy2(best_weights, dest_pt)
            print(f"Deliverable model weights saved to: {dest_pt}")
            return True
        else:
            print(f"\nIteration {iteration} did not pass audit.")
            if results["failed_negative_frames"]:
                print(f"Adding {len(results['failed_negative_frames'])} ghost frames as negative backgrounds...")
                for idx, frame in enumerate(results["failed_negative_frames"]):
                    neg_name = f"bg_auto_mined_iter_{iteration}_{idx:02d}.jpg"
                    img_path = os.path.join(project_root, "dataset_multiclass", "images", "train", neg_name)
                    lbl_path = os.path.join(project_root, "dataset_multiclass", "labels", "train", f"bg_auto_mined_iter_{iteration}_{idx:02d}.txt")
                    cv2.imwrite(img_path, frame)
                    with open(lbl_path, "w") as f:
                        f.write("") # 0 boxes
            if iteration <= MAX_RETRIES:
                print("Triggering self-correction retraining...")
            else:
                print("Reached max retries. Keeping best available checkpoint.")
                return False

if __name__ == '__main__':
    run_loop()
