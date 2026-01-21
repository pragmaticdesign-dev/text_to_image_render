from playwright.async_api import async_playwright

from src.app.core.interfaces.engine_contract import BaseRenderingEngine
from src.app.schemas.requests import RenderOptions


class HtmlPlaywrightEngine(BaseRenderingEngine):
    """
    Concrete implementation of a rendering engine using Playwright to convert
    HTML, CSS, and JavaScript into a raster image (PNG).

    This engine launches a headless browser, loads the provided HTML code,
    and takes a screenshot of the rendered result.
    """

    async def render(self, source_code: str, options: RenderOptions) -> bytes:
        """
        Renders the given HTML source code into a PNG image using Playwright.

        Args:
            source_code: A string containing the HTML, CSS, and/or
                         JavaScript to render.
            options: A RenderOptions object specifying dimensions and scale
                     factor.

        Returns:
            The raw bytes of the resulting PNG image.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page(
                    viewport={"width": options.width, "height": options.height},
                    device_scale_factor=options.scale_factor,
                )

                # Set the HTML content of the page
                await page.set_content(source_code, wait_until="networkidle")

                # Take the screenshot and return the bytes
                screenshot_bytes = await page.screenshot(type="png")
                return screenshot_bytes
            finally:
                await browser.close()
