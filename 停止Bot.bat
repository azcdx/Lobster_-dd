@echo off
REM LobsterAI Bot - 停止脚本

title LobsterAI Bot - 停止中...

echo.
echo 🛑 停止 LobsterAI Bot...
echo.

REM 查找并终止所有 Python 进程
tasklist | findstr python >nul
if %errorlevel% neq 0 (
    echo ℹ️  Bot 未运行
    pause
    exit /b 0
)

echo 🔍 找到 Python 进程，正在停止...
taskkill /F /IM python.exe >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ Bot 已停止
) else (
    echo ❌ 停止失败
)

echo.
pause
