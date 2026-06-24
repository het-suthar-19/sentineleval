import json


def save_test_cases(test_cases: list[str], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as file_handle:
        json.dump(test_cases, file_handle, ensure_ascii=False, indent=2)


def load_test_cases(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)
