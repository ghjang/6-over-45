import json
import random
import time

# 파일 경로 상수 정의
FREQUENCY_FILE_PATH = "data/frequency.json"
NEXT_GUESS_FILE_PATH = "data/next_guess.json"

# 난수 시퀀스 초기화
random.seed(time.time())

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


# 가중치가 적용된 랜덤 번호 생성 (중복 없이)
def weighted_random_choice(weights, k=6):
    population = list(range(1, 46))
    choices = random.choices(
        population, weights=weights, k=k * 2
    )  # 중복을 피하기 위해 더 많이 선택
    unique_choices = list(set(choices))[:k]  # 중복 제거 후 필요한 개수만큼 자르기
    while len(unique_choices) < k:
        additional_choices = random.choices(
            population, weights=weights, k=k - len(unique_choices)
        )
        unique_choices.extend(list(set(additional_choices)))
        unique_choices = list(set(unique_choices))[:k]
    return sorted(unique_choices)


next_guesses = [weighted_random_choice(frequency_with_bonus) for _ in range(5)]

# next_guess.json 파일 업데이트
next_guess_data = {"next_guesses": next_guesses}


# 'data'로부터 'JSON' 문자열 생성
def format_data(data):
    formatted_str = '{\n  "next_guesses": [\n'
    for guess in data["next_guesses"]:
        formatted_str += "    " + json.dumps(guess, ensure_ascii=False) + ",\n"
    formatted_str = formatted_str.rstrip(",\n") + "\n  ]\n}"
    return formatted_str


# JSON 데이터를 원하는 형식으로 출력
formatted_json_str = format_data(next_guess_data)

# 파일에 쓰기
with open(NEXT_GUESS_FILE_PATH, "w", encoding="utf-8") as f:
    f.write(formatted_json_str)
