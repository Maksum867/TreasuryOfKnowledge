@echo off
title Treasury of Knowledge

REM Quick check for required modules
python -c "import customtkinter, selenium, bs4, docx, plyer, deep_translator, docx2pdf, readability, requests" 2>nul

if %errorlevel% neq 0 (
    echo ===================================================
    echo Treasury of Knowledge: First run setup...
    echo Installing missing libraries. Please wait...
    echo ===================================================

    pip install customtkinter selenium beautifulsoup4 python-docx plyer deep-translator docx2pdf readability-lxml requests

    echo ===================================================
    echo Setup complete! Starting program...
    timeout /t 2 >nul
)

REM Start the program and close the console
start "" pythonw main.py