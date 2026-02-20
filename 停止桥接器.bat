@echo off
REM 停止 LobsterAI 桥接器

title 停止桥接器

echo.
echo 🛑 停止 LobsterAI 桥接器...
echo.

REM 停止所有相关进程
taskkill /F /IM python.exe >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ 桥接器已停止
) else (
    echo ℹ️  未找到运行中的进程
)

echo.
pause
