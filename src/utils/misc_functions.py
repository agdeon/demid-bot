import json
from pathlib import Path
from typing import Union


def read_json_from_file(path: Union[str, Path]) -> Union[dict, list]:
    path = Path(str(path))
    with open(path, 'r', encoding='utf-8') as file:
        json_content = json.load(file)
    return json_content


def write_json_to_file(path: Union[str, Path], json_content: Union[dict, list]):
    path = Path(str(path))
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(json_content, file, indent=4, ensure_ascii=False)


def create_empty_file_by_path(file_path: Union[str, Path]):
    path = Path(str(file_path))
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


if __name__ == '__main__':
    create_empty_file_by_path(r"E:\Code\Git\Projects\DemidBot\Test\InnerFolder\test.json")