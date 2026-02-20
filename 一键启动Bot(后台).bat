@echo off
REM LobsterAI Bot - 真正的后台启动版本

title LobsterAI Bot - 启动中...

echo.
echo 🦞 启动 LobsterAI Bot...
echo.

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未安装 Python
    pause
    exit /b 1
)

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
    echo 🚀 启动守护进程（后台模式）...
    start /B wscript.exe start_bot_hidden.vbs
    timeout /t 3 /nobreak >nul
)

echo.
echo ========================================
echo    ✅ Bot 已启动（后台运行）
echo ========================================
echo.
echo 📱 Telegram Bot: t.me/azcdxDD_bot
echo.
echo 💡 提示:
echo   - Bot 在后台运行，关闭此窗口不影响
echo   - 如需停止 Bot，运行"停止Bot.bat"
echo.
echo ========================================
echo.

REM 自动打开 Telegram
start https://t.me/azcdxDD_bot

timeout /t 3 /nobreak >nul
