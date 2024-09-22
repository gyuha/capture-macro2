.\venv\Scripts\pyinstaller.exe  -y CaptureMacro-win.spec

# .version 파일에서 버전 정보를 읽습니다.
$versionFilePath = ".version"
$version = Get-Content $versionFilePath

# windows-installer.iss 파일 경로
$issFilePath = ".\windows-installer.iss"

# windows-installer.iss 파일의 내용을 읽습니다.
$issContent = Get-Content $issFilePath

# #define MyAppVersion 줄을 찾아서 업데이트합니다.
$pattern = '#define MyAppVersion\s+"(\d+\.\d+\.\d+)"'
$replacement = "#define MyAppVersion `"$version`""
$updatedContent = $issContent -replace $pattern, $replacement

# 업데이트된 내용을 windows-installer.iss 파일에 씁니다.
Set-Content $issFilePath -Value $updatedContent

Write-Output "Updated MyAppVersion to $version in $issFilePath"