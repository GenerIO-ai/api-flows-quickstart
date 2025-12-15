import requests
import time
import base64
from pathlib import Path

# Get your API key at: https://account.generio.ai → API Keys tab
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Path to your input image
IMAGE_PATH = Path("input/test_sneaker.png")

# 1) Create a flow (image → 3D)
payload = {
    "template": "model_generate_fromimage",
    "parameters": {
        "quality": "high",
        "texture": True
    },
    "inputs": None,          # inputs are uploaded via /inputs (like in your test script)
    "additional": None
}

resp = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
resp.raise_for_status()

flow_id = resp.json()["flow_id"]
print(f"Flow created: {flow_id}")

# 2) Upload the image as base64 data URL
img_bytes = IMAGE_PATH.read_bytes()
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

upload_payload = {
    # Use the right mime for your file. If it's actually PNG, keep image/png.
    "data": f"data:image/png;base64,{img_b64}",
    "additional": None
}

resp = requests.post(f"{BASE_URL}/flows/{flow_id}/inputs", headers=headers, json=upload_payload)
resp.raise_for_status()
print("✓ Image uploaded")

# 3) Start the flow
resp = requests.patch(f"{BASE_URL}/flows/{flow_id}", headers=headers, json={"action": "start"})
resp.raise_for_status()
print("✓ Flow started")

# 4) Poll status until done
while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    progress = status.get("progress", 0) * 100
    state = status.get("state")
    print(f"Progress: {progress:.0f}% - State: {state}")

    if state in ["completed", "failed", "aborted"]:
        break

    time.sleep(5)

# 5) Download outputs (GLB)
if status["state"] == "completed":
    outputs_resp = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers)
    outputs_resp.raise_for_status()
    outputs = outputs_resp.json().get("outputs", [])

    for output in outputs:
        out_id = output["id"]
        model_resp = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs/{out_id}", headers=headers)
        model_resp.raise_for_status()

        out_path = Path(f"model_{out_id}.glb")
        out_path.write_bytes(model_resp.content)
        print(f"✓ Model saved: {out_path}")
else:
    print(f"✗ Flow finished with state: {status['state']}")
    print("Details:", status)
