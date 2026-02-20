@echo off
REM LobsterAI Telegram Bot Wrapper - 自动重启版本

echo ========================================
echo   LobsterAI Bot 启动包装器
echo   (自动重启模式)
echo ========================================
echo.

:LOOP
echo [%TIME%] 启动 Bot...
cd /d "C:\Users\Administrator\lobsterai\project"

python telegram_bot.py

echo [%TIME%] Bot 意外退出，5秒后自动重启...
echo ========================================
timeout /t 5 /nobreak >nul

goto LOOP
