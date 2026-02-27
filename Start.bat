@echo off
REM Вмикаємо підтримку UTF-8 (щоб українська мова відображалася коректно)
chcp 65001 >nul
title Treasury of Knowledge v5.0
color 0E

REM Переходимо в папку зі скриптом
cd /d "%~dp0"

echo ===================================================
echo 🏛️ Treasury of Knowledge v5.0
echo Перевірка системних вимог...
echo ===================================================

REM Перевірка наявності бібліотек
python -c "import customtkinter, selenium, bs4, docx, plyer, deep_translator, docx2pdf, PIL, pystray, pyperclip" 2>nul

if %errorlevel% neq 0 (
    echo [!] Виявлено перший запуск або відсутні модулі.
    echo [~] Встановлюємо необхідні бібліотеки. Будь ласка, зачекайте...
    echo ===================================================

    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        pip install customtkinter selenium beautifulsoup4 lxml python-docx plyer deep-translator docx2pdf requests Pillow pystray pyperclip
    )

    echo ===================================================
    echo [V] Усі залежності успішно встановлено!
)

REM Автоматичне створення красивого ярлика
set SHORTCUT="%USERPROFILE%\Desktop\Скарбниця Знань.lnk"
if not exist %SHORTCUT% (
    echo [~] Створення ярлика на Робочому столі...

    echo Set oWS = WScript.CreateObject^("WScript.Shell"^) > CreateShortcut.vbs
    echo sLinkFile = %SHORTCUT% >> CreateShortcut.vbs
    echo Set oLink = oWS.CreateShortcut^(sLinkFile^) >> CreateShortcut.vbs
    echo oLink.TargetPath = "%~dp0Start.bat" >> CreateShortcut.vbs
    echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
    echo oLink.IconLocation = "%~dp0icon.ico" >> CreateShortcut.vbs
    echo oLink.Save >> CreateShortcut.vbs

    REM Створюємо системне віконце повідомлення для користувача!
    echo MsgBox "Ярлик програми успішно створено на Вашому Робочому столі!" ^& vbCrLf ^& "Наступного разу просто запускайте Скарбницю Знань звідти.", 64, "Скарбниця Знань" >> CreateShortcut.vbs

    cscript //nologo CreateShortcut.vbs
    del CreateShortcut.vbs
    echo [V] Ярлик створено!
)

echo [V] Запуск програми...
timeout /t 2 >nul

REM Запуск програми без чорного вікна консолі на фоні
start "" pythonw main.py