from openpyxl import Workbook
from datetime import datetime
from typing import Any

class Writer:
    def __init__(self, work_book = None):
        if work_book is None:
            self.work_book = Workbook()

    def _file_name_generator(self) -> str:
        return f".result/report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"

    def new_book(self, product_list: list[dict[str, Any]]) -> None:
        work_book_sheet = self.work_book[self.work_book.sheetnames[0]]
        for product in product_list:
            work_book_sheet.append([product["title"], product["raw_price"], product['raw_stock']])
        self.work_book.save(self._file_name_generator())