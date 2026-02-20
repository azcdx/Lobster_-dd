@echo off
REM LobsterAI Telegram 桥接 - 一键启动

title LobsterAI Telegram 桥接器

color 0B

echo.
echo ========================================
echo    🦞 LobsterAI Telegram 桥接器
echo ========================================
echo.

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未安装 Python
    pause
    exit /b 1
)

echo [1/2] 启动 Telegram 桥接器...
start /B wscript.exe start_bridge_hidden.vbs

timeout /t 2 /nobreak >nul

echo [2/2] 启动 LobsterAI 监听器...
start /B python lobsterai_telegram_monitor.py

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo    ✅ 桥接器已启动
echo ========================================
echo.
echo 📱 Telegram Bot: t.me/azcdxDD_bot
echo.
echo 💬 现在可以在 Telegram 与 LobsterAI 对话了！
echo.
echo 💡 提示:
echo   - 桥接器在后台运行
echo   - 关闭此窗口不影响运行
echo   - 运行"停止桥接器.bat"可停止
echo.
echo ========================================
echo.

REM 自动打开 Telegram
start https://t.me/azcdxDD_bot

timeout /t 3 /nobreak >nul
