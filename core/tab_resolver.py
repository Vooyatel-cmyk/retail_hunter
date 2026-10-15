class TabResolver:
    def __init__(self, cdp_url: str, keyword: str, category_url:str) -> None:
        self.cdp_url = cdp_url
        self.target_tab_keyword = keyword
        self.categiories = category_url

    async def get_target_page(self, playwright_instance):
        browser = await playwright_instance.chromium.connect_over_cdp(self.cdp_url)
        for page in browser.contexts[0].pages:
            if self.target_tab_keyword in page.url:
                return page
        page = await browser.contexts[0].new_page()
        await page.goto(self.categiories)
        return page