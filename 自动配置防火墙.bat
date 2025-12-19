@echo off
chcp 65001 >nul
color 0B
echo ========================================
echo 自动配置Windows防火墙
echo ========================================
echo.
echo 此脚本将自动为Streamlit应用配置防火墙规则
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    color 0C
    echo [错误] 需要管理员权限！
    echo.
    echo 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [成功] 已获得管理员权限
echo.

echo [步骤1/3] 删除可能存在的旧规则...
netsh advfirewall firewall delete rule name="Streamlit应用-TCP8501" >nul 2>&1
netsh advfirewall firewall delete rule name="Python-Streamlit" >nul 2>&1
echo [完成]
echo.

echo [步骤2/3] 创建新的防火墙规则（端口8501）...
netsh advfirewall firewall add rule name="Streamlit应用-TCP8501" dir=in action=allow protocol=TCP localport=8501
if errorlevel 1 (
    color 0E
    echo [警告] 端口规则创建可能失败
) else (
    echo [成功] 端口8501已允许通过防火墙
)
echo.

echo [步骤3/3] 查找并添加Python.exe到防火墙...
where python >nul 2>&1
if errorlevel 1 (
    echo [警告] 未找到Python，跳过此步骤
) else (
    for /f "tokens=*" %%i in ('where python') do (
        echo 正在添加: %%i
        netsh advfirewall firewall add rule name="Python-Streamlit" dir=in action=allow program="%%i" enable=yes
        goto :found
    )
    :found
    echo [成功] Python已添加到防火墙
)
echo.

echo ========================================
echo 防火墙配置完成！
echo ========================================
echo.
echo 已创建的规则：
echo 1. 允许TCP端口8501的入站连接
echo 2. 允许Python程序通过防火墙
echo.
echo 现在可以尝试运行程序了！
echo 双击"一键解决并启动.bat"启动应用
echo.
pause
