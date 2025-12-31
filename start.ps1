# 网上商城系统 - 全栈快速启动脚本（Windows PowerShell）
# 说明：本脚本将同时启动前端和后端服务

Write-Host "============================================" -ForegroundColor Green
Write-Host "  网上商城系统 - 全栈服务启动" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "项目状态:" -ForegroundColor Cyan
Write-Host "  ✓ 后端系统: 已完成 (22个API接口)" -ForegroundColor Green
Write-Host "  ✓ AI算法: 已完成 (协同过滤+规则引擎)" -ForegroundColor Green
Write-Host "  ✓ 数据库: 已完成 (4表+12索引)" -ForegroundColor Green
Write-Host "  ✓ 前端界面: 已完成 (Vue3+Element Plus+ECharts)" -ForegroundColor Green
Write-Host "  ✓ 文档: 已完成 (完整技术文档)" -ForegroundColor Green
Write-Host ""

# 检查Python版本
Write-Host "[1/7] 检查Python环境..." -ForegroundColor Cyan
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ 未检测到Python，请先安装Python 3.9+" -ForegroundColor Red
    exit 1
}

# 检查MySQL
Write-Host ""
Write-Host "[2/7] 检查MySQL服务..." -ForegroundColor Cyan
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

# 检查Node.js
Write-Host ""
Write-Host "[3/7] 检查Node.js环境..." -ForegroundColor Cyan

# 尝试添加Node.js到PATH（常见安装路径）
$nodePaths = @(
    "C:\Program Files\nodejs",
    "C:\Program Files (x86)\nodejs",
    "$env:LOCALAPPDATA\Programs\nodejs",
    "$env:ProgramFiles\nodejs"
)

foreach ($nodePath in $nodePaths) {
    if (Test-Path $nodePath) {
        if ($env:Path -notlike "*$nodePath*") {
            $env:Path += ";$nodePath"
            Write-Host "✓ 已添加Node.js到PATH: $nodePath" -ForegroundColor Yellow
        }
        break
    }
}

# 检查Node.js是否可用
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v\d+") {
        Write-Host "✓ Node.js已安装: $nodeVersion" -ForegroundColor Green
    } else {
        throw "Node.js未正确配置"
    }
} catch {
    Write-Host "✗ 未检测到Node.js，请先安装Node.js 16+" -ForegroundColor Red
    Write-Host "提示: 如果已安装Node.js但仍报错，请尝试：" -ForegroundColor Yellow
    Write-Host "  1. 退出虚拟环境: deactivate" -ForegroundColor White
    Write-Host "  2. 重新运行脚本" -ForegroundColor White
    Write-Host "  或手动添加: `$env:Path += ';C:\Program Files\nodejs\'" -ForegroundColor White
    exit 1
}

# 安装后端依赖
Write-Host ""
Write-Host "[4/7] 安装后端依赖..." -ForegroundColor Cyan
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

# 安装前端依赖
Write-Host ""
Write-Host "[5/7] 安装前端依赖..." -ForegroundColor Cyan
Set-Location ..
Set-Location frontend
if (Test-Path "package.json") {
    if (-not (Test-Path "node_modules")) {
        Write-Host "正在安装前端依赖，请稍候..." -ForegroundColor Yellow
        try {
            npm install 2>&1 | Out-Null
            if (Test-Path "node_modules") {
                Write-Host "✓ 前端依赖安装成功" -ForegroundColor Green
            } else {
                throw "npm install执行失败"
            }
        } catch {
            Write-Host "✗ 前端依赖安装失败: $_" -ForegroundColor Red
            Write-Host "提示: 请确认npm命令可用" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "✓ 前端依赖已安装" -ForegroundColor Green
    }
} else {
    Write-Host "✗ 未找到package.json" -ForegroundColor Red
    exit 1
}
Set-Location ..

# 初始化数据库提示
Write-Host ""
Write-Host "[6/7] 数据库初始化" -ForegroundColor Cyan
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

# 启动服务
Write-Host ""
Write-Host "[7/7] 启动前后端服务..." -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  服务信息" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host "后端API: http://localhost:8000" -ForegroundColor White
Write-Host "API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "前端页面: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "测试账号:" -ForegroundColor Yellow
Write-Host "  买家: zhang_san / password123" -ForegroundColor White
Write-Host "  商家: 数码专营店 / merchant123" -ForegroundColor White
Write-Host ""
Write-Host "功能说明:" -ForegroundColor Yellow
Write-Host "  • 买家端: 商品浏览、AI推荐、订单管理" -ForegroundColor White
Write-Host "  • 商家端: 数据看板、AI建议、商品管理" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "正在启动服务，请稍候..." -ForegroundColor Yellow
Write-Host "提示: 按 Ctrl+C 停止所有服务" -ForegroundColor Gray
Write-Host ""

# 启动后端服务（后台运行）
Set-Location backend
$backendJob = Start-Job -ScriptBlock {
    param($path)
    Set-Location $path
    python main.py
} -ArgumentList (Get-Location).Path

Write-Host "✓ 后端服务已启动 (端口: 8000)" -ForegroundColor Green

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端服务（前台运行）
Set-Location ..
Set-Location frontend
Write-Host "✓ 前端服务启动中 (端口: 5173)" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  🎉 系统已启动！请访问前端页面" -ForegroundColor Green
Write-Host "  前端地址: http://localhost:5173" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

try {
    npm run dev
} finally {
    # 清理后端进程
    Write-Host ""
    Write-Host "正在停止后端服务..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob
    Remove-Job -Job $backendJob
    Write-Host "✓ 所有服务已停止" -ForegroundColor Green
}
