import re


def format_text(text: str) -> str:
    pattern = r"(#{1,3})\s*(.*?)(\n)"
    formatted_text = re.sub(pattern, r"<b><u>\2</u></b>\3", text)

    return formatted_text


text = """### 1. Определение состояния
# Заголовок первого уровня
## Подзаголовок второго уровня
Текст без решеточек."""

formatted_text = format_text(text)
print(formatted_text)