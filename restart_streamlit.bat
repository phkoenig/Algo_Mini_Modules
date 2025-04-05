@echo off
echo.
echo ========================================
echo    Streamlit App Restart Utility
echo ========================================
echo.

:: Kill existing processes
echo [1/5] Cleaning up old processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

:: Clear Chrome's localhost cache
echo [2/5] Clearing browser cache...
taskkill /F /IM chrome.exe /FI "WINDOWTITLE eq localhost:8501*" 2>nul
timeout /t 1 /nobreak >nul

:: Activate virtual environment and install dependencies
echo [3/5] Setting up Python environment...
call venv\Scripts\activate.bat
python -m pip install -U streamlit
timeout /t 2 /nobreak >nul

:: Start Browser-Tools-Server in a visible window
echo [4/5] Starting Browser-Tools-Server...
echo.
echo WICHTIG: Bitte erlaube den Admin-Zugriff im nächsten Fenster!
echo.
start "Browser-Tools-Server" cmd /k "title Browser-Tools-Server && color 0A && echo Browser-Tools-Server wird gestartet... && echo. && npx @agentdeskai/browser-tools-server@1.2.0 --port 3025 --log-level debug"

:: Wait for server to initialize
echo Warte auf Server-Start...
timeout /t 5 /nobreak >nul

:: Start Streamlit in a visible window with activated venv
echo [5/5] Starting Streamlit...
start "Streamlit App" cmd /k "title Streamlit App && color 0B && cd /d %~dp0 && call venv\Scripts\activate.bat && echo Streamlit wird gestartet... && echo. && python -m streamlit run gui/app.py --server.port 8501"

:: Wait for Streamlit to initialize
timeout /t 3 /nobreak >nul

:: Final instructions
echo.
echo ========================================
echo    Setup abgeschlossen!
echo ========================================
echo.
echo Bitte überprüfe:
echo 1. Browser-Tools-Server (grünes Fenster):
echo    - Läuft auf Port 3025
echo    - Zeigt "Server started successfully"
echo.
echo 2. Streamlit App (blaues Fenster):
echo    - Läuft auf Port 8501
echo    - Zeigt "You can now view your Streamlit app in the browser"
echo.
echo 3. Chrome Extension:
echo    - Öffne Chrome DevTools (F12)
echo    - Wechsle zum "BrowserToolsMCP" Tab
echo    - Status sollte "Connected" (grün) zeigen
echo.
echo Drücke eine Taste zum Beenden...
pause >nul 