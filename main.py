import os
import json
import asyncio
import logging
import sys
from datetime import datetime
from playwright.async_api import async_playwright, Error
from core.tab_resolver import TabResolver
from core.page_loader import PageLoader
from core.product_searcher import ProductSearcher
from core.cleaner import Cleaner
from core.writer import Writer
from core.storage import Storage

required_dirs = ['.logs', '.result']

for folder in required_dirs:
    os.makedirs(folder, exist_ok=True)

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

cdp_url = config.get("network_settings", {}).get("cdp_url", "http://localhost:9222")
target_tab_keyword = config.get("parsing_targets", {}).get("target_tab_keyword")
timeout_delay = config.get("network_settings", {}).get("timeout_seconds", 1000)
category = config.get("parsing_targets", {}).get("categories")
db_name = config.get("storage_settings", {}).get("db_name")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler = logging.FileHandler(
    filename=f'.logs/log_report_{datetime.now().strftime("%Y-%m-%d")}.log',
    encoding='utf-8'
)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


async def main(tab_resolver, page_loader, product_searcher, cleaner, writer, storage):

    async with async_playwright() as p:
        try:
            page = await tab_resolver.get_target_page(p)
        except Error as e:
            clean_error_message = str(e).split("Call log:")[0].strip()
            logger.error(f"Не удалось получить целевую вкладку: {clean_error_message}")
            return
        logger.info(f"Успешно подключились к странице:{await page.title()}")
        await page_loader.scroll_page(page, timeout_delay)
        await page.wait_for_timeout(5000)
        cards = await page.locator('div[class*="min-h-[232px]"]').all()
        logger.info(f"Робот нашел карточек на экране: {len(cards)}")
        raw_data = await product_searcher.collect_new_products(page)
        clprod = await cleaner.clean_products(raw_data)
        logger.info("Сохранение данных..")
        with storage as s:
            s.init_db()
            s.save_items(clprod)
        logger.info("Данные сохранены успешно.")


if __name__ == "__main__":
    asyncio.run(
        main(
            TabResolver(cdp_url, target_tab_keyword, category), 
            PageLoader(), 
            ProductSearcher(), 
            Cleaner(),
            Writer(),
            Storage(dbname= db_name)
        )
    )