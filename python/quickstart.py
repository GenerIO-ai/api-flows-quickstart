import requests
import time

# Get your API key at: https://account.generio.ai → API Keys tab
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Define the JSON payload
payload = {
    "template": "model_generate_fromprompt",
    "parameters": {
        "quality": "high"
    },
    "inputs": [
        {
            "data": "A modern office chair",
            "additional": None
        }
    ],
    "additional": None
}

# Create and start flow using the payload
response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)

flow_id = response.json()["flow_id"]
print(f"Flow created: {flow_id}")

# Wait for completion
while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    print(f"Progress: {status['progress']*100:.0f}% - State: {status['state']}")

    if status['state'] in ['completed', 'failed', 'aborted']:
        break
    time.sleep(5)

# Download the 3D model
if status['state'] == 'completed':
    outputs = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers).json()["outputs"]

    for output in outputs:
        model_data = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs/{output['id']}", headers=headers)

        with open(f"model_{output['id']}.glb", "wb") as f:
            f.write(model_data.content)

        print(f"✓ Model saved: model_{output['id']}.glb")