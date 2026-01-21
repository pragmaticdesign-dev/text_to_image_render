from playwright.async_api import async_playwright
from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import RenderOptions

class MermaidPlaywrightEngine(BaseRenderingEngine):
    """
    Renders Mermaid graphs by injecting the Mermaid.js library 
    into a headless browser page.
    """
    MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"

    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page(
                    viewport={"width": options.width, "height": options.height},
                    device_scale_factor=options.scale_factor
                )

                # We create a simple HTML wrapper that loads mermaid
                # and renders the graph in a centered container.
                html_template = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body {{ margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background: #fff; }}
                    </style>
                </head>
                <body>
                    <div class="mermaid">
                        {source_code}
                    </div>
                    <script type="module">
                        import mermaid from '{self.MERMAID_CDN}';
                        mermaid.initialize({{ startOnLoad: true }});
                    </script>
                </body>
                </html>
                """

                await page.set_content(html_template, wait_until="networkidle")
                
                # Locate the rendered SVG to take a tighter screenshot (optional)
                # or just screenshot the viewport
                element = await page.locator(".mermaid")
                return await element.screenshot(type="png")

            finally:
                await browser.close()