import base64
import os
import sys
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "Dbsq4wpnTVr9UkRb7YBj"
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=API_KEY
).configure(InferenceConfiguration(api_key_transport="header"))

test_images = [
    ("scratch/c2_m15.jpg", "Cam 02 - Daytime Shelf Resting"),
    ("scratch/civet_sand_nap_5395.jpg", "Cam 03 - Night IR Sand Nap")
]

for img_path, desc in test_images:
    if not os.path.exists(img_path):
        continue
    print(f"\n==========================================")
    print(f"Testing on: {desc} ({img_path})")
    print(f"==========================================")
    res = client.run_workflow(
        workspace_name="mes-workspace-02uvi",
        workflow_id="civet-detection-prototype-1793407785222",
        images={"image": img_path},
        use_cache=True
    )
    
    output_data = res[0]
    preds = output_data.get("predictions", {}).get("predictions", [])
    print(f"Total Detections: {len(preds)}")
    for i, p in enumerate(preds, 1):
        cls_name = p.get("class", "unknown")
        conf = p.get("confidence", 0)
        x = p.get("x", 0)
        y = p.get("y", 0)
        w = p.get("width", 0)
        h = p.get("height", 0)
        print(f"  [{i}] Class: '{cls_name}' | Conf: {conf:.2f} | BBox: [center=({x}, {y}), size=({w}x{h})]")
        
    if "output_image" in output_data and output_data["output_image"]:
        b64_str = output_data["output_image"]
        img_bytes = base64.b64decode(b64_str)
        fname = f"roboflow_out_{os.path.basename(img_path)}"
        out_save = os.path.join("scratch", fname)
        with open(out_save, "wb") as f:
            f.write(img_bytes)
        print(f"  [SAVED] Annotated visual output: {out_save} ({len(img_bytes)/1024:.1f} KB)")
