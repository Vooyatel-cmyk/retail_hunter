# retail_hunter
Парсер цен и остатков интернет магазина. Собирает названия товаров, текущие и старые цены, наличие.

## Возможности
- сбор данных по выбранной категории
- очистка цен

## Стек
Python, Playwright, openpyxl

## Запуск проекта

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Vooyatel-cmyk/retail_hunter
   cd retail_hunter
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Установите системные зависимости для Playwright:
   ```bash
   playwright install chromium
   ```
4. Настройте конфигурацию:
   * Скопируйте файл `example.config.json` и переименуйте его в `config.json`
   * Откройте `config.json` и впишите ваш адрес
5. Запустите Google Chrome в режиме отладки (команда откроет браузер и сразу освободит консоль):
   ```cmd
   start "" "%PROGRAMFILES%\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="%USERPROFILE%\chrome_dev_profile"
   ```
   *(Если Chrome установлен без прав администратора, замените `%PROGRAMFILES%` на `%LOCALAPPDATA%`)*
6. Запустите главный скрипт:
   ```bash
   python main.py
   ```
## Планы
- асинхронный режим
- парсинг нескольких категорий
- сохранение данных в sqlite
- сохранение данных в Excel
