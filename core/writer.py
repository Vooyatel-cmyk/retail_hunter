from openpyxl import Workbook
from datetime import datetime

class Writer:
    def __init__(self, work_book = None):
        if work_book is None:
            self.work_book = Workbook()

    def _file_name_generator(self) -> str:
        return f".result/report_{datetime.now().strftime("%Y-%m-%d")}.xlsx"

    def new_book(self, data):
        work_book_sheet = self.work_book[self.work_book.sheetnames[0]]
        for product in data:
            work_book_sheet.append([product["title"], product["raw_price"], product['raw_stock']])
        self.work_book.save(self._file_name_generator())

def test():
    writer = Writer()
    data = [
 {'raw_old_price': '542.89',
  'raw_price': '406.89',
  'raw_stock': '20 шт',
  'sale_percent': 25.05,
  'title': 'Пицца Классическая 600гр'},
 {'raw_old_price': '399',
  'raw_price': '359',
  'raw_stock': '20 шт',
  'sale_percent': 10.03,
  'title': 'Пицца Маргарита 600гр '},
 {'raw_old_price': '542.89',
  'raw_price': '406.89',
  'raw_stock': '20 шт',
  'sale_percent': 25.05,
  'title': 'Пицца Пепперони 600гр'},
 {'raw_old_price': '598.89',
  'raw_price': '448.89',
  'raw_stock': '20 шт',
  'sale_percent': 25.05,
  'title': 'Пицца Сырная курочка 600гр'},
 {'raw_old_price': '406.89',
  'raw_price': '304.89',
  'raw_stock': '20 шт',
  'sale_percent': 25.07,
  'title': 'Пицца ДУЭТ 550гр'},
 {'raw_old_price': None,
  'raw_price': '179',
  'raw_stock': '5 шт',
  'sale_percent': 0,
  'title': 'Свекольник 500гр'},
 ]
    writer.new_book(data)

if __name__ == "__main__":
    print("go")
    test()
