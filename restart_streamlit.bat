@echo off
setlocal EnableDelayedExpansion

echo.
echo ========================================
echo    Streamlit App Restart Utility
echo ========================================
echo.

:: Set error handling
set "error_occurred=0"

:: Kill existing processes
echo [1/4] Cleaning up old processes...
taskkill /F /IM streamlit.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1
:: Give processes time to fully terminate
timeout /t 3 /nobreak >nul

:: Clear Chrome's localhost cache
echo [2/4] Clearing browser cache...
taskkill /F /IM chrome.exe /FI "WINDOWTITLE eq localhost:8501*" >nul 2>&1
:: Wait for browser to close
timeout /t 2 /nobreak >nul

:: Activate virtual environment and install dependencies
echo [3/4] Setting up Python environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    python -m pip install -U streamlit >nul 2>&1
) else (
    echo Error: Virtual environment not found!
    set "error_occurred=1"
    goto :error
)
timeout /t 2 /nobreak >nul

:: Start services
echo [4/4] Starting services...
echo.
echo WICHTIG: Alle Services werden gestartet
echo.

:: Start Browser-Tools-MCP
echo Starting Browser-Tools-MCP on port 3025...
cmd /c npx -y @agentdeskai/browser-tools-mcp@1.2.0 --port 3025
if !errorlevel! neq 0 (
    echo Error: Failed to start Browser-Tools-MCP
    set "error_occurred=1"
    goto :error
)

:: Wait for MCP to initialize
timeout /t 5 /nobreak >nul

:: Start Streamlit
echo Starting Streamlit on port 8501...
python -m streamlit run gui/login.py --server.port 8501
if !errorlevel! neq 0 (
    echo Error: Failed to start Streamlit
    set "error_occurred=1"
    goto :error
)

goto :end

:error
echo.
echo ========================================
echo    Fehler beim Starten der Services!
echo ========================================
echo.
echo Bitte überprüfe:
echo 1. Läuft bereits eine Instanz der Services?
echo 2. Sind alle erforderlichen Pakete installiert?
echo 3. Sind die Ports 3025 und 8501 verfügbar?
echo.
pause
exit /b 1

:end
if !error_occurred!==0 (
    echo.
    echo ========================================
    echo    Setup erfolgreich abgeschlossen!
    echo ========================================
    echo.
    echo Services erfolgreich gestartet:
    echo 1. Browser-Tools-MCP auf Port 3025
    echo 2. Streamlit App auf Port 8501
    echo.
    echo Öffne http://localhost:8501 im Browser
    echo.
) 