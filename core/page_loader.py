from playwright.async_api import async_playwright

class PageLoader:
    def __init__(self) -> None:
        pass


    async def scroll_page(self, page, timeout):
        await page.wait_for_timeout(5000)
        while True:
            old_height = await page.evaluate("document.body.scrollHeight")
            await page.evaluate(f"window.scrollTo(0, {old_height})")
            await page.wait_for_timeout(timeout)
            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == old_height:
                break