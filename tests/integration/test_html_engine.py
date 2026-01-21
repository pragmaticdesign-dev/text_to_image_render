import requests
import json
import base64

# Configuration
API_URL = "http://localhost:8000/api/v1/generate"
OUTPUT_FILE = "array_visual.png"

# 1. Define the Visual (The "Source Code")
# We use Tailwind CSS classes because your engine injects Tailwind.
html_payload = """
<div class="h-screen w-screen bg-slate-900 flex flex-col items-center justify-center font-sans text-white">
    
    <h1 class="text-6xl font-bold mb-20 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
        Python Array
    </h1>

    <div class="flex gap-6">
        
        <div class="flex flex-col items-center group">
            <div class="w-32 h-32 flex items-center justify-center bg-slate-800 border-4 border-cyan-400 rounded-2xl text-5xl font-mono shadow-lg shadow-cyan-500/20 z-10 relative">
                12
                <div class="absolute -right-8 w-6 h-1 bg-slate-700"></div>
            </div>
            <span class="mt-4 text-3xl text-slate-500 font-mono">0</span>
        </div>

        <div class="flex flex-col items-center">
            <div class="w-32 h-32 flex items-center justify-center bg-slate-800 border-4 border-purple-400 rounded-2xl text-5xl font-mono shadow-lg shadow-purple-500/20 z-10 relative">
                45
                <div class="absolute -right-8 w-6 h-1 bg-slate-700"></div>
            </div>
            <span class="mt-4 text-3xl text-slate-500 font-mono">1</span>
        </div>

        <div class="flex flex-col items-center">
            <div class="w-32 h-32 flex items-center justify-center bg-slate-800 border-4 border-pink-400 rounded-2xl text-5xl font-mono shadow-lg shadow-pink-500/20 z-10">
                99
            </div>
            <span class="mt-4 text-3xl text-slate-500 font-mono">2</span>
        </div>

    </div>

    <div class="mt-20 p-8 bg-slate-800/50 rounded-xl border border-slate-700 max-w-2xl text-center">
        <p class="text-2xl text-slate-300">
            Elements are accessed by their <span class="text-cyan-400 font-bold">index</span>, starting at 0.
        </p>
    </div>

</div>
"""

# 2. Construct the Request Data
payload = {
    "engine_type": "html",
    "source_code": html_payload,
    "options": {
        "width": 1080,
        "height": 1920,
        "device_scale_factor": 2  # Retina quality
    }
}

try:
    print(f"Sending request to {API_URL}...")
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        # 3. Save the Image
        with open(OUTPUT_FILE, "wb") as f:
            f.write(response.content)
        print(f"✅ Success! Image saved to: {OUTPUT_FILE}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except requests.exceptions.ConnectionError:
    print(f"❌ Could not connect to {API_URL}. Is the server running?")