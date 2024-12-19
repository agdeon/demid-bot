import re

class GPTResponseHTMLFormatter:

    @classmethod
    def format(cls, text: str) -> str:
        """
        :param text: Текст ответа который включает в себя код
        :return: Возвращает массив состоящий из строк в котором либо строка содержит исключительно текст, либо же это код
        """
        result_list = []
        text_flag = True
        while True:
            tag_start, tag_end = cls._find_code_tag_indexes(text)
            if tag_start == -1:
                result_list.append(text)
                break

            # Когда открыли ТЕКСТ и записываем его
            if text_flag:
                text_flag = False
                corrected_text = cls._replace_hashes(text[:tag_start])
                corrected_text = cls._replace_asterisks(corrected_text)
                result_list.append(corrected_text)
                text = text[tag_end:]
            # Когда открыли ТЕКСТ и записываем его
            else:
                text_flag = True
                wrapped_code = cls._wrap_with_tag(text[:tag_start], '<pre>', '</pre>')
                result_list.append(wrapped_code)
                text = text[tag_end:]

        return "".join(result_list)

    @classmethod
    def _replace_hashes(cls, text: str) -> str:
        pattern = r"(#{1,5})\s*(.*?)(\n)"
        formatted_text = re.sub(pattern, r"<b><u>\2</u></b>\3", text)
        return formatted_text

    @classmethod
    def _replace_asterisks(cls, text: str) -> str:
        pattern = r"(\*{1,4})(.*?)(\*{1,4})"
        formatted_text = re.sub(pattern, r"<b>\2</b>", text)
        return formatted_text

    @classmethod
    def _wrap_code(cls, text: str):
        """
        Функция должна разбивать текст на массив строк, где строки текста будут отдельно, а строки с кодом - отдельно
        Затем в строках с текстом удаляем звездочки решетки и  меняем их соотв. тэгами html, а строки с кодом
        очищаем от markdown тэгов ```python  и ``` например и оборачиваем в тэг <pre></pre>
        """
        pass

    @classmethod
    def _has_code(cls, text: str):
        pattern = r"```[a-zA-Z]*\n"
        if re.search(pattern, text):
            return True
        return False

    @classmethod
    def _find_code_tag_indexes(cls, text: str) -> tuple:
        """
        Ищет открывающий или же закрывающий тэг кода + перенос на новую строку.
        """
        code_tag_pattern = r"```[a-zA-Z]*\n"
        match = re.search(code_tag_pattern, text)
        if not match:
            return -1, -1
        start, end = match.start(), match.end()
        if start or end:
            return start, end
        return -1, -1

    @classmethod
    def _wrap_with_tag(cls, text: str, html_open_tag: str, html_close_tag: str) -> str:
        return html_open_tag + text + html_close_tag


if __name__ == "__main__":
    text = ("Here is some text!\n"
    "```python\n"
    "print(\"Hello, world!\")\n"
    "```\n"
    "Lorem ipsum...\n"
    "```javascript\n"
    "console.log(\"Hi\");\n"
    "```\n"
    "Some text again\n")
    print(GPTResponseHTMLFormatter.format(text))
