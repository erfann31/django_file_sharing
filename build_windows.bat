@echo off
setlocal
set "BUILD_EXIT_CODE=0"
cd /d "%~dp0"

echo ========================================
echo Building LocalShare from:
echo %CD%
echo ========================================
echo.

echo [1/3] Installing build requirements...
python -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo.
echo [2/3] Collecting Django static files...
python manage.py collectstatic --noinput
if errorlevel 1 goto :failed

echo.
echo [3/3] Creating the Windows executable...
echo Stopping any running LocalShare instance...
taskkill /F /IM LocalShare.exe >nul 2>&1

if exist "dist\LocalShare.exe" (
    echo Removing the previous executable...
    del /F /Q "dist\LocalShare.exe"
    if exist "dist\LocalShare.exe" (
        echo.
        echo ERROR: Cannot replace dist\LocalShare.exe because it is still in use.
        echo Close LocalShare, any Explorer preview of the file, and antivirus scans, then try again.
        goto :failed
    )
)

python -m PyInstaller --noconfirm --clean run.spec
if errorlevel 1 goto :failed

if not exist "dist\LocalShare.exe" (
    echo.
    echo ERROR: PyInstaller finished but dist\LocalShare.exe was not created.
    goto :failed
)

echo.
echo ========================================
echo Build complete: dist\LocalShare.exe
echo ========================================
goto :end

:failed
set "BUILD_EXIT_CODE=%ERRORLEVEL%"
if "%BUILD_EXIT_CODE%"=="0" set "BUILD_EXIT_CODE=1"
echo.
echo ========================================
echo BUILD FAILED (exit code %BUILD_EXIT_CODE%)
echo Review the error shown above. This window will remain open.
echo ========================================

:end
echo.
if not defined CI pause
endlocal & exit /b %BUILD_EXIT_CODE%
