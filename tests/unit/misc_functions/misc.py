
def _remove_active_status_str(text):
    text = str(text)
    if text[0:2] == '✅ ':
        return text[2:]
    else:
        return text


print(_remove_active_status_char(' gdfsg'))