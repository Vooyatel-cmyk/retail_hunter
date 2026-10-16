import os
import json
import asyncio
import pprint
from playwright.async_api import async_playwright
from core.tab_resolver import TabResolver
from core.page_loader import PageLoader
from core.product_searcher import ProductSearcher
from core.cleaner import Cleaner

required_dirs = ['.logs', '.result']

for folder in required_dirs:
    os.makedirs(folder, exist_ok=True)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

cdp_url = config["network_settings"]["cdp_url"]
target_tab_keyword = config["parsing_targets"]["target_tab_keyword"]
timeout_delay = config["network_settings"]["timeout_seconds"]
category = config["parsing_targets"]["categories"]

async def main(tab_resolver, page_loader, product_searcher, cleaner):

    async with async_playwright() as p:

        page = await tab_resolver.get_target_page(p)
        print("Успешно подключились к странице:", await page.title())

        await page_loader.scroll_page(page, timeout_delay)

        await page.wait_for_timeout(5000)

        cards = await page.locator('div[class*="min-h-[232px]"]').all()
        print(f"Робот нашел карточек на экране: {len(cards)}")

        raw_data = await product_searcher.collect_new_products(page)

        clprod = await cleaner.clean_raw_price(raw_data, 'raw_price')
        clprod = await cleaner.clean_raw_old_price(clprod, 'raw_old_price')
        clprod = await cleaner.process_sale_percent(clprod, 'raw_price', 'raw_old_price')
        
        pprint.pprint(clprod)


if __name__ == "__main__":
    asyncio.run(
        main(
            TabResolver(cdp_url, target_tab_keyword, category), 
            PageLoader(), 
            ProductSearcher(), 
            Cleaner()
        )
    )