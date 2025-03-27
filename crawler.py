import requests
from bs4 import BeautifulSoup

def get_boj_problem(problem_number):
    """
    BOJ 문제 번호를 받아 해당 문제의 정보를 크롤링하여 JSON 형식(dict)으로 반환합니다.

    Parameters:
        problem_number (int): 백준 문제 번호

    Returns:
        dict or None: 문제 정보 또는 실패 시 None
    """
    url = f"https://www.acmicpc.net/problem/{problem_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Failed to fetch problem {problem_number} (status code: {response.status_code})")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # 문제 설명, 입력, 출력 설명 가져오기
    problem_desc = " ".join([p.text.strip() for p in soup.select("#problem_description p")])
    input_desc = " ".join([p.text.strip() for p in soup.select("#problem_input p")])
    output_desc = " ".join([p.text.strip() for p in soup.select("#problem_output p")])

    # 예시 입력/출력 가져오기
    example_inputs = {f"sampleinput{i}": pre.text.strip() for i, pre in enumerate(soup.select("section[id^=sampleinput] pre"), start=1)}
    example_outputs = {f"sampleoutput{i}": pre.text.strip() for i, pre in enumerate(soup.select("section[id^=sampleoutput] pre"), start=1)}

    return {
        "problem_number": problem_number,
        "description": problem_desc,
        "input_description": input_desc,
        "output_description": output_desc,
        "example_inputs": example_inputs,
        "example_outputs": example_outputs
    }
