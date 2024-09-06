#!/bin/bash

# 변수 설정
APP_NAME="CaptureMacro"
SPEC_FILE="CaptureMacro.spec"
ICON_FILE="resources/icon.icns"  # 아이콘 파일 경로를 지정하세요
DMG_BACKGROUND="resources/background.png"  # DMG 배경 이미지 경로를 지정하세요
VERSION_FILE=".version"

# 버전 파일에서 버전 정보 읽기
if [ -f "$VERSION_FILE" ]; then
    VERSION=$(head -n 1 "$VERSION_FILE")
else
    echo "Error: Version file not found. Please create a .version file with the version number in the first line."
    exit 1
fi

echo "Building version: $VERSION"

# PyInstaller를 사용하여 앱 빌드
echo "Building the app with PyInstaller..."
pyinstaller -y "$SPEC_FILE"

# 앱 번들 경로
APP_BUNDLE="dist/$APP_NAME.app"

# 아이콘 파일 복사 (필요한 경우)
if [ -f "$ICON_FILE" ]; then
    echo "Copying icon file..."
    cp "$ICON_FILE" "$APP_BUNDLE/Contents/Resources/"
fi

# DMG 생성
echo "Creating DMG..."

# DMG 파일 이름 및 경로 설정
DMG_NAME="${APP_NAME}-${VERSION}.dmg"
DMG_PATH="dist/${DMG_NAME}"
TMP_DMG_PATH="dist/${APP_NAME}-tmp.dmg"

# 임시 DMG 생성
hdiutil create -srcfolder "$APP_BUNDLE" -volname "$APP_NAME $VERSION" -fs HFS+ \
        -fsargs "-c c=64,a=16,e=16" -format UDRW -size 200m "$TMP_DMG_PATH"

# 임시 DMG를 마운트
MOUNT_DIR="/Volumes/$APP_NAME $VERSION"
hdiutil attach -readwrite -noverify -noautoopen "$TMP_DMG_PATH"

# 볼륨 아이콘 설정 (선택사항)
# cp /path/to/volume_icon.icns "$MOUNT_DIR/.VolumeIcon.icns"
# SetFile -c icnC "$MOUNT_DIR/.VolumeIcon.icns"

# 응용 프로그램 폴더로의 심볼릭 링크 생성
ln -s /Applications "$MOUNT_DIR/Applications"

# DMG 최종화
hdiutil detach "$MOUNT_DIR"
hdiutil convert "$TMP_DMG_PATH" -format UDZO -o "$DMG_PATH"
rm -f "$TMP_DMG_PATH"

echo "DMG creation complete: $DMG_PATH"

