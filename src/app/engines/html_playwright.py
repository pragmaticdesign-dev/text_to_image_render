from playwright.async_api import async_playwright

from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import RenderOptions


class HtmlPlaywrightEngine(BaseRenderingEngine):
    """
    Concrete implementation of a rendering engine using Playwright.
    """

    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            try:
                page = await browser.new_page(
                    viewport={"width": options.width, "height": options.height},
                    device_scale_factor=options.scale_factor,
                )

                # LOGIC BRANCH:
                # 1. Transparent + Tight Crop -> Wrap in inline-block to shrink-wrap.
                # 2. Transparent + Full Size  -> Use standard full-width body.
                # 3. Background Mode          -> Use standard full-width body.
                
                if options.omit_background and options.tight_crop:
                    # TIGHT CROP MODE (Transparent)
                    html_content = f"""
                    <div id="snapshot-target" style="display: inline-block; max-width: 100%;">
                        {source_code}
                    </div>
                    """
                else:
                    # CANVAS MODE (With Background OR Transparent Full Page)
                    html_content = source_code

                full_html = f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <script src="https://cdn.tailwindcss.com"></script>
                    <style>
                        body {{ margin: 0; padding: 0; }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """

                await page.set_content(full_html, wait_until="networkidle")

                if options.omit_background:
                    if options.tight_crop:
                        # 1. Transparent Crop: Screenshot ONLY the element
                        element = page.locator("#snapshot-target")
                        return await element.screenshot(type="png", omit_background=True)
                    else:
                        # 2. Transparent Full: Screenshot FULL PAGE with transparency
                        return await page.screenshot(type="png", omit_background=True)
                else:
                    # 3. Background: Screenshot FULL PAGE (fixed size)
                    return await page.screenshot(type="png")

            finally:
                await browser.close()