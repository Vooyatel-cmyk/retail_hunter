import os
import json
import asyncio
from playwright.async_api import async_playwright
from core.tab_resolver import TabResolver
from core.page_loader import PageLoader
from core.product_searcher import ProductSearcher
from core.cleaner import Cleaner
from core.writer import Writer

required_dirs = ['.logs', '.result']

for folder in required_dirs:
    os.makedirs(folder, exist_ok=True)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

cdp_url = config.get("network_settings", {}).get("cdp_url", "http://localhost:9222")
target_tab_keyword = config.get("parsing_targets", {}).get("target_tab_keyword")
timeout_delay = config.get("network_settings",{}).get("tiomeout_seconds", 1000)
category = config.get("parsing_targets", {}).get("categories")

async def main(tab_resolver, page_loader, product_searcher, cleaner, writer):

    async with async_playwright() as p:
        page = await tab_resolver.get_target_page(p)
        print("Успешно подключились к странице:", await page.title())
        await page_loader.scroll_page(page, timeout_delay)
        await page.wait_for_timeout(5000)
        cards = await page.locator('div[class*="min-h-[232px]"]').all()
        print(f"Робот нашел карточек на экране: {len(cards)}")
        raw_data = await product_searcher.collect_new_products(page)
        clprod = await cleaner.clean_products(raw_data)
        writer.new_book(clprod)


if __name__ == "__main__":
    asyncio.run(
        main(
            TabResolver(cdp_url, target_tab_keyword, category), 
            PageLoader(), 
            ProductSearcher(), 
            Cleaner(),
            Writer()
        )
    )