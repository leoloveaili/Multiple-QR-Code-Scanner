@echo off
echo Starting QR Scanner...
echo.

REM 激活Python虚拟环境
call .\venv\Scripts\activate.bat

REM 运行Python程序
python run.py

REM 如果发生错误，暂停以查看错误信息
if errorlevel 1 (
    echo.
    echo An error occurred! Press any key to exit...
    pause > nul
)

REM 停用虚拟环境
deactivate 