# Quickstart - Flows API

**Quick Links:**
- [GENERIO Homepage](https://generio.ai/)
- [Complete API Documentation](https://flows.generio.ai/docs)

## Table of Contents

1. [TL;DR - Quick Start](#tldr---quick-start)
2. [Overview](#overview)
3. [Understanding the Workflow System](#understanding-the-workflow-system)
4. [Prerequisites](#prerequisites)
5. [Step 1: Obtain Your API Key](#step-1-obtain-your-api-key)
6. [Step 2: Understanding Available Templates](#step-2-understanding-available-templates)
7. [Step 3: Quick Start Examples](#step-3-quick-start-examples)
   - [Example 1: Generate from Text Prompt](#example-1-generate-3d-model-from-text-prompt)
   - [Example 2: Generate from Image](#example-2-generate-3d-model-from-image)
   - [Example 3: Optimize a 3D Model](#example-3-optimize-a-3d-model)
8. [Downloading Your Generated Assets](#downloading-your-generated-assets)

---

## TL;DR - Quick Start

**Want to generate 3D models in 5 minutes?** Jump straight to our [Quick Start Examples](#step-4-quick-start-examples) or check out our [example repository on GitHub](https://github.com/generio-ai/api-examples) with ready-to-use code.

### Prerequisites
- **API Key:** Get one at [account.generio.ai](https://account.generio.ai) → API Keys tab

### Minimal Example - Generate from Text Prompt

**Python Code:**
```python
import requests
import time

# Get your API key at: https://account.generio.ai → API Keys tab
API_KEY = "your-api-key-here"
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
```

**Need an API key?** Get one at [account.generio.ai](https://account.generio.ai) → API Keys tab

**Need help?** Contact us at [info@generio.ai](mailto:info@generio.ai) or join our [Discord server](https://discord.com/invite/8hwcxmgkv3)

---

## Overview

The GENERIO Flows API enables you to automatically generate and optimize 3D models through simple API calls. The API uses a template-based system where each template defines a specific workflow (e.g., generating models from text prompts or images).

## Understanding the Workflow System

The GENERIO API is built around a **workflow system** that automates complex 3D modeling tasks through simple API calls. Here's how it works:

### What is a Workflow?

A workflow (or "flow") is an automated process that takes inputs, processes them according to specific parameters, and produces outputs. Think of it as a recipe: you provide ingredients (inputs), specify how you want them prepared (parameters), and receive the finished dish (outputs).

### Templates: The Blueprints

Templates are pre-defined blueprints for different types of workflows. Each template specifies:

- **What it does** (description)
- **What it needs** (input types)
- **How to configure it** (parameters)
- **What it produces** (output types)

The API currently offers three templates:

| Template | Purpose | Input | Output |
|----------|---------|-------|--------|
| `model_generate_fromprompt` | Generate 3D models from text | Text prompts | 3D model (glTF) |
| `model_generate_fromimage` | Generate 3D models from images | Images (PNG, JPG, TIFF, WEBP) | 3D model (glTF) |
| `model_optimize` | Optimize/reduce polygon count | 3D model (glTF) | Optimized 3D model (glTF) |

### The Workflow Lifecycle

Every workflow follows this lifecycle:

1. **Created** - Flow is initialized with a template and parameters
2. **Starting** - Flow is preparing to process inputs (brief transition state)
3. **Running** - Flow is actively processing your inputs
4. **Completed** - Flow finished successfully, outputs are ready
5. **Aborted** - Flow was manually stopped
6. **Failed** - Flow encountered an error

### How to Create and Start a Flow

Include inputs when creating the flow - it will start automatically:
```python
payload = {
    "template": "model_generate_fromprompt",
    "parameters": {"quality": "high"},
    "inputs": [{"data": "A modern chair"}]
}
response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
# Flow is now running
```

### Chaining Workflows

You can chain workflows together to create complex pipelines. For example:
1. Generate a 3D model from an image (`model_generate_fromimage`)
2. Optimize the generated model (`model_optimize`)

```python
# Step 1: Generate model
generate_response = requests.post(f"{BASE_URL}/flows", headers=headers, json={
    "template": "model_generate_fromimage",
    "inputs": [{"data": image_base64}]
})
generate_flow_id = generate_response.json()["flow_id"]

# Wait for completion, then download the model
# ...

# Step 2: Optimize the generated model
optimize_response = requests.post(f"{BASE_URL}/flows", headers=headers, json={
    "template": "model_optimize",
    "parameters": {"polygon_count": 50000},
    "inputs": [{"data": generated_model_base64}]
})
```

## Prerequisites

- A GENERIO account (if you don't have one, [sign up for free](https://auth.generio.ai/signup))
- Python 3.7+ (for the examples shown)
- `requests` library (`pip install requests`)

## Step 1: Obtain Your API Key

To use the GENERIO API, you'll need an API key:

1. Log in to your account at [https://account.generio.ai](https://account.generio.ai)
2. Navigate to the **API Keys** tab in your account settings
3. Click **Add Key**
4. Set a name for your key and choose an expiration date
5. Click **Add Key** to generate the key
6. **Important:** Copy the API key immediately - you won't be able to see the full key again!

## Step 2: Understanding Available Templates

The API currently offers three templates for different use cases:

### 1. Generate from Text Prompt (`model_generate_fromprompt`)

Generate 3D models from text descriptions.

**Parameters:**
- `quality` (string, default: `"high"`)
  - Generation quality level
  - Values: `"low"` or `"high"`
- `seed` (integer, default: `-1`)
  - Seed for reproducible generation
  - Use `-1` for random seed
- `texture` (boolean, default: `true`)
  - Generate PBR (Physically Based Rendering) texture

**Input Types:** 
- `"prompt"` - Plain text description
- `"text/plain"`

**Output Type:** 
- `"model/gltf-binary"` - 3D model in glTF format

**Example Use Case:** "A modern office chair with armrests"

---

### 2. Generate from Image (`model_generate_fromimage`)

Generate 3D models from images.

**Parameters:**
- `quality` (string, default: `"high"`)
  - Generation quality level
  - Values: `"low"` or `"high"`
- `seed` (integer, default: `-1`)
  - Seed for reproducible generation
  - Use `-1` for random seed
- `texture` (boolean, default: `true`)
  - Generate PBR texture

**Input Types:**
- `"image/png"`
- `"image/jpg"`
- `"image/tiff"`
- `"image/webp"`

**Output Type:**
- `"model/gltf-binary"` - 3D model in glTF format

**Example Use Case:** Upload a photo of a product to generate a 3D model

---

### 3. Optimize Model (`model_optimize`)

Reduce polygon count and optimize existing 3D models.

**Parameters:**
- `polygon_count` (integer, default: `100000`)
  - Target number of polygons in optimized model

**Input Type:**
- `"model/gltf-binary"` - Existing 3D model

**Output Type:**
- `"model/gltf-binary"` - Optimized 3D model

**Example Use Case:** Reduce a high-poly model from 500k to 100k polygons for web use

## Step 3: Quick Start Examples

### Example 1: Generate 3D Model from Text Prompt

**JSON Request:**
```json
{
  "template": "model_generate_fromprompt",
  "parameters": {
    "quality": "high",
    "seed": -1,
    "texture": true
  },
  "inputs": [
    {
      "data": "A modern wooden chair with armrests",
      "additional": null
    }
  ],
  "additional": null
}
```

**Python Code:**
```python
import requests
import time
# Get your API key at: https://account.generio.ai → API Keys tab

API_KEY = "your-api-key-here"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Create and start a flow with text prompt
payload = {
    "template": "model_generate_fromprompt",
    "parameters": {
        "quality": "high",
        "seed": -1,
        "texture": True
    },
    "inputs": [
        {
            "data": "A modern wooden chair with armrests",
            "additional": None
        }
    ],
    "additional": None
}

# Create and automatically start the flow
response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_data = response.json()
flow_id = flow_data["flow_id"]
print(f"Flow created with ID: {flow_id}")
print(f"Flow state: {flow_data['state']}")

# Monitor flow progress
while True:
    status_response = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers)
    status = status_response.json()
    
    print(f"Progress: {status['progress']*100:.1f}% - State: {status['state']}")
    
    if status['state'] in ['completed', 'failed', 'aborted']:
        break
    
    time.sleep(5)  # Check every 5 seconds

# Download the generated model
if status['state'] == 'completed':
    outputs_response = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers)
    outputs = outputs_response.json()["outputs"]
    
    for output in outputs:
        asset_id = output["id"]
        asset_response = requests.get(
            f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", 
            headers=headers
        )
        
        # Save the 3D model
        with open(f"generated_model_{asset_id}.glb", "wb") as f:
            f.write(asset_response.content)
        
        print(f"Model saved as generated_model_{asset_id}.glb")
```

---

### Example 2: Generate 3D Model from Image

**Python Code:**
```python
import requests
import base64
import time
# Get your API key at: https://account.generio.ai → API Keys tab

API_KEY = "your-api-key-here"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Read and encode image
with open("product_image.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode('utf-8')
    image_base64 = f"data:image/jpeg;base64,{image_data}"

# Create and start flow with image
payload = {
    "template": "model_generate_fromimage",
    "parameters": {
        "quality": "high",
        "seed": -1,
        "texture": True
    },
    "inputs": [
        {
            "data": image_base64,
            "additional": None
        }
    ],
    "additional": None
}

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_data = response.json()
flow_id = flow_data["flow_id"]
print(f"Flow created with ID: {flow_id}")

# Monitor progress (same as Example 1)
while True:
    status_response = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers)
    status = status_response.json()
    
    print(f"Progress: {status['progress']*100:.1f}% - State: {status['state']}")
    
    if status['state'] in ['completed', 'failed', 'aborted']:
        break
    
    time.sleep(5)

# Download outputs (same as Example 1)
if status['state'] == 'completed':
    outputs_response = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers)
    outputs = outputs_response.json()["outputs"]
    
    for output in outputs:
        asset_id = output["id"]
        asset_response = requests.get(
            f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", 
            headers=headers
        )
        
        with open(f"generated_model_{asset_id}.glb", "wb") as f:
            f.write(asset_response.content)
        
        print(f"Model saved as generated_model_{asset_id}.glb")
```

---

### Example 3: Optimize a 3D Model

**JSON Request:**
```json
{
  "template": "model_optimize",
  "parameters": {
    "polygon_count": 50000
  },
  "inputs": [
    {
      "data": "data:model/gltf-binary;base64,<your-base64-encoded-glb-model>",
      "additional": null
    }
  ],
  "additional": null
}
```

**Python Code:**
```python
import requests
import base64
import time
# Get your API key at: https://account.generio.ai → API Keys tab

API_KEY = "your-api-key-here"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Read and encode the 3D model file
with open("high_poly_model.glb", "rb") as model_file:
    model_data = base64.b64encode(model_file.read()).decode('utf-8')
    model_base64 = f"data:model/gltf-binary;base64,{model_data}"

# Create and start optimization flow
payload = {
    "template": "model_optimize",
    "parameters": {
        "polygon_count": 50000  # Reduce to 50k polygons
    },
    "inputs": [
        {
            "data": model_base64,
            "additional": None
        }
    ],
    "additional": None
}

response = requests.post(f"{BASE_URL}/flows", headers=headers, json=payload)
flow_data = response.json()
flow_id = flow_data["flow_id"]
print(f"Flow created with ID: {flow_id}")

# Monitor progress
while True:
    status_response = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers)
    status = status_response.json()
    
    print(f"Progress: {status['progress']*100:.1f}% - State: {status['state']}")
    
    if status['state'] in ['completed', 'failed', 'aborted']:
        break
    
    time.sleep(5)

# Download the optimized model
if status['state'] == 'completed':
    outputs_response = requests.get(f"{BASE_URL}/flows/{flow_id}/outputs", headers=headers)
    outputs = outputs_response.json()["outputs"]
    
    for output in outputs:
        asset_id = output["id"]
        asset_response = requests.get(
            f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}", 
            headers=headers
        )
        
        with open(f"optimized_model_{asset_id}.glb", "wb") as f:
            f.write(asset_response.content)
        
        print(f"Optimized model saved as optimized_model_{asset_id}.glb")
```

---

## Understanding the Workflow

The GENERIO API follows a simple workflow:

1. **Create a Flow** - Initialize a new workflow using a template
2. **Upload Inputs** - Provide input data (text prompts or images)
3. **Start the Flow** - Begin processing
4. **Monitor Progress** - Check the status of your flow
5. **Download Outputs** - Retrieve your generated 3D models

## Downloading Your Generated Assets

Once a flow is completed, you can download the generated 3D models (or other output assets). This is a two-step process:

### Step 1: List Available Outputs

First, get a list of all output assets for your completed flow:

**Endpoint:** `GET /flows/{flow_id}/outputs`

**Python Example:**
```python
import requests
# Get your API key at: https://account.generio.ai → API Keys tab

API_KEY = "your-api-key-here"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

flow_id = "your-flow-id-here"

# Get list of outputs
outputs_response = requests.get(
    f"{BASE_URL}/flows/{flow_id}/outputs",
    headers=headers
)
outputs = outputs_response.json()["outputs"]

print(f"Found {len(outputs)} output file(s):")
for output in outputs:
    print(f"  - Asset ID: {output['id']}")
    print(f"    Status: {output['status']}")
```

**Response Example:**
```json
{
  "flow_id": "abc123...",
  "outputs": [
    {
      "id": "asset_xyz789",
      "status": "ready",
      "processed": "2024-01-15T10:30:00Z",
      "additional": null
    }
  ]
}
```

### Step 2: Download Individual Assets

Use the asset ID from Step 1 to download each output file:

**Endpoint:** `GET /flows/{flow_id}/outputs/{asset_id}`

**Python Example:**
```python
# Download each output asset
for output in outputs:
    asset_id = output["id"]
    
    # Download the asset
    asset_response = requests.get(
        f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}",
        headers=headers
    )
    
    # Save to file
    filename = f"generated_model_{asset_id}.glb"
    with open(filename, "wb") as f:
        f.write(asset_response.content)
    
    print(f"✓ Downloaded: {filename}")
```

### Complete Download Example

Here's a complete example that waits for a flow to complete and then downloads all outputs:

```python
import requests
import time
# Get your API key at: https://account.generio.ai → API Keys tab

API_KEY = "your-api-key-here"
BASE_URL = "https://test-flows.generio.ai"
headers = {"Authorization": f"Bearer {API_KEY}"}

flow_id = "your-flow-id-here"

# Wait for flow to complete
print("Waiting for flow to complete...")
while True:
    status_response = requests.get(f"{BASE_URL}/flows/{flow_id}", headers=headers)
    status = status_response.json()
    
    state = status['state']
    progress = status['progress']
    
    print(f"Progress: {progress*100:.1f}% - State: {state}")
    
    if state in ['completed', 'failed', 'aborted']:
        break
    
    time.sleep(5)

# Download outputs if completed successfully
if state == 'completed':
    print("\nDownloading outputs...")
    
    # Step 1: Get list of outputs
    outputs_response = requests.get(
        f"{BASE_URL}/flows/{flow_id}/outputs",
        headers=headers
    )
    outputs = outputs_response.json()["outputs"]
    
    # Step 2: Download each output
    for i, output in enumerate(outputs, 1):
        asset_id = output["id"]
        
        asset_response = requests.get(
            f"{BASE_URL}/flows/{flow_id}/outputs/{asset_id}",
            headers=headers
        )
        
        filename = f"model_{i}_{asset_id}.glb"
        with open(filename, "wb") as f:
            f.write(asset_response.content)
        
        print(f"✓ Downloaded: {filename}")
    
    print(f"\nSuccessfully downloaded {len(outputs)} file(s)!")
else:
    print(f"\nFlow did not complete successfully. State: {state}")
```

### Important Notes

- **Timing:** You can only download outputs after the flow reaches a final state (`completed`, `failed`, or `aborted`)
- **File Format:** Generated 3D models are in glTF binary format (`.glb` files)
- **Multiple Outputs:** Some workflows may generate multiple output files (e.g., when processing multiple input images)
- **Storage:** Output files remain available after download, so you can re-download them if needed

---

## Support

Need help or have questions? We're here to support you!

- **Email:** [info@generio.ai](mailto:info@generio.ai)
- **Discord:** Join our community at [https://discord.com/invite/8hwcxmgkv3](https://discord.com/invite/8hwcxmgkv3)

We appreciate your feedback! If you encounter any errors, bugs, or inconsistencies, please reach out to us :)