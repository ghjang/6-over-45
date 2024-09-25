import json


def format_json(obj, indent=2):
    """JSON 객체를 보기 좋게 포맷팅하는 함수"""
    if isinstance(obj, dict):
        return (
            "{\n"
            + ",\n".join(
                f'{" " * indent}"{k}": {format_json(v, indent + 2)}'
                for k, v in obj.items()
            )
            + "\n"
            + " " * (indent - 2)
            + "}"
        )
    elif isinstance(obj, list):
        if all(isinstance(item, int) for item in obj):
            items = [str(item) for item in obj]
            chunks = [items[i : i + 10] for i in range(0, len(items), 10)]
            formatted_chunks = [", ".join(chunk) for chunk in chunks]
            return (
                "[\n"
                + ",\n".join(f'{" " * indent}{chunk}' for chunk in formatted_chunks)
                + "\n"
                + " " * (indent - 2)
                + "]"
            )
        return (
            "[\n"
            + ",\n".join(
                f'{" " * indent}{format_json(item, indent + 2)}' for item in obj
            )
            + "\n"
            + " " * (indent - 2)
            + "]"
        )
    elif isinstance(obj, str):
        return f'"{obj}"'
    else:
        return json.dumps(obj)


# 최신 로또 결과 파일 읽기
with open("data/latest_lottery_result.json", "r") as f:
    latest_result = json.load(f)

# frequency.json 파일 읽기
with open("data/frequency.json", "r") as f:
    frequency_data = json.load(f)

# 최신 로또 결과를 recent_draws에 추가 또는 업데이트
draw_key = f"draw_{latest_result['draw_number']}"
frequency_data["recent_draws"][draw_key] = {
    "winning_numbers": latest_result["winning_numbers"],
    "bonus_number": latest_result["bonus_number"],
}

# 포맷팅된 JSON 문자열 생성
formatted_json = format_json(frequency_data)

# 포맷팅된 데이터를 frequency.json 파일에 쓰기
with open("data/frequency.json", "w") as f:
    f.write(formatted_json)

print(
    f"frequency.json 파일이 성공적으로 업데이트되고 포맷팅되었습니다. (회차: {latest_result['draw_number']})"
)
