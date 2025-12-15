# Quickstart - Flows API Documentation

## Table of Contents

1. [TL;DR – Quick Start](#tldr--quick-start)
2. [Overview](#overview)
3. [Understanding the Workflow System](#understanding-the-workflow-system)
4. [Prerequisites](#prerequisites)
5. [Step 1: Obtain Your API Key](#step-1-obtain-your-api-key)
6. [Step 2: Available Templates](#step-2-available-templates)
7. [Step 3: Quick Start Examples](#step-3-quick-start-examples)

   * [Example 1: Generate from Text Prompt](#example-1-generate-3d-model-from-text-prompt)
   * [Example 2: Generate from Image](#example-2-generate-3d-model-from-image)
   * [Example 3: Optimize a 3D Model](#example-3-optimize-a-3d-model)
8. [Downloading Generated Assets](#downloading-generated-assets)
9. [Support](#support)

---

## TL;DR – Quick Start

Generate a 3D model from a text prompt in just a few minutes.

* **API Key:** [https://account.generio.ai](https://account.generio.ai) → *API Keys*
* **Base URL:** `https://flows.generio.ai`

### Minimal Python Example (Text → 3D)

```python
import requests
import time

# Get your API key at: https://account.generio.ai → API Keys tab
API_KEY = "your-api-key-here"
BASE_URL = "https://flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# 1. Create and start a flow
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

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_id = response.json()["flow_id"]
print(f"Flow created: {flow_id}")

# 2. Wait for completion
while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    print(f"Progress: {status['progress']*100:.0f}% – State: {status['state']}")

    if status["state"] in ["completed", "failed", "aborted"]:
        break

    time.sleep(5)

# 3. Download the 3D model
if status["state"] == "completed":
    outputs = requests.get(
        f"{BASE_URL}/flows/{flow_id}/outputs",
        headers=headers
    ).json()["outputs"]

    for output in outputs:
        model_data = requests.get(
            f"{BASE_URL}/flows/{flow_id}/outputs/{output['id']}",
            headers=headers
        )

        with open(f"model_{output['id']}.glb", "wb") as f:
            f.write(model_data.content)

        print(f"✓ Model saved: model_{output['id']}.glb")
```

---

## Overview

The GENERIO Flows API allows you to **generate, process, and optimize 3D models** through a template-based workflow system.

Each API call creates a **flow** that:

* receives inputs (text, images, or 3D models),
* executes an AI workflow,
* produces downloadable output assets (usually `.glb` files).

---

## Understanding the Workflow System

### What Is a Flow?

A **flow** is a single execution of a workflow template.

**Lifecycle:**

1. `created`
2. `starting`
3. `running`
4. `completed` / `failed` / `aborted`

### Templates

Templates define what a flow does.

| Template                    | Purpose       | Input | Output |
| --------------------------- | ------------- | ----- | ------ |
| `model_generate_fromprompt` | Text → 3D     | Text  | GLB    |
| `model_generate_fromimage`  | Image → 3D    | Image | GLB    |
| `model_optimize`            | Optimize mesh | GLB   | GLB    |

### Chaining Workflows

You can chain workflows manually:

1. Generate a model
2. Download the output
3. Use it as input for optimization or further processing

---

## Prerequisites

* GENERIO account (register at [https://generio.ai](https://generio.ai))

---

## Step 1: Obtain Your API Key

1. Go to [https://account.generio.ai](https://account.generio.ai)
2. Open **API Keys**
3. Create a new key
4. Copy it (shown only once)

---

## Step 2: Available Templates

### `model_generate_fromprompt`

Generate 3D models from text descriptions.

**Parameters**

* `quality`: `"low"` | `"high"` (default: `"high"`)
* `seed`: integer (default: `-1`)
* `texture`: boolean (default: `true`)

**Input**

* Plain text (`text/plain`)

**Output**

* `model/gltf-binary` (`.glb`)

---

### `model_generate_fromimage`

Generate 3D models from images.

**Input Types**

* `image/png`
* `image/jpeg`
* `image/webp`
* `image/tiff`

**Parameters**

* Same as text generation

---

### `model_optimize`

Reduce polygon count and optimize geometry.

**Parameters**

* `polygon_count` (default: `100000`)

**Input**

* `model/gltf-binary` (`.glb`)

---

## Step 3: Quick Start Examples

---

## Example 1: Generate 3D Model from Text Prompt

```python
import requests
import time

API_KEY = "your-api-key-here"
BASE_URL = "https://flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

payload = {
    "template": "model_generate_fromprompt",
    "parameters": {
        "quality": "high",
        "seed": -1,
        "texture": True
    },
    "inputs": [
        {"data": "A modern wooden chair with armrests", "additional": None}
    ],
    "additional": None
}

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_id = response.json()["flow_id"]
print(f"Flow created: {flow_id}")

while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    print(f"Progress: {status['progress']*100:.0f}% – State: {status['state']}")
    if status["state"] in ["completed", "failed", "aborted"]:
        break
    time.sleep(5)

if status["state"] == "completed":
    outputs = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers).json()["outputs"]
    for output in outputs:
        asset_id = output["id"]
        model_data = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", headers=headers)
        with open(f"generated_model_{asset_id}.glb", "wb") as f:
            f.write(model_data.content)
        print(f"✓ Model saved: generated_model_{asset_id}.glb")
```

---

## Example 2: Generate 3D Model from Image

```python
import requests
import base64
import time

API_KEY = "your-api-key-here"
BASE_URL = "https://flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

with open("product_image.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

payload = {
    "template": "model_generate_fromimage",
    "parameters": {
        "quality": "high",
        "seed": -1,
        "texture": True
    },
    "inputs": [
        {"data": f"data:image/jpeg;base64,{image_b64}", "additional": None}
    ],
    "additional": None
}

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_id = response.json()["flow_id"]
print(f"Flow created: {flow_id}")

while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    print(f"Progress: {status['progress']*100:.1f}% – State: {status['state']}")
    if status["state"] in ["completed", "failed", "aborted"]:
        break
    time.sleep(5)

if status["state"] == "completed":
    outputs = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers).json()["outputs"]
    for output in outputs:
        asset_id = output["id"]
        model_data = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", headers=headers)
        with open(f"generated_model_{asset_id}.glb", "wb") as f:
            f.write(model_data.content)
        print(f"✓ Model saved: generated_model_{asset_id}.glb")
```

---

## Example 3: Optimize a 3D Model

```python
import requests
import base64
import time

API_KEY = "your-api-key-here"
BASE_URL = "https://flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

with open("high_poly_model.glb", "rb") as f:
    glb_b64 = base64.b64encode(f.read()).decode()

payload = {
    "template": "model_optimize",
    "parameters": {
        "polygon_count": 50000
    },
    "inputs": [
        {"data": f"data:model/gltf-binary;base64,{glb_b64}", "additional": None}
    ],
    "additional": None
}

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_id = response.json()["flow_id"]
print(f"Flow created: {flow_id}")

while True:
    status = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers).json()
    print(f"Progress: {status['progress']*100:.1f}% – State: {status['state']}")
    if status["state"] in ["completed", "failed", "aborted"]:
        break
    time.sleep(5)

if status["state"] == "completed":
    outputs = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers).json()["outputs"]
    for output in outputs:
        asset_id = output["id"]
        model_data = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", headers=headers)
        with open(f"optimized_model_{asset_id}.glb", "wb") as f:
            f.write(model_data.content)
        print(f"✓ Model saved: optimized_model_{asset_id}.glb")
```

---

## Downloading Generated Assets

Once a flow is completed, you can download outputs in two steps.

### Step 1: List Outputs

```python
outputs = requests.get(
    f"{BASE_URL}/flows/{flow_id}/outputs",
    headers=headers
).json()["outputs"]
```

### Step 2: Download Assets

```python
for output in outputs:
    asset_id = output["id"]

    response = requests.get(
        f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}",
        headers=headers
    )

    with open(f"model_{asset_id}.glb", "wb") as f:
        f.write(response.content)

    print(f"✓ Downloaded model_{asset_id}.glb")
```

---

## Support

If you encounter any problems or errors, or would like to provide feedback, please feel free to contact us at any time :)

* **Email:** [info@generio.ai](mailto:info@generio.ai)
* **Discord:** [https://discord.com/invite/8hwcxmgkv3](https://discord.com/invite/8hwcxmgkv3)
* **Examples:** [https://github.com/GenerIO-ai/api-flows-quickstart](https://github.com/GenerIO-ai/api-flows-quickstart)
