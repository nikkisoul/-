@echo off
chcp 65001 >nul
color 0A
echo ========================================
echo 供应链物料时间差距分析工具
echo 一键解决并启动
echo ========================================
echo.

echo [步骤1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [错误] 未检测到Python！
    echo.
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    echo 安装时请务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo [成功] Python已安装
python --version
echo.

echo [步骤2/4] 安装依赖库...
echo 这可能需要5-10分钟，请耐心等待...
echo.

python -m pip install --upgrade pip >nul 2>&1

echo 正在安装streamlit...
python -m pip install streamlit --quiet
if errorlevel 1 (
    echo [警告] streamlit安装可能失败，尝试使用镜像源...
    python -m pip install streamlit -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
)

echo 正在安装pandas...
python -m pip install pandas --quiet

echo 正在安装numpy...
python -m pip install numpy --quiet

echo 正在安装plotly...
python -m pip install plotly --quiet

echo 正在安装openpyxl...
python -m pip install openpyxl --quiet

echo 正在安装xlrd...
python -m pip install xlrd --quiet

echo.
echo [成功] 所有依赖库已安装
echo.

echo [步骤3/4] 验证安装...
python -c "import streamlit, pandas, numpy, plotly, openpyxl" 2>nul
if errorlevel 1 (
    color 0E
    echo [警告] 部分库可能未正确安装
    echo 但我们仍然尝试启动程序...
    echo.
) else (
    echo [成功] 所有库验证通过
    echo.
)

echo [步骤4/4] 启动应用程序...
echo.
echo ========================================
echo 重要提示：
echo ========================================
echo 1. 程序启动后会显示网址
echo 2. 浏览器会自动打开（如果没有，请手动访问显示的网址）
echo 3. 如果看到防火墙提示，请点击"允许访问"
echo 4. 按 Ctrl+C 可以停止程序
echo ========================================
echo.
echo 正在启动...
echo.

timeout /t 3 >nul

python -m streamlit run app.py --server.headless true

echo.
echo ========================================
echo 程序已停止
echo ========================================
pause
