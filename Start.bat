@echo off
chcp 65001 > nul
title Запуск Скарбниця Знань v6.0

:: Переходимо в папку, де лежить цей бат-файл (щоб працювало з будь-якого місця)
cd /d "%~dp0"

:: 1. Перевірка, чи є на ПК Python
python --version >nul 2>&1
if errorlevel 1 (
    color 4F
    echo [ПОМИЛКА] Python не знайдено на цьому комп'ютері!
    echo.
    echo Щоб програма працювала, вам потрібно встановити Python.
    echo Завантажте його з сайту: https://www.python.org/downloads/
    echo ВАЖЛИВО: При встановленні обов'язково поставте галочку "Add Python.exe to PATH"!
    echo.
    pause
    exit /b
)

:: 2. Перевірка першого запуску (встановлення бібліотек)
if not exist ".venv\Scripts\python.exe" (
    color 0B
    echo =======================================================
    echo    ПЕРШИЙ ЗАПУСК: Зачекайте, йде налаштування...
    echo =======================================================
    echo.
    echo [1/3] Створення ізольованого середовища...
    python -m venv .venv

    echo [2/3] Підготовка до встановлення...
    .venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1

    if exist "requirements.txt" (
        echo [3/3] Завантаження компонентів (PyQt6, Selenium тощо)...
        echo Це може зайняти хвилину, не закривайте вікно!
        .venv\Scripts\python.exe -m pip install -r requirements.txt
        echo.
        color 0A
        echo [УСПІХ] Усе готово! Запускаю програму...
        timeout /t 3 >nul
    ) else (
        color 4F
        echo [ПОМИЛКА] Файл requirements.txt не знайдено! Програма не може встановити залежності.
        pause
        exit /b
    )
)

:: 3. Звичайний запуск програми
:: Використовуємо pythonw.exe, щоб сховати чорне вікно консолі під час роботи програми
start "" ".venv\Scripts\pythonw.exe" main.py