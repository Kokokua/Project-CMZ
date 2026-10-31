import os
import sys
from inference_sdk import InferenceHTTPClient, InferenceConfiguration

sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Roboflow Civet Detection Prototype
# Workspace: mes-workspace-02uvi
# Workflow ID: civet-detection-prototype-1793407785222
# ============================================================

# 1. Put your Roboflow API Key here (or set environment variable ROBOFLOW_API_KEY)
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY", "Dbsq4wpnTVr9UkRb7YBj")

if ROBOFLOW_API_KEY == "YOUR_ROBOFLOW_API_KEY":
    print("==================================================================")
    print("[NOTICE] Please replace 'YOUR_ROBOFLOW_API_KEY' with your actual key!")
    print("Get your key at: Roboflow -> Workspace Settings -> API Keys")
    print("==================================================================")
    sys.exit(1)

# 2. Path to test image (using our verified civet frame)
project_root = r"D:\CMU\4th\1 st\image processing\project cmz"
test_image = os.path.join(project_root, "scratch", "c2_m15.jpg")

if not os.path.exists(test_image):
    test_image = os.path.join(project_root, "scratch", "civet_sand_nap_5395.jpg")

print(f"Connecting to Roboflow workflow...")
print(f"Testing image: {test_image}")

# 3. Connect to workflow
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=ROBOFLOW_API_KEY
).configure(InferenceConfiguration(
    api_key_transport="header"
))

# 4. Run workflow on image
result = client.run_workflow(
    workspace_name="mes-workspace-02uvi",
    workflow_id="civet-detection-prototype-1793407785222",
    images={
        "image": test_image
    },
    use_cache=True
)

# 5. Output results
print("\n=== WORKFLOW DETECTION RESULT ===")
import json
print(json.dumps(result, indent=2))
print("=================================")
