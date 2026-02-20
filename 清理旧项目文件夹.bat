@echo off
chcp 65001 >nul
echo ========================================
echo 小d - 清理旧项目文件夹
echo ========================================
echo.
echo 正在删除旧项目文件夹...
echo 路径: C:\Users\Administrator\lobsterai\project
echo.

REM 等待2秒，确保文件不被占用
timeout /t 2 >nul

REM 尝试删除旧文件夹
if exist "C:\Users\Administrator\lobsterai\project" (
    rd /s /q "C:\Users\Administrator\lobsterai\project" 2>nul
    if %errorlevel% equ 0 (
        echo ✓ 旧项目文件夹已成功删除
    ) else (
        echo ✗ 删除失败，文件夹可能仍被占用
        echo 提示: 请关闭所有相关程序后重试
    )
) else (
    echo ✓ 旧项目文件夹不存在，无需删除
)

echo.
echo ========================================
echo 新工作区: E:\实例\DD_project
echo ========================================
echo.
timeout /t 3
