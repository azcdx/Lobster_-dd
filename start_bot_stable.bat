@echo off
REM LobsterAI Telegram Bot - 稳定版启动脚本

set "BOT_DIR=C:\Users\Administrator\lobsterai\project"
set "LOG_FILE=%BOT_DIR%\telegram_bot.log"
set "PID_FILE=%BOT_DIR%\bot.pid"

cd /d "%BOT_DIR%"

REM 检查是否已经在运行
if exist "%PID_FILE%" (
    set /p OLD_PID=<"%PID_FILE%"
    tasklist /FI "PID eq %OLD_PID%" 2>nul | find /I /N "python.exe">nul
    if "%ERRORLEVEL%"=="0" (
        echo [信息] Bot 已经在运行中 (PID: %OLD_PID%)
        pause
        exit /b 0
    )
    REM PID 文件过期，删除
    del "%PID_FILE%"
)

echo [%TIME%] 启动 LobsterAI Bot...
echo [%TIME%] 工作目录: %BOT_DIR%
echo.

REM 启动 Bot 并记录 PID
start /B python telegram_bot.py > "%BOT_DIR%\bot_stdout.log" 2>&1

REM 等待一下确保进程启动
timeout /t 3 /nobreak >nul

REM 获取 Python 进程 PID
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| find "python.exe"') do (
    set BOT_PID=%%~i
    echo !BOT_PID! > "%PID_FILE%"
    goto :FOUND
)

:FOUND
echo [%TIME%] Bot 已启动
echo [%TIME%] 日志文件: %LOG_FILE%
echo [%TIME%] 按 Ctrl+C 停止 Bot
echo.

REM 持续监控日志
tail -f "%LOG_FILE%" 2>nul

if exist "%PID_FILE%" del "%PID_FILE%"
echo [%TIME%] Bot 已停止
