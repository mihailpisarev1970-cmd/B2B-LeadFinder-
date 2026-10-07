# B2B-LeadFinder-
Этот скрипт собирает лиды для холодного аутрича и выходит напрямую на Лиц, Принимающих Решения
# 🎯 B2B-LeadFinder: Асинхронный парсер контактов и ЛПР

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Async-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev/)
[![DaData API](https://img.shields.io/badge/DaData-Enrichment-FF4F00?style=flat)](https://dadata.ru/)
[![Pandas](https://img.shields.io/badge/Pandas-Excel_Export-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**B2B-LeadFinder** — инструмент на Python для автоматизированного сбора прямых контактных данных с сайтов компаний и автоматического выявления Лиц, Принимающих Решения (директоров, учредителей, индивидуальных предпринимателей) по ИНН через реестры API DaData.

Решает задачу быстрого формирования чистой и обогащенной базы контактов для холодного аутрича, мессенджер-маркетинга и рассылки коммерческих предложений.

---

## 💡 Как это работает

```text
[Список сайтов (sites.txt)]
            │
            ▼
┌─────────────────────────┐
│ Playwright (Headless)   │ ──► Обход страниц (/, /contacts, /about, /policy)
└─────────────────────────┘     Рендеринг JS / SPA с ожиданием DOM
            │
            ▼
┌─────────────────────────┐
│ Регулярные выражения    │ ──► Извлечение телефонов, E-mail и ИНН
└─────────────────────────┘
            │
            ▼ (при наличии ИНН)
┌─────────────────────────┐
│ API DaData (EGRUL/EGRIP)│ ──► Поиск ФИО руководителя и точной должности
└─────────────────────────┘
            │
            ▼
[Excel-файл: Результаты_ЛПР_YYYY-MM-DD_HH-MM.xlsx]

📂 Структура репозитория
b2b-leadfinder/
├── config/
│   └── settings.py          # Валидация и загрузка настроек из .env
├── services/
│   ├── dadata_api.py        # Асинхронный клиент к API DaData
│   ├── extractor.py         # Парсинг текста регулярными выражениями
│   └── parser.py            # Модуль веб-скрейпинга на Playwright
├── .env.example             # Шаблон конфигурации окружения
├── .gitignore               # Список исключений для Git
├── main.py                  # Главный скрипт оркестрации и выгрузки в Excel
├── requirements.txt         # Список внешних зависимостей
├── sites.txt                # Список целевых веб-сайтов
└── README.md                # Документация проекта

🚀 Быстрый старт
1. Клонирование репозитория
git clone [https://github.com/ВАШ_АККАУНТ/b2b-leadfinder.git](https://github.com/ВАШ_АККАУНТ/b2b-leadfinder.git)
cd b2b-leadfinder

2. Развертывание виртуального окружения
Windows:
python -m venv venv
venv\Scripts\activate

Linux / macOS:
python3 -m venv venv
source venv/bin/activate

3. Установка зависимостей и браузеров
pip install -r requirements.txt
playwright install chromium

4. Настройка переменных окружения
Создайте локальный файл .env на основе шаблона:
cp .env.example .env

Откройте файл .env и укажите ваш API-токен сервиса DaData:
DADATA_TOKEN=ваш_токен_dadata

🛠️ Запуск и использование
1. Откройте файл sites.txt и внесите список ссылок (каждая строка — отдельный сайт):
[https://example-service.ru/](https://example-service.ru/)
koreamaster.ru
[https://only-vag.ru](https://only-vag.ru)

Запустите основной скрипт:
python main.py

По окончании обработки скрипт сгенерирует Excel-файл в корневой папке с названием вида:

Результаты_ЛПР_2026-10-07_18-50.xlsx.
