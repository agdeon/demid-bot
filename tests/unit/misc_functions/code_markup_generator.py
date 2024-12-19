import re

class CodeMarkupGenerator:
    def __init__(self, text):
        self.start_code_pattern = r"```[a-zA-Z]*\n"
        self.end_code_pattern = "```"

    def get_html(self):

        while True:


    def find_first_pattern_indexes(self, pattern, text: str) -> tuple | int:
        match = re.search(pattern, text)
        start, end = match.start(), match.end()
        if start or end:
            return start, end
        return -1


text = """Here is some text.
```python
print("Hello, world!")
```javascript
console.log("Hi");
```bash
echo "Hello"
```text
Some simple text.
"""

start, end = TextCodeSplitter().find_first_pattern_indexes(TextCodeSplitter.START_CODE_PATTERN, text)

print(text[:start])
print(text[end:])




# Пример использования
text = "This is normal text. ```python\nprint('Hello')``` And more text. ```javascript\nconsole.log('Hi')```"




# def split_text_and_code(text: str):
#     # Регулярное выражение для поиска блоков с кодом и обычного текста
#     pattern = r"```[^\n]*```"  # Ищет блоки с кодом (включая тройные обратные кавычки)
#
#     result = []
#     last_end = 0  # Указатель на конец последнего совпадения
#
#     # Проходим по всем совпадениям с шаблоном
#     for match in re.finditer(pattern, text):
#         # Добавляем текст до текущего блока кода
#         if match.start() > last_end:
#             result.append({
#                 "type": "text",
#                 "content": text[last_end:match.start()].strip()
#             })
#
#         # Добавляем сам блок кода
#         result.append({
#             "type": "code",
#             "content": match.group(0).strip("`")  # Убираем обратные кавычки
#         })
#
#         last_end = match.end()  # Обновляем конец для следующего текста
#
#     # Добавляем оставшийся текст после последнего блока кода
#     if last_end < len(text):
#         result.append({
#             "type": "text",
#             "content": text[last_end:].strip()
#         })
#
#     return result