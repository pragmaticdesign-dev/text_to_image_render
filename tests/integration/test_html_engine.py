import requests
import json

API_URL = "http://localhost:8000/api/v1/generate"

def run_test(name, filename, payload):
    print(f"Testing {name}...")
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved to {filename}")
    except Exception as e:
        print(f"❌ Failed: {e}")

# 1. Image WITH Background
payload_bg = {
    "engine_type": "html",
    "source_code": """<div class="h-screen w-screen bg-slate-900 flex flex-col items-center justify-center font-sans text-white">
    <h1 class="text-6xl font-bold mb-20 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
        Python Array
    </h1>
    <div class="mt-20 p-8 bg-slate-800/50 rounded-xl border border-slate-700 max-w-2xl text-center">
        <p class="text-2xl text-slate-300">
            Elements are accessed by their <span class="text-cyan-400 font-bold">index</span>, starting at 0.
        </p>
    </div>
</div>
""",
    "options": { "width": 1080, "height": 1920, "omit_background": False }
}

# 2. Image WITHOUT Background (Transparent Tight Crop)
payload_trans_crop = {
    "engine_type": "html",
    "source_code": "<h1 class='text-6xl text-red-500 font-bold'>Transparent Crop</h1>",
    "options": { "width": 500, "height": 300, "omit_background": True, "tight_crop": True }
}

# 3. Image WITHOUT Background (Transparent Full Size)
payload_trans_full = {
    "engine_type": "html",
    "source_code": "<h1 class='text-6xl text-green-500 font-bold p-10'>Transparent Full Viewport</h1>",
    # This will be a 500x300 image, mostly transparent, with the text at the top-left
    "options": { "width": 500, "height": 300, "omit_background": True, "tight_crop": False }
}

# 4. Voice Generation
payload_voice = {
    "engine_type": "kokorro",
    "source_code": "System check complete. Transparency enabled.",
    "options": { "voice": "af_heart", "speed": 1.0 }
}

if __name__ == "__main__":
    run_test("Image (With BG)", "test_bg.png", payload_bg)
    run_test("Image (Transparent Crop)", "test_trans_crop.png", payload_trans_crop)
    run_test("Image (Transparent Full)", "test_trans_full.png", payload_trans_full)
    run_test("Voice", "test_voice.wav", payload_voice)