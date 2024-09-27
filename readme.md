# gksdud 
#### 한글/영어 키보드 입력 전환기

gksdud는 한글과 영어 키보드 입력을 빠르게 전환할 수 있는 macOS용 애플리케이션입니다.

## 기능

- 시스템 트레이에 상주하여 간편하게 사용
- 단축키를 통한 빠른 텍스트 선택 및 변환
- 한글을 영어 키보드 입력으로, 영어 키보드 입력을 한글로 변환

## 설치 방법

1. 최신 릴리즈에서 `gksdud.app`을 다운로드합니다.
2. 다운로드한 `gksdud.app`을 응용 프로그램 폴더로 이동합니다.

## 사용 방법

1. `gksdud` 앱을 실행합니다.
2. 변환하고 싶은 텍스트 블록을 선택합니다.
3. 다시 `Ctrl + Shift + L`을 눌러 선택된 텍스트를 변환합니다.

## 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/yourusername/gksdud.git
cd gksdud

# 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 빌드 방법

```bash
pyinstaller --onefile --windowed --icon=icon.icns --name "gksdud" --add-data "icon.png:." --add-data "converter.py:." app.py
```

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다. 기여하기 전에 프로젝트의 기여 가이드라인을 확인해주세요.