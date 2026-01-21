

# Render Engine Microservice

A high-performance, asynchronous microservice designed to convert code (HTML, CSS, JS) into pixel-perfect images. 

Built with **FastAPI** and **Playwright**, this engine serves as a reliable "Screenshot API" for applications that need to generate accurate technical visuals (like DSA Cheat Sheets, Infographics, or Code Snippets) where standard Generative AI models often fail.

## ❓ The "Why"
**Problem:** Generative AI models (DALL-E, Midjourney) are incredible at art but terrible at logic. If you ask them to "Draw a Binary Search Tree" or "Write text on a blackboard," they often hallucinate structures or misspell words.

**Solution:** The **Render Engine**.
Instead of asking AI to *draw* the pixels, we ask AI to *write the code* (HTML/Mermaid), and we use this engine to render that code exactly as intended.
* **Zero Hallucinations:** HTML/CSS renders exactly what is written.
* **Perfect Text:** No more gibberish characters.
* **Infinite Styling:** Leverage the full power of CSS/Tailwind.

## 🏗️ Architecture & Design
This project is built using **Clean Architecture** (Hexagonal / Ports & Adapters) and strictly follows **SOLID Principles**.

### Key Design Patterns
* **Ports & Adapters:** The core business logic (generating an image) is decoupled from the specific tool doing the work (Playwright). This means we can swap Playwright for Selenium or a Cloud Renderer without touching the core logic.
* **Factory Pattern:** An `EngineFactory` dynamically selects the correct rendering engine based on the request type (`html`, `mermaid`, etc.).
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
└── engines/        # 🔧 The "Secondary Adapters" (Playwright Implementation)

```

## 🚀 Getting Started

### Prerequisites

* Python 3.12+
* [uv](https://github.com/astral-sh/uv) (Modern Python package manager)

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

**Generate a Visual from HTML/CSS:**

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
    "device_scale_factor": 2
  }
}'

```

**Payload Fields:**

* `engine_type`: `"html"` (Extensible for `"mermaid"`, `"react"`, etc.)
* `source_code`: The raw string content to render.
* `options`:
* `width`: Viewport width (default: 1080)
* `height`: Viewport height (default: 1920)
* `device_scale_factor`: Pixel density (2 for Retina/Crisp text)



## 🛠️ Extending the Engine

Want to add support for **Mermaid.js** diagrams?

1. Create a new engine in `src/app/engines/mermaid_engine.py` implementing `BaseRenderingEngine`.
2. Register it in `src/app/core/container.py`:
```python
engine_factory.register_engine(EngineType.MERMAID, mermaid_engine)

```


3. That's it! The API now supports Mermaid.

