from typing import List, Dict, Any, Optional
from playwright.async_api import Locator

class ProductSearcher:
    def __init__(self):
        self.seen_products = set()

    async def _parse_single_card(self, card_locator) -> Optional[Dict[str, Any]]:
        try:

            title = (await card_locator.locator("span.line-clamp-3:visible").inner_text()).strip()
            raw_price = await card_locator.locator('div.text-roman, div.text-text-black').first.inner_text()

            old_price_locator = card_locator.locator('del.text-gray-dark')

            if await old_price_locator.count() > 0:
                raw_old_price = await old_price_locator.inner_text()
            else:
                raw_old_price = None

            raw_stock_locator = card_locator.locator('span.text-accent-primary')

            if await raw_stock_locator.count() > 0:
                raw_stock = await raw_stock_locator.inner_text()
            else:
                raw_stock = None

            return {
                "title":title,
                "raw_price":raw_price,
                "raw_old_price":raw_old_price,
                "raw_stock":raw_stock
            }
        
        except Exception as e: 
            print(f"Ошибка внутри карточки: {e}") # ТУТ МЫ УВИДИМ ОШИБКУ
            return None

    
    async def collect_new_products(self, page) -> List[Dict[str, Any]]:
        cards = await page.locator('div[class*="min-h-[232px]"]').all()

        products = []

        for card in cards:

            title = (await card.locator("span.line-clamp-3:visible").inner_text()).strip()

            if title in self.seen_products:
                continue

            self.seen_products.add(title)
            product_data = await self._parse_single_card(card)

            if product_data is not None:
                products.append(product_data)
        return products
