import json
import random

# 파일 경로 상수 정의
FREQUENCY_FILE_PATH = "data/frequency.json"
NEXT_GUESS_FILE_PATH = "data/next_guess.json"

# frequency.json 파일 읽기
with open(FREQUENCY_FILE_PATH, "r", encoding="utf-8") as f:
    frequency_data = json.load(f)

# 최근 회차의 당첨번호와 보너스 번호 정보 가져오기
recent_draws = frequency_data["recent_draws"]

# 누적 빈도수 정보 업데이트
for draw in recent_draws.values():
    winning_numbers = draw["winning_numbers"]
    bonus_number = draw["bonus_number"]

    for number in winning_numbers:
        frequency_data["cumulative_stats"]["frequency_with_bonus"][number - 1] += 1

    frequency_data["cumulative_stats"]["frequency_with_bonus"][bonus_number - 1] += 1

# 빈도수 정보 가져오기
frequency_with_bonus = frequency_data["cumulative_stats"]["frequency_with_bonus"]


# 가중치가 적용된 랜덤 번호 생성
def weighted_random_choice(weights, k=6):
    return random.choices(range(1, 46), weights=weights, k=k)


next_guesses = [weighted_random_choice(frequency_with_bonus) for _ in range(5)]

# next_guess.json 파일 업데이트
next_guess_data = {"next_guesses": next_guesses}

with open(NEXT_GUESS_FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(next_guess_data, f, ensure_ascii=False, indent=2)
