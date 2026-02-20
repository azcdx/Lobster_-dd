@echo off
REM LobsterAI Telegram Bot 开机启动配置脚本

echo ========================================
echo   LobsterAI Bot 开机启动配置
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

echo [1/4] 配置开机启动任务...
echo.

REM 获取当前脚本的目录
set "SCRIPT_DIR=%~dp0"
set "BOT_SCRIPT=%SCRIPT_DIR%start_bot.bat"
set "WORK_DIR=%SCRIPT_DIR%"

REM 删除旧任务（如果存在）
schtasks /delete /tn "LobsterAI_Telegram_Bot" /f >nul 2>&1

REM 创建新任务
schtasks /create /tn "LobsterAI_Telegram_Bot" /tr "\"%BOT_SCRIPT%\"" /sc onlogon /rl highest /f

if %errorlevel% neq 0 (
    echo [错误] 任务创建失败
    pause
    exit /b 1
)

echo [2/4] 设置任务为系统启动时运行...
schtasks /change /tn "LobsterAI_Telegram_Bot" /disable

REM 删除旧任务（如果存在）
schtasks /delete /tn "LobsterAI_Bot_AutoStart" /f >nul 2>&1

REM 创建系统启动任务
schtasks /create /tn "LobsterAI_Bot_AutoStart" /tr "\"%BOT_SCRIPT%\"" /sc onstart /ru "SYSTEM" /rl highest /f

if %errorlevel% neq 0 (
    echo [错误] 系统启动任务创建失败
    pause
    exit /b 1
)

echo [3/4] 创建启动快捷方式...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_DIR%\LobsterAI Bot.lnk"

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath = '%BOT_SCRIPT%'; $s.WorkingDirectory = '%WORK_DIR%'; $s.Save()"

if %errorlevel% neq 0 (
    echo [警告] 快捷方式创建失败，但任务计划已配置
) else (
    echo [信息] 启动文件夹快捷方式已创建
)

echo [4/4] 验证配置...
schtasks /query /tn "LobsterAI_Bot_AutoStart" /fo list | findstr "状态"

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo Bot 已配置为开机自动启动，包括：
echo.
echo 1. 系统启动时运行（任务计划程序）
echo    - 任务名称: LobsterAI_Bot_AutoStart
echo    - 触发器: 系统启动时
echo    - 运行身份: SYSTEM
echo.
echo 2. 用户登录时运行（启动文件夹）
echo    - 位置: %STARTUP_DIR%
echo.
echo 管理任务:
echo   查看任务: schtasks /query /tn "LobsterAI_Bot_AutoStart"
echo   手动运行: schtasks /run /tn "LobsterAI_Bot_AutoStart"
echo   禁用任务: schtasks /disable /tn "LobsterAI_Bot_AutoStart"
echo   启用任务: schtasks /enable /tn "LobsterAI_Bot_AutoStart"
echo   删除任务: schtasks /delete /tn "LobsterAI_Bot_AutoStart" /f
echo.
echo 如需测试，请重启计算机或运行:
echo   schtasks /run /tn "LobsterAI_Bot_AutoStart"
echo.

pause
