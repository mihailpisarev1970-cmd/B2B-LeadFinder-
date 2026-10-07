import logging
from playwright.async_api import async_playwright
from services.extractor import DataExtractor

logger = logging.getLogger(__name__)

class SiteParser:
    def __init__(self):
        self.extractor = DataExtractor()
        # Дополнительные пути для поиска контактов
        self.paths_to_check = ['/', '/contacts', '/about', '/privacy-policy', '/policy']

    async def parse_site(self, base_url: str) -> dict:
        base_url = base_url.strip()
        if not base_url.startswith("http"):
            base_url = "https://" + base_url

        collected_data = {"phones": set(), "emails": set(), "inns": set()}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = await context.new_page()

            for path in self.paths_to_check:
                url = base_url.rstrip('/') + path
                try:
                    logger.info(f"Проверяем: {url}")
                    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    
                    # Ждем выполнения JS-скриптов (особенно для SPA)
                    await page.wait_for_timeout(3000) 
                    
                    html_content = await page.content()
                    
                    # 1. Извлекаем из HTML
                    extracted = self.extractor.extract_from_html(html_content)
                    collected_data["phones"].update(extracted["phones"])
                    collected_data["emails"].update(extracted["emails"])
                    collected_data["inns"].update(extracted["inns"])

                    # 2. Делаем скриншот для OCR (если нужно вытащить данные с картинок)
                    screenshot_bytes = await page.screenshot(full_page=True)
                    ocr_extracted = self.extractor.extract_from_image(screenshot_bytes)
                    
                    collected_data["phones"].update(ocr_extracted["phones"])
                    collected_data["emails"].update(ocr_extracted["emails"])
                    collected_data["inns"].update(ocr_extracted["inns"])

                except Exception as e:
                    logger.debug(f"Страница {url} недоступна или произошла ошибка: {e}")
                    continue

            await browser.close()

        # Возвращаем первое найденное значение (или объединяем все)
        return {
            "site": base_url,
            "phone": list(collected_data["phones"])[0] if collected_data["phones"] else "",
            "email": list(collected_data["emails"])[0] if collected_data["emails"] else "",
            "inn": list(collected_data["inns"])[0] if collected_data["inns"] else ""
        }