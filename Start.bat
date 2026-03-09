@echo off
:: Go to the exact folder where this .bat file is located
cd /d "%~dp0"

:: Check if the virtual environment folder exists
IF NOT EXIST ".venv\" (
    echo ========================================================
    echo    * Treasury of Knowledge: First Run Setup *
    echo ========================================================
    echo.
    echo [1/3] Creating isolated virtual environment (.venv)...
    python -m venv .venv

    echo.
    echo [2/3] Updating package installer (pip)...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet

    echo.
    echo [3/3] Installing required libraries from requirements.txt...
    ".venv\Scripts\pip.exe" install -r requirements.txt

    echo.
    echo ========================================================
    echo  OK! Installation successfully completed!
    echo  Starting the application...
    echo ========================================================
    timeout /t 3 > nul
)

:: Run the app in the background using pythonw.exe (no terminal window)
start "" ".venv\Scripts\pythonw.exe" "main.py"

:: Close the .bat file immediately
exit