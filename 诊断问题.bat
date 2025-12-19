@echo off
chcp 65001 >nul
echo ========================================
echo 供应链分析工具 - 问题诊断
echo ========================================
echo.

echo [步骤1] 检查Python环境...
python --version
if errorlevel 1 (
    echo [失败] Python未安装或未添加到PATH
    echo 请安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [成功] Python已安装
echo.

echo [步骤2] 检查依赖库...
echo 检查 streamlit...
python -c "import streamlit; print('streamlit版本:', streamlit.__version__)" 2>nul
if errorlevel 1 (
    echo [失败] streamlit未安装
    echo 正在尝试安装...
    python -m pip install streamlit
)

echo 检查 pandas...
python -c "import pandas; print('pandas版本:', pandas.__version__)" 2>nul
if errorlevel 1 (
    echo [失败] pandas未安装
    echo 正在尝试安装...
    python -m pip install pandas
)

echo 检查 plotly...
python -c "import plotly; print('plotly版本:', plotly.__version__)" 2>nul
if errorlevel 1 (
    echo [失败] plotly未安装
    echo 正在尝试安装...
    python -m pip install plotly
)
echo.

echo [步骤3] 检查app.py文件...
if exist app.py (
    echo [成功] app.py文件存在
) else (
    echo [失败] app.py文件不存在
    echo 请确保在正确的目录中运行此脚本
    pause
    exit /b 1
)
echo.

echo [步骤4] 测试运行Streamlit...
echo 正在尝试启动Streamlit（5秒后自动关闭）...
timeout /t 2 >nul
start /b python -m streamlit run app.py --server.headless=true
timeout /t 5 >nul
taskkill /f /im python.exe >nul 2>&1
echo.

echo ========================================
echo 诊断完成
echo ========================================
echo.
echo 如果所有检查都通过，请尝试：
echo 1. 双击"启动程序.bat"
echo 2. 或手动运行: streamlit run app.py
echo.
echo 如果仍有问题，请查看上方的错误信息
echo.
pause
