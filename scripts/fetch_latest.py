import json
import re
import sys
import requests
from bs4 import BeautifulSoup

def fetch_lottery_data():
    """
    Fetches lottery data from Naver Search results.
    
    HISTORY / CONTEXT:
    1. **Direct Request (dhlottery.co.kr)**: Originally attempted to scrape the official website using `requests`.
       FAILED: The site is protected by NetFunnel and other blocking mechanisms, returning a waiting page instead of content.
       
    2. **Headless Browser (Playwright)**: Attempted to use Playwright to bypass NetFunnel by waiting for the queue.
       FAILED: Even with a 90-second timeout, the NetFunnel queue often persisted or the page structure was difficult to reliably interact with in a headless environment.
       
    3. **Naver Search Scraping (Current Solution)**: 
       We switched to scraping Naver's search results for "로또당첨번호". 
       - Pros: Fast, no NetFunnel blocking, simple HTML structure.
       - Cons: Dependent on Naver's search result layout remaining consistent.
    """
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%A1%9C%EB%98%90%EB%8B%B9%EC%B2%A8%EB%B2%88%ED%98%B8"
    
    print(f"Fetching data from Naver Search: {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.naver.com/"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract Draw Number
    # Found in: <a class="text _select_trigger _text" ...>1210회차 (2026.02.07.)</a>
    draw_no_element = soup.select_one("._select_trigger._text")
    if not draw_no_element:
        raise ValueError("Could not find draw number element on Naver page.")
        
    draw_text = draw_no_element.get_text()
    draw_number = re.search(r"(\d+)회차", draw_text)
    if not draw_number:
        raise ValueError(f"Could not parse draw number from text: {draw_text}")
    
    draw_number = draw_number.group(1)
    print(f"Found Draw Number: {draw_number}")

    # Extract Winning Numbers & Bonus
    # Found in: <span class="ball ...">1</span>
    # Assuming the first 6 are winning numbers and the 7th is bonus
    balls = soup.select(".ball")
    if len(balls) < 7:
        raise ValueError(f"Found fewer than 7 balls: {len(balls)}")
        
    numbers = [int(b.get_text()) for b in balls]
    winning_numbers = numbers[:6]
    bonus_number = numbers[6]
    
    print(f"Winning Numbers: {winning_numbers}")
    print(f"Bonus Number: {bonus_number}")
    
    return draw_number, winning_numbers, bonus_number


def validate_lottery_data(draw_number, winning_numbers, bonus_number):
    if not draw_number.isdigit():
        raise ValueError("회차 번호가 숫자가 아닙니다.")

    if not isinstance(winning_numbers, list) or len(winning_numbers) != 6:
        raise ValueError("당첨 번호가 6개의 숫자로 구성된 배열이 아닙니다.")

    for num in winning_numbers:
        if not isinstance(num, int) or num < 1 or num > 45:
            raise ValueError("당첨 번호에 유효하지 않은 숫자가 포함되어 있습니다.")

    if not isinstance(bonus_number, int) or bonus_number < 1 or bonus_number > 45:
        raise ValueError("보너스 번호가 유효한 숫자가 아닙니다.")


def save_lottery_result(result, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    try:
        draw_number, winning_numbers, bonus_number = fetch_lottery_data()
        validate_lottery_data(draw_number, winning_numbers, bonus_number)

        result = {
            "draw_number": draw_number,
            "winning_numbers": winning_numbers,
            "bonus_number": bonus_number,
        }

        save_lottery_result(result, "data/latest_lottery_result.json")
        print(f"최신 로또 결과 (회차 {draw_number})가 저장되었습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
