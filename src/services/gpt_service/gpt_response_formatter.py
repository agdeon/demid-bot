import re

class GPTResponseHTMLFormatter:

    @classmethod
    def format(cls, text):
        text = cls._replace_hashes(text)
        text = cls._replace_asterisks(text)
        return text

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

    def _has_code(self, text):
        pattern = r"```[^\n]*```"
        if re.search(pattern, text):
            return True
        return False


if __name__ == "__main__":
    pass