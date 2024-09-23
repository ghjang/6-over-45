import json
import random
import time

# 파일 경로 상수 정의
FREQUENCY_FILE_PATH = "data/frequency.json"
NEXT_GUESS_FILE_PATH = "data/next_guess.json"

# 난수 시퀀스 초기화
random.seed(time.time())


# frequency.json 파일 읽기
def load_frequency_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# 누적 빈도수 정보 업데이트
def update_cumulative_stats(frequency_data):
    recent_draws = frequency_data["recent_draws"]
    for draw in recent_draws.values():
        winning_numbers = draw["winning_numbers"]
        bonus_number = draw["bonus_number"]

        for number in winning_numbers:
            frequency_data["cumulative_stats"]["frequency_with_bonus"][number - 1] += 1
            frequency_data["cumulative_stats"]["frequency_without_bonus"][
                number - 1
            ] += 1

        frequency_data["cumulative_stats"]["frequency_with_bonus"][
            bonus_number - 1
        ] += 1


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


# JSON 데이터를 직접 문자열로 변환하는 함수
# NOTE: 'data' 전체를 'json.dumps'로 변환하면 원하는 형태의 줄바꿈이 되지 않아 커스텀 처리를 했음.
def format_json_directly(data):
    formatted_str = '{\n  "next_guesses": [\n'
    for guess in data["next_guesses"]:
        formatted_str += "    " + json.dumps(guess, ensure_ascii=False) + ",\n"
    formatted_str = formatted_str.rstrip(",\n") + "\n  ]\n}"
    return formatted_str


# main 함수
def main():
    frequency_data = load_frequency_data(FREQUENCY_FILE_PATH)
    update_cumulative_stats(frequency_data)

    frequency_with_bonus = frequency_data["cumulative_stats"]["frequency_with_bonus"]
    frequency_without_bonus = frequency_data["cumulative_stats"][
        "frequency_without_bonus"
    ]

    # 추첨번호 5개중에 3개는 보너스 번호가 있는 빈도 데이터에서 선택하고, 2개는 보너스 번호가 없는 빈도 데이터에서 선택
    next_guesses = [weighted_random_choice(frequency_with_bonus) for _ in range(3)]
    next_guesses += [weighted_random_choice(frequency_without_bonus) for _ in range(2)]

    next_guess_data = {"next_guesses": next_guesses}
    formatted_json_str = format_json_directly(next_guess_data)

    with open(NEXT_GUESS_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(formatted_json_str)


if __name__ == "__main__":
    main()
