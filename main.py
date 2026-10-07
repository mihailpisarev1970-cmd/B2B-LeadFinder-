import asyncio
import logging
import pandas as pd
from datetime import datetime
from services.parser import SiteParser
from services.dadata_api import get_lpr_by_inn

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_site(url: str, parser: SiteParser) -> dict:
    logger.info(f"=== Начало обработки сайта: {url} ===")
    
    # 1. Парсинг сайта (ищем контакты и ИНН)
    site_data = await parser.parse_site(url)
    
    # Формируем структуру будущей строки в Excel
    final_data = {
        "Название компании": "",
        "Сайт": site_data["site"],
        "Телефон": site_data["phone"],
        "E-mail": site_data["email"],
        "ИНН": site_data["inn"],
        "Фамилия ЛПР": "",
        "Имя ЛПР": "",
        "Отчество ЛПР": "",
        "Должность": ""
    }

    # 2. Если нашли ИНН, пробиваем ЛПР через DaData
    if site_data["inn"]:
        logger.info(f"Найден ИНН: {site_data['inn']}. Обращение к DaData...")
        lpr_data = await get_lpr_by_inn(site_data["inn"])
        
        # Обновляем словарь полученными данными
        final_data["Название компании"] = lpr_data.get("company_name", "")
        final_data["Фамилия ЛПР"] = lpr_data.get("surname", "")
        final_data["Имя ЛПР"] = lpr_data.get("name", "")
        final_data["Отчество ЛПР"] = lpr_data.get("patronymic", "")
        final_data["Должность"] = lpr_data.get("position", "")
    else:
        logger.warning(f"ИНН на сайте {url} не найден.")

    logger.info(f"=== Завершение обработки: {url} ===\n")
    return final_data

async def main():
    # Чтение списка сайтов
    try:
        with open("sites.txt", "r", encoding="utf-8") as f:
            sites = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logger.error("Файл sites.txt не найден в корневой директории.")
        return

    if not sites:
        logger.warning("Файл sites.txt пуст.")
        return

    parser = SiteParser()
    all_results = []
    
    # Обработка сайтов по очереди
    for site in sites:
        result = await process_site(site, parser)
        all_results.append(result)

    # Сохранение результатов в Excel
    if all_results:
        # Автоматическое имя файла с текущей датой и временем
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
        excel_filename = f"Результаты_ЛПР_{current_time}.xlsx"
        
        # Создаем DataFrame из списка словарей
        df = pd.DataFrame(all_results)
        
        # Сохраняем в Excel без колонки с индексами (0, 1, 2...)
        df.to_excel(excel_filename, index=False, engine='openpyxl')
        
        logger.info(f"ПАРСИНГ ЗАВЕРШЕН! Все данные успешно сохранены в файл: {excel_filename}")
    else:
        logger.info("Нет данных для сохранения.")

if __name__ == "__main__":
    asyncio.run(main())