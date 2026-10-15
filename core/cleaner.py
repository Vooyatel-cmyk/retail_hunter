class Cleaner:
    def __init__(self):
        pass

    async def clean_raw_price(self, products: list[dict], key: str) -> list[dict]:
        for product in products: 
            if '\xa0' and '\n' not in product[key]:
                continue
            if '\n' in product[key]:

                product[key] = product[key].replace('\n', '').replace('\xa0', '')
                kopeiki = product[key][-2]+product[key][-1]
                product[key] = product[key].replace(kopeiki, '')
                product[key] = product[key]+'.'+ kopeiki

            if '\xa0' in product[key]:
                product[key] = product[key].replace('\xa0', '')
        return products

    async def clean_raw_old_price(self, products:list[dict], key:str)-> list[dict]:
        for product in products:
            if product[key] is None:
                continue
            if '\xa0₽' in product[key]:
                product[key] = product[key].replace('\xa0₽', '')
                if len(product[key]) > 3:
                    kopeiki = product[key][-2]+product[key][-1]
                    product[key] = product[key].replace(kopeiki, '')
                    product[key] = product[key]+'.'+ kopeiki
                else:
                    continue
        return products