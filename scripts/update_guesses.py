import json
import random
import os

# 파일 경로 상수 정의
FREQUENCY_FILE_PATH = "data/frequency.json"
PREVIOUS_GUESSES_FILE_PATH = "data/guesses.json"
NEXT_GUESS_FILE_PATH = "data/next_guess.json"

# 난수 시퀀스 초기화
random.seed(int.from_bytes(os.urandom(8), byteorder="big"))


# frequency.json 파일 읽기
def load_frequency_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"JSON 파일 형식이 올바르지 않습니다: {file_path}")
        return None


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
#
# NOTE: 'random.choices' 함수는 '가중치'를 적용해서 중복을 허용해 랜덤 번호를 뽑고,
#       'random.sample' 함수는 '가중치' 적용은 없지만 중복을 허용하지 않고 랜덤 번호를 뽑는다.
def weighted_random_choice(weights, k=6):
    population = list(range(1, 46))  # 1부터 45까지의 번호
    chosen = set()
    attempts = 0
    max_attempts = 1024  # 최대 시도 횟수를 1024로 설정

    while len(chosen) < k and attempts < max_attempts:
        choice = random.choices(population, weights=weights, k=1)[0]
        if choice not in chosen:
            chosen.add(choice)
        attempts += 1

    if len(chosen) < k:
        # 최대 시도 횟수를 초과했을 경우, 남은 번호를 무작위로 선택
        remaining = set(population) - chosen
        chosen.update(random.sample(remaining, k - len(chosen)))

    return sorted(chosen)


# JSON 데이터를 직접 문자열로 변환하는 함수
def format_json_directly(data, is_guesses=False):
    if is_guesses:
        # guesses.json 파일용 포맷팅
        formatted_str = '{\n  "start_draw": ' + str(data["start_draw"]) + ",\n"
        formatted_str += '  "end_draw": ' + str(data["end_draw"]) + ",\n"
        formatted_str += '  "guesses": [\n'
        for guess in data["guesses"]:
            draw_number = list(guess.keys())[0]
            formatted_str += f'    {{\n      "{draw_number}": [\n'
            for numbers in guess[draw_number]:
                formatted_str += f"        {json.dumps(numbers)},\n"
            formatted_str = formatted_str.rstrip(",\n") + "\n      ]\n    },\n"
        formatted_str = formatted_str.rstrip(",\n") + "\n  ]\n}"
    else:
        # next_guess.json 파일용 포맷팅
        formatted_str = '{\n  "next_guesses": [\n'
        for guess in data["next_guesses"]:
            formatted_str += "    " + json.dumps(guess) + ",\n"
        formatted_str = formatted_str.rstrip(",\n") + "\n  ]\n}"
    return formatted_str


# 기존의 next_guess.json 데이터를 guesses.json에 추가
def update_guesses_file():
    # guesses.json 파일 읽기
    with open(PREVIOUS_GUESSES_FILE_PATH, "r", encoding="utf-8") as f:
        guesses_data = json.load(f)

    # next_guess.json 파일 읽기
    with open(NEXT_GUESS_FILE_PATH, "r", encoding="utf-8") as f:
        next_guess_data = json.load(f)

    # end_draw 값을 1 증가
    guesses_data["end_draw"] += 1
    new_draw_number = guesses_data["end_draw"]

    # 이전 회차의 추측 데이터 추가 (현재의 next_guess 데이터)
    new_guess = {f"draw_{new_draw_number}": next_guess_data["next_guesses"]}
    guesses_data["guesses"].append(new_guess)

    # 포맷팅된 JSON 문자열 생성
    formatted_json_str = format_json_directly(guesses_data, is_guesses=True)

    # 업데이트된 데이터를 guesses.json 파일에 쓰기
    with open(PREVIOUS_GUESSES_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(formatted_json_str)


def write_json_file(file_path, data, is_guesses=False):
    try:
        formatted_json_str = format_json_directly(data, is_guesses)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_json_str)
    except IOError:
        print(f"파일을 쓸 수 없습니다: {file_path}")


# main 함수
def main():
    try:
        # 기존의 next_guess.json 데이터를 guesses.json에 추가
        update_guesses_file()

        # 새로운 next_guess 데이터 생성
        frequency_data = load_frequency_data(FREQUENCY_FILE_PATH)
        if frequency_data is None:
            print("빈도 데이터를 불러오는데 실패했습니다. 프로그램을 종료합니다.")
            return

        update_cumulative_stats(frequency_data)

        frequency_with_bonus = frequency_data["cumulative_stats"][
            "frequency_with_bonus"
        ]
        frequency_without_bonus = frequency_data["cumulative_stats"][
            "frequency_without_bonus"
        ]

        # 추첨번호 5개중에 3개는 보너스 번호가 있는 빈도 데이터에서 선택하고, 2개는 보너스 번호가 없는 빈도 데이터에서 선택
        next_guesses = [weighted_random_choice(frequency_with_bonus) for _ in range(3)]
        next_guesses += [
            weighted_random_choice(frequency_without_bonus) for _ in range(2)
        ]

        next_guess_data = {"next_guesses": next_guesses}
        # 새로운 next_guess 데이터를 파일에 쓰기
        write_json_file(NEXT_GUESS_FILE_PATH, next_guess_data)
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
