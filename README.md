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
