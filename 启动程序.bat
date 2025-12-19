@echo off
chcp 65001 >nul
echo ========================================
echo 供应链物料时间差距分析工具
echo ========================================
echo.
echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python环境检测成功！
echo.
echo 正在检查依赖库...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 首次运行，正在安装必要的依赖库...
    echo 这可能需要几分钟时间，请耐心等待...
    echo.
    
    echo [1/3] 尝试使用清华镜像源...
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install streamlit pandas numpy plotly openpyxl xlrd -i https://pypi.tuna.tsinghua.edu.cn/simple
    
    if errorlevel 1 (
        echo [2/3] 清华源失败，尝试阿里云镜像源...
        python -m pip install streamlit pandas numpy plotly openpyxl xlrd -i https://mirrors.aliyun.com/pypi/simple/
        
        if errorlevel 1 (
            echo [3/3] 阿里云源失败，尝试官方源...
            python -m pip install streamlit pandas numpy plotly openpyxl xlrd
            
            if errorlevel 1 (
                echo.
                echo [错误] 所有镜像源均安装失败
                echo 请尝试以下解决方案：
                echo 1. 检查网络连接
                echo 2. 手动运行: 安装依赖.bat
                echo 3. 或手动执行: python -m pip install streamlit pandas numpy plotly openpyxl xlrd
                pause
                exit /b 1
            )
        )
    )
    echo.
    echo 依赖库安装完成！
)

echo.
echo ========================================
echo 正在启动应用程序...
echo ========================================
echo.
echo 应用将在浏览器中自动打开
echo 如果没有自动打开，请手动访问: http://localhost:8501
echo.
echo 按 Ctrl+C 可以停止程序
echo ========================================
echo.

python -m streamlit run app.py --server.headless true

pause
