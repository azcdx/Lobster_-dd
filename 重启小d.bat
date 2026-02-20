@echo off
chcp 65001 >nul
echo ========================================
echo 小d - 重启脚本
echo ========================================
echo.
echo 此脚本将:
echo 1. 清理旧项目文件夹
echo 2. 重启 LobsterAI
echo.

pause

REM 执行清理
call "%~dp0清理旧项目文件夹.bat"

REM 提示用户手动重启
echo.
echo ========================================
echo 请手动重启 LobsterAI 应用
echo ========================================
echo.
echo 重启后，小d将在新工作区工作:
echo E:\实例\DD_project
echo.
pause
