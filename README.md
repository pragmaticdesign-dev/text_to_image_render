# Render Engine Microservice

A high-performance, asynchronous microservice designed to convert code (HTML, CSS, JS) into pixel-perfect images and text into natural-sounding speech.

Built with **FastAPI**, **Playwright**, and **Kokoro**, this engine serves as a reliable "Media Generation API" for applications that need to generate accurate technical visuals (like DSA Cheat Sheets, Infographics) or high-quality AI narration.

## ❓ The "Why"
**Problem:** Generative AI models (DALL-E, Midjourney) are incredible at art but terrible at logic. If you ask them to "Draw a Binary Search Tree" or "Write text on a blackboard," they often hallucinate structures or misspell words. Similarly, many TTS engines sound robotic or require expensive cloud subscriptions.

**Solution:** The **Render Engine**.
Instead of asking AI to *draw* the pixels, we ask AI to *write the code* (HTML/Mermaid), and we use this engine to render that code exactly as intended.
* **Zero Hallucinations:** HTML/CSS renders exactly what is written.
* **Perfect Text:** No more gibberish characters.
* **Infinite Styling:** Leverage the full power of CSS/Tailwind.
* **Local Neural TTS:** High-quality, offline text-to-speech using Kokoro (82M).

## 🏗️ Architecture & Design
This project is built using **Clean Architecture** (Hexagonal / Ports & Adapters) and strictly follows **SOLID Principles**.

### Key Design Patterns
* **Ports & Adapters:** The core business logic (generating media) is decoupled from the specific tool doing the work (Playwright/Kokoro).
* **Factory Pattern:** An `EngineFactory` dynamically selects the correct rendering engine based on the request type (`html`, `mermaid`, `kokorro`, etc.).
* **Dependency Injection:** Services and Engines are injected at runtime, making the system highly testable and modular.

### Project Structure
```text
src/app/
├── api/            # 🔌 The "Primary Adapter" (FastAPI Endpoints)
├── core/           # ⚙️ Config & Dependency Injection Container
├── domain/         # 📦 Pure Data Models (Pydantic)
├── ports/          # 🚪 Interfaces (Contracts for Renderers)
├── services/       # 🧠 Business Logic (Orchestrator)
├── factories/      # 🏭 Factory to pick the right Engine
└── engines/        # 🔧 The "Secondary Adapters" (Playwright & TTS Implementations)

```

## 🚀 Getting Started

### Prerequisites

* Python 3.12+
* [uv](https://github.com/astral-sh/uv) (Modern Python package manager)
* FFmpeg (Required for audio processing)

### Installation

1. **Clone the repository**

```bash
git clone [https://github.com/your-repo/render-engine.git](https://github.com/your-repo/render-engine.git)
cd render-engine

```

2. **Install dependencies**

```bash
uv sync

```

3. **Install Browsers** (Required for Playwright)

```bash
uv run playwright install chromium

```

### Running the Server

```bash
uv run uvicorn src.app.main:app --reload

```

The API will be available at `http://localhost:8000`.
Interactive documentation is at `http://localhost:8000/docs`.

## 🔌 API Usage

### Endpoint: `POST /api/v1/generate`

#### 1. Generate Visuals (HTML/CSS)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/generate' \
  -H 'Content-Type: application/json' \
  -d '{
  "engine_type": "html",
  "source_code": "<div class=\"bg-slate-900 text-cyan-400 p-10 font-bold text-6xl\">Binary Search</div>",
  "options": {
    "width": 1080,
    "height": 1920,
    "scale_factor": 2
  }
}'

```

#### 2. Generate Audio (TTS)

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/generate' \
  -H 'Content-Type: application/json' \
  -d '{
  "engine_type": "kokorro",
  "source_code": "Hello! This is a test of the local text to speech engine.",
  "options": {
    "voice": "af_heart",
    "speed": 1.0
  }
}'

```

### Payload Fields

* `engine_type`: The engine to use. Options: `"html"`, `"mermaid"`, `"kokorro"`.
* `source_code`: The raw string content (HTML code or text to speak).
* `options`:
* **Visual Options:**
* `width`: Viewport width (default: 1024)
* `height`: Viewport height (default: 768)
* `scale_factor`: Pixel density (default: 1.0)


* **Audio Options:**
* `voice`: Kokoro voice ID (default: "af_heart")
* `speed`: Playback speed (default: 1.0)





## 🛠️ Extending the Engine

Want to add support for **Mermaid.js** diagrams?

1. Create a new engine in `src/app/engines/mermaid_engine.py` implementing `BaseRenderingEngine`.
2. Register it in `src/app/factories/engine_factory.py`:

```python
engine_factory.register_engine(EngineType.MERMAID, mermaid_engine)

```

