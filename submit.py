import time
import os
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import openai

# .env 파일 로드
load_dotenv(".env")
BOJ_ID = os.getenv("ID")
BOJ_PW = os.getenv("PW")
openai.api_key = os.getenv("openAI_KEY")
BOJ_PROBLEM_START = (int) (os.getenv("BOJ_PROBLEM_START"))
BOJ_PROBLEM_END = (int) (os.getenv("BOJ_PROBLEM_END"))

# Chrome 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def boj_login():
    """백준 로그인"""
    driver.get("https://www.acmicpc.net/login")
    time.sleep(2)

    try:
        id_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.NAME, "login_user_id"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", id_input, BOJ_ID)

        pw_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.NAME, "login_password"))
        )
        driver.execute_script("arguments[0].value = arguments[1];", pw_input, BOJ_PW)

        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "submit_button"))
        )
        login_button.click()
        time.sleep(3)

        print("✅ 로그인 성공!")

    except:
        print("⚠️ 이미 로그인되어 있거나 로그인 페이지 접근 불가.")

import crawler  # 모듈 임포트 추가

def generate_code(problem_number):
    """BOJ 문제 설명을 크롤링하고, ChatGPT API를 사용해 자동으로 코드를 생성"""

    try:
        # crawler에서 문제 정보 크롤링
        problem_data = crawler.get_boj_problem(problem_number)
        if not problem_data:
            print(f"⚠️ 문제 {problem_number} 정보를 가져오지 못했습니다.")
            return None

        # 문제 설명 가져오기
        description = problem_data["description"]
        input_description = problem_data["input_description"]
        output_description = problem_data["output_description"]
        example_inputs = problem_data["example_inputs"]
        example_outputs = problem_data["example_outputs"]

        # 예제 입력과 출력 포맷팅
        example_prompt = "\n".join([
            f"입력 예제:\n{inp}\n출력 예제:\n{example_outputs.get(key, '출력 예제 없음')}"
            for key, inp in example_inputs.items()
        ])

        # ChatGPT 프롬프트 (코드만 출력하도록)
        prompt = f"""
        당신은 프로그래머이며, 부연 설명 없이 파이썬 코드만 반환해야 합니다.
        문제를 해결하는 파이썬 코드를 작성하세요.

        문제 설명:
        {description}

        입력 형식:
        {input_description}

        출력 형식:
        {output_description}

        예제 데이터:
        {example_prompt}

        **부연 설명 없이, 코드만 출력하세요.**
        ```python
        """

        # OpenAI API 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful AI coding assistant."},
                      {"role": "user", "content": prompt}]
        )

        # 응답에서 코드만 추출
        generated_code = response["choices"][0]["message"]["content"].strip()

        # ```python 및 ``` 제거
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]

        return generated_code.strip()

    except Exception as e:
        print(f"⚠️ 문제 {problem_number} 처리 중 오류 발생: {e}")
        return None

def submit_solution(problem_number, language):

    # 코드 자동 생성 및 입력
    code = generate_code(problem_number)
    print(code)
    if code:
        """백준 문제 제출"""
        submit_url = f"https://www.acmicpc.net/submit/{problem_number}"
        driver.get(submit_url)
        time.sleep(3)

        try:
            submit_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "제출"))
            )
            submit_tab.click()
            time.sleep(2)
        except:
            print(f"⚠️ 문제 {problem_number} 제출 탭을 찾을 수 없음. 계속 진행.")

        # 언어 선택 (chosen-single)
        try:
            chosen_single = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "chosen-single"))
            )
            chosen_single.click()
            time.sleep(1)

            lang_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{language}')]"))
            )
            lang_option.click()
            time.sleep(1)

        except:
            print(f"⚠️ 문제 {problem_number} 언어 선택 실패.")

        try:
            editor_div = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
            )
            driver.execute_script("arguments[0].CodeMirror.setValue(arguments[1]);", editor_div, code)
            time.sleep(1)
        except:
            print(f"⚠️ 문제 {problem_number} 코드 입력 실패.")

        # 제출 버튼 클릭
        try:
            submit_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "submit_button"))
            )
            submit_button.click()
            time.sleep(5)
            print(f"✅ 문제 {problem_number} 제출 완료!")
        except:
            print(f"⚠️ 문제 {problem_number} 제출 버튼 클릭 실패.")

    else:
        print(f"⚠️ 문제 {problem_number} 자동 코드 생성 실패.")

# 실행
boj_login()

# 문제 번호: 1001 ~ 1103, 5초 간격으로 제출
for problem_number in range(BOJ_PROBLEM_START, BOJ_PROBLEM_END + 1):
    print(f"🚀 문제 {problem_number} 제출 시작")
    submit_solution(problem_number, "Python 3")
    print(f"⏳ 5초 대기 후 다음 문제 진행...")
    time.sleep(5)

# 크롬 종료
driver.quit()