from typing import Any

class Cleaner:
    def __init__(self):
        pass

    def _clean_text_feld(self, text:Any) -> str:
        # вынес очистку строк в отдельный метод чтоб не повторять ее несколько раз
        if not isinstance(text, str):
            return ''
        cleaned = text.replace('\xa0', '').strip()

        if '\n' in cleaned:
            cleaned = '.'.join(cleaned.split('\n'))

        return cleaned

    async def clean_products(self, product_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
        cleaned_list = []
        for product in product_list:

            cleaned_product = product.copy()

            if 'raw_price' in cleaned_product:
                cleaned_product['raw_price'] = self._clean_text_feld(cleaned_product['raw_price'])
            if 'title' in cleaned_product:
                cleaned_product['title'] = self._clean_text_feld(cleaned_product['title'])

            cleaned_list.append(cleaned_product)

        return cleaned_list