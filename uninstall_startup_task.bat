@echo off
REM LobsterAI Telegram Bot 开机启动卸载脚本

echo ========================================
echo   LobsterAI Bot 开机启动卸载
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 需要管理员权限
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/3] 删除任务计划程序任务...
schtasks /delete /tn "LobsterAI_Telegram_Bot" /f >nul 2>&1
schtasks /delete /tn "LobsterAI_Bot_AutoStart" /f >nul 2>&1

if %errorlevel% neq 0 (
    echo [警告] 任务删除失败或任务不存在
) else (
    echo [成功] 任务计划已删除
)

echo [2/3] 删除启动文件夹快捷方式...
set "SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\LobsterAI Bot.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo [成功] 启动文件夹快捷方式已删除
) else (
    echo [信息] 启动文件夹快捷方式不存在
)

echo [3/3] 验证卸载...
schtasks /query /tn "LobsterAI_Bot_AutoStart" >nul 2>&1
if %errorlevel% equ 0 (
    echo [警告] 任务仍然存在，请手动检查
) else (
    echo [成功] 所有开机启动项已删除
)

echo.
echo ========================================
echo   卸载完成！
echo ========================================
echo.
echo Bot 不再会在开机时自动启动。
echo 如需手动启动，请双击: start_bot.bat
echo.

pause
