# gksdud [1.2.0]

![gksdud logo](assets/icon.png)

### 한글/영어 키보드 입력 전환기

gksdud는 macOS 환경에서 한글과 영어 키보드 입력을 빠르고 편리하게 전환할 수 있는 애플리케이션입니다.

![Demo](assets/test.gif)

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

2. 설치 스크립트를 실행합니다:
   ```
   chmod +x gksdud.sh
   ./gksdud.sh
   ```

   이 스크립트는 가상 환경을 생성하고, 필요한 의존성을 설치한 후 애플리케이션을 실행합니다.

## 사용 방법

1. 변환하고 싶은 텍스트를 선택합니다.

2. `Ctrl + Shift + L`을 누릅니다. 선택한 텍스트와 변환될 내용이 툴팁으로 표시됩니다.

3. 변환을 원하면 다시 `Ctrl + Shift + L`을 누릅니다. 선택한 텍스트가 변환되어 붙여넣어집니다.

## 주요 파일 설명

- `main.py`: 메인 애플리케이션 파일
- `modules/converter.py`: 한글-영어 변환 로직이 구현된 파일
- `assets/icon.png`: 시스템 트레이 아이콘 파일
- `gksdud.sh`: 설치 및 실행 스크립트

## 개발 환경 설정

개발에 참여하고 싶으시다면 다음 단계를 따라주세요:

```bash
# 저장소 클론
git clone https://github.com/DaeJongLee/gksdud.git
cd gksdud

# 가상 환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

## 주의사항

- macOS 환경에서 개발 및 테스트되었습니다.
- 일부 애플리케이션에서는 보안 설정으로 인해 작동하지 않을 수 있습니다.
- 처음 실행 시 접근성 권한을 요구할 수 있습니다.

## To-Do List

- [ ] Windows 지원
- [ ] Linux 지원 
- [ ] 키보드 매핑 기능 추가
- [ ] 혼합 컨버팅 기능 추가
- [ ] 단축키 변경 기능 추가 
- [ ] 프로그램 종료 기능 추가
- [ ] 접근성 도우미 추가 

## 기여

버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다. 기여하기 전에 프로젝트의 기여 가이드라인을 확인해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

프로젝트 관리자: DAE JONG LEE
GitHub: [https://github.com/daejonglee](https://github.com/daejonglee)