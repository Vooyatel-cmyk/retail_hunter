class Cleaner:
    def __init__(self):
        pass

    async def clean_raw_price(self, products: list[dict], key: str) -> list[dict]:
        for product in products: 
            if '\xa0' not in product[key] and '\n' not in product[key]:
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

    async def process_sale_percent(self, products, new_price, old_price):
        for product in products:
            if product[new_price] is not None and product[old_price] is not None:
                product['sale_percent'] = round((1 - (float(product[new_price]) / float(product[old_price]))) * 100, 2)
            else:
                product['sale_percent'] = 0 
        return products