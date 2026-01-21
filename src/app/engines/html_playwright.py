from playwright.async_api import async_playwright

from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import RenderOptions


class HtmlPlaywrightEngine(BaseRenderingEngine):
    """
    Concrete implementation of a rendering engine using Playwright.
    
    AUTOMATICALLY INJECTS:
    - Tailwind CSS (via CDN)
    - Basic CSS Reset
    """

    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        async with async_playwright() as p:
            # Launch the browser
            browser = await p.chromium.launch(headless=True)
            try:
                # Configure the viewport
                page = await browser.new_page(
                    viewport={"width": options.width, "height": options.height},
                    device_scale_factor=options.scale_factor,
                )

                # --- THE FIX IS HERE ---
                # We wrap the user's source_code in a standard HTML shell 
                # that pre-loads Tailwind CSS.
                full_html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    
                    <script src="https://cdn.tailwindcss.com"></script>
                    
                    <style>
                        body {{ margin: 0; padding: 0; box-sizing: border-box; }}
                        /* You can add more global styles here if you want */
                    </style>
                </head>
                <body>
                    {source_code}
                </body>
                </html>
                """

                # Load the page and wait for the network to be idle 
                # (This ensures Tailwind has finished downloading)
                await page.set_content(full_html, wait_until="networkidle")

                # Take the screenshot
                screenshot_bytes = await page.screenshot(type="png")
                return screenshot_bytes

            finally:
                await browser.close()