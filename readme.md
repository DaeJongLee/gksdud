<img src="assets/icon.png" alt="simbol">

todo list 
- [ ] win 지원
- [ ] linux 지원 
- [ ] 키보드 매핑 기능 추가
- [ ] 혼합 컨버팅 기능 추가
- [ ] 단축키 변경 기능 추가 

# gksdud 
### 한글/영어 키보드 입력 전환기

#### gksdud는 macOS 환경에서 한글과 영어 키보드 입력을 빠르고 편리하게 전환할 수 있는 애플리케이션입니다.
<img src="assets/test.gif" alt="Testing" width="400">

## 주요 기능

- 시스템 트레이에 상주하여 간편하게 사용
- 단축키를 통한 빠른 텍스트 선택 및 변환
- 한글을 영어 키보드 입력으로, 영어 키보드 입력을 한글로 변환
- 변환 전 미리보기 기능 제공

## 설치 방법

1. 저장소를 클론합니다:
   ```
   git clone https://github.com/DaeJongLee/gksdud.git
   cd gksdud
   ```

2. 가상 환경을 생성하고 활성화합니다:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. 필요한 라이브러리를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 사용 방법

1. 애플리케이션을 실행합니다:
   ```
   python app.py
   ```

2. 변환하고 싶은 텍스트를 선택합니다.

3. `Ctrl + Shift + L`을 누릅니다. 선택한 텍스트와 변환될 내용이 툴팁으로 표시됩니다.

4. 변환을 원하면 다시 `Ctrl + Shift + L`을 누릅니다. 선택한 텍스트가 변환되어 붙여넣어집니다.

## 주요 파일 설명

- `app.py`: 메인 애플리케이션 파일
- `converter.py`: 한글-영어 변환 로직이 구현된 파일
- `icon.png`: 시스템 트레이 아이콘 파일

## 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/yourusername/gksdud.git
cd gksdud

# 가상 환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 실행 스크립트

애플리케이션을 쉽게 실행하기 위해 다음과 같은 쉘 스크립트(`run_gksdud.sh`)를 사용할 수 있습니다:

```bash
#!/bin/bash

# 가상 환경 활성화
source /Users/dj/project-l/gksdud/.venv/bin/activate

# Python 스크립트 실행
python /Users/dj/project-l/gksdud/app.py
```

이 스크립트에 실행 권한을 부여하고 실행하세요:

```bash
chmod +x run_gksdud.sh
./run_gksdud.sh
```

## 주의사항

- macOS 환경에서 개발 및 테스트되었습니다.
- 일부 애플리케이션에서는 보안 설정으로 인해 작동하지 않을 수 있습니다.
- 처음 실행 시 접근성 권한을 요구할 수 있습니다.

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다. 기여하기 전에 프로젝트의 기여 가이드라인을 확인해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.