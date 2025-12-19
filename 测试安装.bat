@echo off
chcp 65001 >nul
echo ========================================
echo 测试依赖库安装情况
echo ========================================
echo.

echo 测试 Python...
python --version
echo.

echo 测试 streamlit...
python -c "import streamlit; print('streamlit 版本:', streamlit.__version__)"
if errorlevel 1 (
    echo [失败] streamlit 未安装
) else (
    echo [成功] streamlit 已安装
)
echo.

echo 测试 pandas...
python -c "import pandas; print('pandas 版本:', pandas.__version__)"
if errorlevel 1 (
    echo [失败] pandas 未安装
) else (
    echo [成功] pandas 已安装
)
echo.

echo 测试 numpy...
python -c "import numpy; print('numpy 版本:', numpy.__version__)"
if errorlevel 1 (
    echo [失败] numpy 未安装
) else (
    echo [成功] numpy 已安装
)
echo.

echo 测试 plotly...
python -c "import plotly; print('plotly 版本:', plotly.__version__)"
if errorlevel 1 (
    echo [失败] plotly 未安装
) else (
    echo [成功] plotly 已安装
)
echo.

echo 测试 openpyxl...
python -c "import openpyxl; print('openpyxl 版本:', openpyxl.__version__)"
if errorlevel 1 (
    echo [失败] openpyxl 未安装
) else (
    echo [成功] openpyxl 已安装
)
echo.

echo ========================================
echo 测试完成
echo ========================================
pause
