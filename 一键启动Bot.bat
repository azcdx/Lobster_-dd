@echo off
REM LobsterAI Bot - 一键启动脚本

title LobsterAI Bot - 正在启动...

REM 颜色设置
color 0A

echo.
echo ========================================
echo    🦞 LobsterAI Bot - 一键启动
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python
    echo 请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装依赖...
    pip install python-telegram-bot==20.7 -q
)

REM 获取当前目录
set "BOT_DIR=%~dp0"
cd /d "%BOT_DIR%"

echo [1/3] 检查运行状态...
tasklist | findstr python >nul
if %errorlevel% equ 0 (
    echo [信息] Bot 已经在运行
    echo.
    goto :SHOW_INFO
)

echo [2/3] 启动守护进程...
start /B python bot_daemon.py

REM 等待启动
timeout /t 5 /nobreak >nul

echo [3/3] 检查连接状态...
tasklist | findstr python >nul
if %errorlevel% neq 0 (
    echo [错误] 启动失败
    pause
    exit /b 1
)

:SHOW_INFO
echo.
echo ========================================
echo    ✅ 启动成功！
echo ========================================
echo.
echo 📱 Telegram Bot: t.me/azcdxDD_bot
echo.
echo 📋 可用命令:
echo   /start   - 开始使用
echo   /help    - 查看帮助
echo   /status  - 系统状态
echo   /exec    - 执行命令
echo   /ls      - 列出文件
echo.
echo 💡 提示:
echo   - 直接发送文本消息即可对话
echo   - 可以发送文件和图片
echo   - 此窗口可以关闭，Bot 会继续运行
echo.
echo 📊 日志文件:
echo   - Bot 日志: telegram_bot.log
echo   - 守护进程: bot_daemon.log
echo.
echo ========================================
echo.

REM 询问是否打开 Telegram
echo 按任意键关闭此窗口...
pause >nul

exit
