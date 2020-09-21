from pyppeteer import launch


class WebScraper:
    async def get_html(self, url: str) -> str:
        browser = await launch(headless=True)
        page = await browser.newPage()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content