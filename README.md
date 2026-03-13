# EasyOff

EasyOff는 Windows의 `shutdown` 명령을 직관적인 GUI로 간편하게 사용할 수 있도록 도와주는 유틸리티입니다.

> 예약 종료 프로그램은 시중에 많지만, 지인이 깔끔하게 종료기능만 담은 프로그램을 요청하여 만들게 되었습니다.

## 🚀 주요 기능

- 직관적인 달력 및 시간 선택 UI
- 강제 종료 및 재부팅 옵션 지원
- **예약 감지**: Windows 이벤트 뷰어(Event ID 1074)를 백그라운드에서 조회하여, 프로그램 실행 시 기존 종료 예약 존재 여부를 알림 창 없이 자동으로 감지합니다. 이미 예약이 존재하는 경우, 사용자에게 예약 취소 여부를 묻는 메시지 박스를 띄워 불필요한 예약 중복을 방지합니다.

## 💻 실행 방법

배포된 단일 실행 파일을 통해 설치 없이 바로 사용할 수 있습니다.

1. [Releases](https://github.com/RabeMaster/EasyOff/releases) 페이지에서 최신 `EasyOff.exe`를 다운로드합니다.
2. 다운로드한 파일을 실행하여 원하는 시간을 설정하고 예약을 클릭합니다.

## 🛠️ 빌드 방법

**개발 환경 설정**

- Python 3.14.3
- pip 25.3

1. 저장소를 클론합니다.

```bash
git clone [https://github.com/RabeMaster/EasyOff.git](https://github.com/RabeMaster/EasyOff.git)
cd EasyOff

```

2. 가상 환경을 생성하고 패키지를 설치합니다.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

```

3. PyInstaller를 사용하여 단일 실행 파일(.exe)로 빌드합니다.

```bash
pyinstaller --noconsole --onefile --icon=icon.ico --name="EasyOff" run.py

```

> 빌드가 완료되면 `dist` 폴더 안에 `EasyOff.exe` 파일이 생성됩니다.

## 📄 License

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.
