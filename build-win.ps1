# 1. PyInstaller로 실행 파일 빌드
$pyinstallerPath = ".\venv\Scripts\pyinstaller.exe"
Write-Host "Building executable with PyInstaller..." -ForegroundColor Cyan
.\venv\Scripts\pyinstaller.exe -y CaptureMacro-win.spec

# 2. 빌드가 성공했는지 확인
if ($LASTEXITCODE -ne 0) {
    Write-Host "PyInstaller build failed. Exiting." -ForegroundColor Red
    exit $LASTEXITCODE
}

# 3. 현재 버전 가져오기
$versionFile = ".\.version"
$version = Get-Content $versionFile -Raw
$version = $version.Trim()
Write-Host "Current build version: $version" -ForegroundColor Green

# 4. Inno Setup으로 인스톨러 빌드
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
Write-Host "Building installer with Inno Setup..." -ForegroundColor Cyan

if (Test-Path $innoSetupPath) {
    & $innoSetupPath "windows-installer.iss"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Inno Setup build failed. Exiting." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    
    # 인스톨러 파일 확인
    $installerFile = ".\dist\CaptureMacro-$version.exe"
    if (Test-Path $installerFile) {
        Write-Host "Installer build completed: $installerFile" -ForegroundColor Green
    } else {
        Write-Host "Installer file not found: $installerFile" -ForegroundColor Yellow
    }
} else {
    Write-Host "Inno Setup not found: $innoSetupPath" -ForegroundColor Red
    Write-Host "Please make sure Inno Setup is installed." -ForegroundColor Red
    exit 1
}

Write-Host "Build process completed successfully." -ForegroundColor Green

