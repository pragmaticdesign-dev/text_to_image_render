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
""",
    "options": { "width": 1080, "height": 1920, "omit_background": False }
}

# 2. Image WITHOUT Background (Transparent)
payload_trans = {
    "engine_type": "html",
    "source_code": "<h1 class='text-6xl text-red-500 font-bold'>Transparent</h1>",
    "options": { "width": 500, "height": 300, "omit_background": True }
}

# 3. Voice Generation
payload_voice = {
    "engine_type": "kokorro",
    "source_code": "System check complete. Transparency enabled.",
    "options": { "voice": "af_heart", "speed": 1.0 }
}

if __name__ == "__main__":
    run_test("Image (With BG)", "test_bg.png", payload_bg)
    run_test("Image (Transparent)", "test_transparent.png", payload_trans)
    run_test("Voice", "test_voice.wav", payload_voice) # or .mp3