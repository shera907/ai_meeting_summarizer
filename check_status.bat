@echo off
echo ============================================
echo AI Meeting Summarizer - Status Check
echo ============================================
echo.

echo Checking Backend (Port 5000)...
curl -s http://localhost:5000/health
if %errorlevel% equ 0 (
    echo.
    echo [OK] Backend is running!
) else (
    echo.
    echo [ERROR] Backend is not running
)

echo.
echo.
echo Checking if processes are running...
tasklist /FI "IMAGENAME eq python.exe" /FI "WINDOWTITLE eq backend*" 2>NUL | find /I "python.exe" >NUL
if %errorlevel% equ 0 (
    echo [OK] Python backend process found
) else (
    echo [ERROR] Python backend process not found
)

tasklist /FI "IMAGENAME eq electron.exe" 2>NUL | find /I "electron.exe" >NUL
if %errorlevel% equ 0 (
    echo [OK] Electron frontend process found
) else (
    echo [ERROR] Electron frontend process not found
)

echo.
echo ============================================
echo If both are OK, your app is running!
echo ============================================
pause

