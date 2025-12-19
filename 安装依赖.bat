@echo off
chcp 65001 >nul
echo ========================================
echo 供应链物料时间差距分析工具 - 依赖安装
echo ========================================
echo.
echo 正在检查Python环境...
python --version
if errorlevel 1 (
    echo.
    echo [错误] 未检测到Python
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo ========================================
echo 开始安装依赖库...
echo ========================================
echo.

echo 升级pip到最新版本...
python -m pip install --upgrade pip
echo.

echo 尝试使用清华镜像源安装所有依赖...
python -m pip install streamlit pandas numpy plotly openpyxl xlrd -i https://pypi.tuna.tsinghua.edu.cn/simple

if errorlevel 1 (
    echo.
    echo 清华源失败，尝试使用阿里云镜像源...
    python -m pip install streamlit pandas numpy plotly openpyxl xlrd -i https://mirrors.aliyun.com/pypi/simple/
    
    if errorlevel 1 (
        echo.
        echo 阿里云源失败，尝试使用官方源...
        python -m pip install streamlit pandas numpy plotly openpyxl xlrd
        
        if errorlevel 1 (
            echo.
            echo [错误] 依赖安装失败！
            echo 请检查网络连接或手动安装
            pause
            exit /b 1
        )
    )
)

echo.
echo ========================================
echo 依赖库安装完成！
echo ========================================
echo.
echo 正在验证安装...
python -c "import streamlit, pandas, numpy, plotly, openpyxl" 2>nul
if errorlevel 1 (
    echo [警告] 部分库可能未正确安装
    echo 请运行"测试安装.bat"检查详细情况
) else (
    echo [成功] 所有依赖库已正确安装！
)
echo.
echo 您现在可以双击"启动程序.bat"来运行应用
echo.
pause
