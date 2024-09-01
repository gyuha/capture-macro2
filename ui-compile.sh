#!/bin/bash

# ui 폴더 경로 설정
UI_DIR="ui"

# ui 폴더가 존재하는지 확인
if [ ! -d "$UI_DIR" ]; then
    echo "Error: '$UI_DIR' 폴더를 찾을 수 없습니다."
    exit 1
fi

# ui 폴더 내의 모든 .ui 파일에 대해 반복
for ui_file in "$UI_DIR"/*.ui; do
    # 파일이 존재하는지 확인
    if [ -f "$ui_file" ]; then
        # 파일 이름에서 확장자를 제거하고 _ui.py를 추가
        py_file="${ui_file%.ui}_ui.py"

        echo "Converting $ui_file to $py_file"

        # pyuic6를 사용하여 .ui 파일을 .py 파일로 변환
        ./venv/bin/pyside6-uic "$ui_file" -o "$py_file"

        if [ $? -eq 0 ]; then
            echo "Successfully converted $ui_file"
        else
            echo "Error converting $ui_file"
        fi
    fi
done

echo "Conversion complete."
