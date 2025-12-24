# 快速启动脚本（Windows PowerShell）

Write-Host "============================================" -ForegroundColor Green
Write-Host "  网上商城系统 - 快速启动" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

# 检查Python版本
Write-Host "[1/5] 检查Python环境..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未检测到Python，请先安装Python 3.9+" -ForegroundColor Red
    exit 1
}

# 检查MySQL
Write-Host ""
Write-Host "[2/5] 检查MySQL服务..." -ForegroundColor Cyan
$mysqlService = Get-Service -Name MySQL* -ErrorAction SilentlyContinue
if ($mysqlService) {
    Write-Host "✓ MySQL服务已安装" -ForegroundColor Green
    if ($mysqlService.Status -eq 'Running') {
        Write-Host "✓ MySQL服务正在运行" -ForegroundColor Green
    } else {
        Write-Host "⚠ MySQL服务未运行，请手动启动" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ 未检测到MySQL服务，请确保MySQL已安装并运行" -ForegroundColor Yellow
}

# 安装依赖
Write-Host ""
Write-Host "[3/5] 安装Python依赖..." -ForegroundColor Cyan
Set-Location backend
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 依赖安装成功" -ForegroundColor Green
    } else {
        Write-Host "✗ 依赖安装失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ 未找到requirements.txt" -ForegroundColor Red
    exit 1
}

# 初始化数据库提示
Write-Host ""
Write-Host "[4/5] 数据库初始化" -ForegroundColor Cyan
Write-Host "请手动执行以下SQL脚本初始化数据库：" -ForegroundColor Yellow
Write-Host "  1. mysql -u root -p" -ForegroundColor White
Write-Host "  2. source ../database/schema.sql" -ForegroundColor White
Write-Host "  3. source ../database/seed_data.sql" -ForegroundColor White
Write-Host ""
$continue = Read-Host "已完成数据库初始化？(Y/N)"
if ($continue -ne "Y" -and $continue -ne "y") {
    Write-Host "请先初始化数据库后再启动服务" -ForegroundColor Yellow
    exit 0
}

# 启动后端服务
Write-Host ""
Write-Host "[5/5] 启动后端服务..." -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  服务启动信息" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "后端地址: http://localhost:8000" -ForegroundColor White
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor White
Write-Host "测试账号:" -ForegroundColor White
Write-Host "  买家: zhang_san / password123" -ForegroundColor White
Write-Host "  商家: 数码专营店 / merchant123" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

python main.py
