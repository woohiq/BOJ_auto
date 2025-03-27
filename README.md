# ※ 이 텍스트와 프로그램은 AI의 도움을 받아 작성하였습니다.
이 파일의 실행 결과는 백준 페이지의 정답을 보장하지 않으며, 개인의 설정 및 백준 홈페이지의 변경 따라 코드가 작동되지 않을 수 있습니다.

# BOJ Auto Solver & Submitter 🤖

이 프로젝트는 [백준 온라인 저지](https://www.acmicpc.net)의 문제를 자동으로 크롤링하고, OpenAI GPT 모델을 사용하여 파이썬 풀이 코드를 생성한 뒤, 자동으로 백준에 제출하는 프로그램입니다.

## 🧠 주요 기능

- ✅ 백준 문제 실시간 크롤링
- 🤖 GPT를 이용한 파이썬 코드 자동 생성
- 🖱️ Selenium을 활용한 자동 제출
- 🛠️ 환경변수 기반 유연한 설정

## 📁 파일 설명

| 파일명       | 설명 |
|--------------|------|
| `crawler.py` | 문제 정보를 실시간으로 크롤링하는 모듈 |
| `submit.py`  | 백준 로그인 → GPT 코드 생성 → 제출 자동화 |
| `.env`       | 사용자 ID, PW, API 키, 문제 범위 저장 |
| `requirements.txt` | 설치해야 할 패키지 목록 |

## ⚙️ 사전 준비

1. **Python 3.8 이상 설치**
2. **Google Chrome 설치**
3. `.env` 파일 생성 후 아래 정보 추가:

```
ID=your_boj_id
PW=your_boj_password
openAI_KEY=your_openai_api_key
BOJ_PROBLEM_START=1001
BOJ_PROBLEM_END=1103
```

> `BOJ_PROBLEM_START`와 `BOJ_PROBLEM_END`는 자동 제출할 문제 번호 범위입니다.

## 🛠️ 설치 및 실행 방법

```bash
# 1. 가상 환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # 윈도우는 venv\Scripts\activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 자동 제출 실행
python submit.py
```

## ⚠️ 주의 사항

- 백준 계정은 자동화 방지를 위해 자동 제출을 제한할 수 있습니다.
- GPT 모델로 생성된 코드는 정답이 아닐 수 있습니다. 신뢰성은 보장되지 않습니다.
- 5초 간격 제출 등 백준의 규정을 준수해야 합니다.

## 📜 라이선스

MIT License