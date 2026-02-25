@echo off
chcp 65001 > nul

:: 1. Блискавична перевірка: чи є всі потрібні модулі? (Робиться за долі секунди)
python -c "import customtkinter, selenium, bs4, docx, plyer, deep_translator, docx2pdf, readability, requests" 2>nul

:: 2. Якщо хоча б одного модуля немає, запускаємо дозавантаження
if %errorlevel% neq 0 (
    echo ===================================================
    echo ⚙️ Скарбниця Знань: Налаштування середовища...
    echo Виявлено відсутні компоненти. Завантажую необхідне...
    echo ===================================================
    
    :: pip сам розбереться: те що є - пропустить, чого немає - скачає
    pip install customtkinter selenium beautifulsoup4 python-docx plyer deep-translator docx2pdf readability-lxml requests
    
    echo.
    echo ✅ Усі бібліотеки готові до роботи!
    timeout /t 2 >nul
)

:: 3. Запуск самої програми (без чорного вікна на фоні)
start "" pythonw main.py