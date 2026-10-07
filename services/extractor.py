import re
from bs4 import BeautifulSoup

class DataExtractor:
    def __init__(self):
        # Регулярки для парсинга
        self.phone_pattern = re.compile(r'(?:(?:\+7|8)[\s\-]?)?(?:\(?\d{3}\)?[\s\-]?)?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')
        self.email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        self.inn_pattern = re.compile(r'\b\d{10}\b|\b\d{12}\b')

    def extract_from_text(self, text: str) -> dict:
        phones = list(set(self.phone_pattern.findall(text)))
        emails = list(set(self.email_pattern.findall(text)))
        inns = list(set(self.inn_pattern.findall(text)))
        
        return {
            "phones": [p for p in phones if len(re.sub(r'\D', '', p)) >= 10], # Фильтрация ложных срабатываний
            "emails": emails,
            "inns": inns
        }

    def extract_from_html(self, html: str) -> dict:
        soup = BeautifulSoup(html, 'lxml')
        # Удаляем лишние теги (скрипты, стили)
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        text = soup.get_text(separator=' ')
        return self.extract_from_text(text)