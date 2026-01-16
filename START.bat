@echo off
title Modern_USA_News - FREE Automation
color 0A

echo ============================================================
echo            MODERN USA NEWS - FREE AUTOMATION
echo ============================================================
echo.
echo   100%% Free - No API Keys Required
echo   RSS-Based News Collection
echo   AI Content Generation
echo   Image Generation with Watermarks
echo.
echo ============================================================
echo.
echo Select an option:
echo.
echo   1. Run Full Daily Cycle (Recommended)
echo   2. Fetch News Only
echo   3. Generate Posts Only
echo   4. Generate Images Only
echo   5. Open Dashboard
echo   6. Show Status
echo   7. Exit
echo.
echo ============================================================
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto daily
if "%choice%"=="2" goto fetch
if "%choice%"=="3" goto generate
if "%choice%"=="4" goto images
if "%choice%"=="5" goto dashboard
if "%choice%"=="6" goto status
if "%choice%"=="7" goto exit

echo Invalid choice. Please try again.
pause
goto :eof

:daily
echo.
echo Running full daily cycle...
echo.
python cli.py daily
pause
goto :eof

:fetch
echo.
echo Fetching news from RSS feeds...
echo.
python cli.py fetch
pause
goto :eof

:generate
echo.
echo Generating posts...
echo.
set /p count="How many posts? (default 5): "
if "%count%"=="" set count=5
python cli.py generate --count %count%
pause
goto :eof

:images
echo.
echo Generating images...
echo.
python cli.py images
pause
goto :eof

:dashboard
echo.
echo Starting dashboard...
echo.
echo Open http://localhost:5000 in your browser
echo.
python free_dashboard.py
pause
goto :eof

:status
echo.
echo Checking status...
echo.
python cli.py status
pause
goto :eof

:exit
echo.
echo Goodbye!
exit
