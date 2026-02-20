@echo off
REM LobsterAI Telegram Bot 启动脚本

echo ========================================
echo   LobsterAI Telegram Bot 启动器
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
python -c "import telegram" >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

echo [2/3] 检查工作目录...
if not exist "%CD%" (
    echo [错误] 工作目录不存在
    pause
    exit /b 1
)

echo [3/3] 启动 Bot...
echo.
echo ========================================
echo   Bot 正在运行，请按 Ctrl+C 停止
echo ========================================
echo.

python telegram_bot.py

pause
