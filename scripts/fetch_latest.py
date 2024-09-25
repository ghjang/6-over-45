import requests
from bs4 import BeautifulSoup
import json
import re


def fetch_lottery_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 최신 회차 번호 추출 및 숫자만 추출
    draw_number_raw = soup.select_one(".win_result h4 strong").text.strip()
    draw_number = re.search(r"\d+", draw_number_raw).group()  # 숫자만 추출

    # 당첨 번호 추출
    winning_numbers = [int(num.text) for num in soup.select(".win .ball_645")]
    bonus_number = int(soup.select_one(".bonus .ball_645").text)

    return draw_number, winning_numbers, bonus_number


def validate_lottery_data(draw_number, winning_numbers, bonus_number):
    # 1. draw_number가 숫자인지 확인
    if not draw_number.isdigit():
        raise ValueError("회차 번호가 숫자가 아닙니다.")

    # 2. winning_numbers의 값이 배열이고 딱 6개의 숫자인지 확인
    if not isinstance(winning_numbers, list) or len(winning_numbers) != 6:
        raise ValueError("당첨 번호가 6개의 숫자로 구성된 배열이 아닙니다.")

    for num in winning_numbers:
        if not isinstance(num, int) or num < 1 or num > 45:
            raise ValueError("당첨 번호에 유효하지 않은 숫자가 포함되어 있습니다.")

    # 3. bonus_number가 숫자인지 확인
    if not isinstance(bonus_number, int) or bonus_number < 1 or bonus_number > 45:
        raise ValueError("보너스 번호가 유효한 숫자가 아닙니다.")


def save_lottery_result(result, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    url = "https://dhlottery.co.kr/gameResult.do?method=byWin"

    try:
        draw_number, winning_numbers, bonus_number = fetch_lottery_data(url)
        validate_lottery_data(draw_number, winning_numbers, bonus_number)

        result = {
            "draw_number": draw_number,
            "winning_numbers": winning_numbers,
            "bonus_number": bonus_number,
        }

        save_lottery_result(result, "data/latest_lottery_result.json")
        print(f"최신 로또 결과 (회차 {draw_number})가 저장되었습니다.")

    except ValueError as e:
        print(f"오류 발생: {e}")
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")


if __name__ == "__main__":
    main()
