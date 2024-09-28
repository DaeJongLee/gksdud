#!/bin/bash

# 스크립트가 있는 디렉토리로 이동
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || exit

# 가상 환경 경로 설정
VENV_PATH=".venv"

# Python이 설치되어 있는지 확인
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3가 설치되어 있지 않습니다. 먼저 Python3를 설치해 주세요."
    exit 1
fi

# 가상 환경이 없으면 생성
if [ ! -d "$VENV_PATH" ]; then
    echo "가상 환경을 생성합니다..."
    python3 -m venv "$VENV_PATH"
fi

# 가상 환경 활성화
source "$VENV_PATH/bin/activate"

# 필요한 패키지가 설치되어 있는지 확인
if ! python -c "import PyQt5" &> /dev/null; then
    echo "필요한 패키지를 설치합니다..."
    pip install -r requirements.txt
else
    echo "필요한 패키지가 이미 설치되어 있습니다."
fi

# 메인 스크립트 실행
echo "gksdud 애플리케이션을 시작합니다..."
echo "3초 후 터미널이 종료되고 애플리케이션이 백그라운드에서 실행됩니다..."
sleep 3

# nohup을 사용하여 백그라운드에서 실행하고 출력을 /dev/null로 리다이렉트
nohup python main.py > /dev/null 2>&1 &

# 가상 환경 비활성화
deactivate

# 터미널 종료
exit