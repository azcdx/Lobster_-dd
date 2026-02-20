@echo off
REM LobsterAI Bot 守护进程开机启动配置

echo ========================================
echo   LobsterAI Bot 守护进程开机启动配置
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

set "SCRIPT_DIR=%~dp0"
set "DAEMON_SCRIPT=%SCRIPT_DIR%bot_daemon.py"
set "WORK_DIR=%SCRIPT_DIR%"

echo [1/2] 配置开机启动任务（守护进程版本）...
echo.

REM 删除旧任务
schtasks /delete /tn "LobsterAI_Bot_Daemon" /f >nul 2>&1

REM 创建新任务 - 使用守护进程
schtasks /create /tn "LobsterAI_Bot_Daemon" /tr "python \"%DAEMON_SCRIPT%\"" /sc onstart /ru "SYSTEM" /rl highest /f

if %errorlevel% neq 0 (
    echo [错误] 任务创建失败
    pause
    exit /b 1
)

echo [2/2] 验证配置...
schtasks /query /tn "LobsterAI_Bot_Daemon" /fo list | findstr "状态"

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo 守护进程已配置为开机自动启动。
echo.
echo 任务信息:
echo   - 任务名称: LobsterAI_Bot_Daemon
echo   - 触发器: 系统启动时
echo   - 运行身份: SYSTEM
echo   - 脚本: bot_daemon.py (自动重启 Bot)
echo.
echo 管理命令:
echo   查看任务: schtasks /query /tn "LobsterAI_Bot_Daemon"
echo   手动运行: schtasks /run /tn "LobsterAI_Bot_Daemon"
echo   禁用任务: schtasks /disable /tn "LobsterAI_Bot_Daemon"
echo   启用任务: schtasks /enable /tn "LobsterAI_Bot_Daemon"
echo   删除任务: schtasks /delete /tn "LobsterAI_Bot_Daemon" /f
echo.
echo 日志文件:
echo   - Bot 日志: telegram_bot.log
echo   - 守护进程日志: bot_daemon.log
echo.

pause
