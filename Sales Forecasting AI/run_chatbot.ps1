#!/usr/bin/env powershell
# Sales Forecasting AI Chatbot Startup Script

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Sales Forecasting AI Chatbot" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

function Test-PythonCmd {
    param([string]$Cmd)
    try {
        & $Cmd --version 2>&1 | Out-Null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Test-Module {
    param([string]$Cmd, [string]$Module)
    try {
        & $Cmd -c "import $Module" 2>&1 | Out-Null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Prefer venv if it has uvicorn; otherwise use system Python
$pythonCmd = "python"
$venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    if (Test-Module $venvPython "uvicorn") {
        $pythonCmd = $venvPython
        Write-Host "[+] Using virtual environment" -ForegroundColor Green
    } else {
        Write-Host "[!] Virtual env missing uvicorn — using system Python" -ForegroundColor Yellow
    }
}

if (-not (Test-PythonCmd $pythonCmd)) {
    Write-Host "[-] ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install from https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

$version = & $pythonCmd --version 2>&1
Write-Host "[+] Python: $version" -ForegroundColor Green

if (-not (Test-Module $pythonCmd "uvicorn")) {
    Write-Host ""
    Write-Host "[1/2] Installing server packages (fastapi, uvicorn)..." -ForegroundColor Yellow
    & $pythonCmd -m pip install fastapi "uvicorn[standard]" python-multipart --quiet
    if (-not (Test-Module $pythonCmd "uvicorn")) {
        Write-Host "[-] ERROR: Could not install uvicorn. Check your internet connection." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[+] Server packages installed" -ForegroundColor Green
} else {
    Write-Host "[+] uvicorn ready" -ForegroundColor Green
}

if (-not (Test-Module $pythonCmd "pandas")) {
    Write-Host ""
    Write-Host "[!] pandas not found — run when online:" -ForegroundColor Yellow
    Write-Host "    $pythonCmd -m pip install -r requirements.txt" -ForegroundColor White
}

Write-Host ""
Write-Host "[2/2] Starting server (first start may take ~1 min on OneDrive)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Open in your browser:" -ForegroundColor Cyan
Write-Host "    http://127.0.0.1:8000" -ForegroundColor White
Write-Host "    http://127.0.0.1:8000/static/index.html" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""

Set-Location $PSScriptRoot
& $pythonCmd -m uvicorn chatbot_backend:app --host 127.0.0.1 --port 8000
