"""
Standalone Civet Detection & Localization Inference Script
Model: YOLOv8n Fine-tuned on Asian Palm Civet (v3)
Chiang Mai Zoo x Chiang Mai University
"""

import argparse
import sys
from pathlib import Path
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="Run YOLOv8n Civet Detection Inference")
    parser.add_argument(
        "--weights", 
        type=str, 
        default="models/yolov8n_civet_v3/weights/best.pt",
        help="Path to fine-tuned model weights"
    )
    parser.add_argument(
        "--source", 
        type=str, 
        default="dataset_phase2/images/val",
        help="Path to input image, video, or folder of images"
    )
    parser.add_argument(
        "--conf", 
        type=float, 
        default=0.35,
        help="Confidence threshold (default: 0.35)"
    )
    parser.add_argument(
        "--iou", 
        type=float, 
        default=0.45,
        help="NMS IoU threshold (default: 0.45)"
    )
    parser.add_argument(
        "--save", 
        action="store_true", 
        default=True,
        help="Save annotated detection results"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    weights_path = Path(args.weights)
    if not weights_path.exists():
        print(f"Error: Weights file not found at '{weights_path}'")
        sys.exit(1)
        
    print(f"Loading civet detector weights: {weights_path}")
    model = YOLO(str(weights_path))
    
    print(f"Running inference on: {args.source} (conf={args.conf}, iou={args.iou})")
    results = model.predict(
        source=args.source,
        conf=args.conf,
        iou=args.iou,
        imgsz=640,
        save=args.save,
        verbose=True
    )
    
    total_detections = 0
    for idx, r in enumerate(results):
        num_boxes = len(r.boxes)
        total_detections += num_boxes
        if num_boxes > 0:
            for b in r.boxes:
                coords = [round(x, 1) for x in b.xyxy[0].tolist()]
                conf = float(b.conf[0])
                print(f"  [{Path(r.path).name}] Civet at {coords} (confidence: {conf:.2f})")
                
    print("\n" + "=" * 50)
    print(f"Inference complete: {len(results)} items processed, {total_detections} civet detections found.")
    if args.save:
        print("Annotated outputs saved to: runs/detect/predict/")
    print("=" * 50)

if __name__ == "__main__":
    main()
