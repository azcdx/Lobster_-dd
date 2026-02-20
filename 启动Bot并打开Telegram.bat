@echo off
REM LobsterAI Bot - 一键启动并打开 Telegram

title LobsterAI Bot

REM 设置颜色
color 0B

echo.
echo 🦞 启动中...
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未安装 Python
    pause
    exit /b 1
)

cd /d "%~dp0"

REM 检查依赖
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 安装依赖中...
    pip install python-telegram-bot==20.7 -q
)

REM 检查是否已运行
tasklist | findstr python >nul
if %errorlevel% equ 0 (
    echo ✅ Bot 已在运行
) else (
    echo 🚀 启动 Bot...
    start /B python bot_daemon.py
    timeout /t 3 /nobreak >nul
)

echo.
echo ✅ 就绪！
echo.
echo 📱 Bot 地址: t.me/azcdxDD_bot
echo.

REM 自动打开 Telegram Bot
start https://t.me/azcdxDD_bot

echo 💬 窗口已打开，开始对话吧！
echo.
echo 按任意键关闭...
pause >nul
