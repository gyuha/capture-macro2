from pynput.keyboard import Key, KeyCode

KEY_MAPPING = {
    # 특수 키
    "alt": Key.alt,
    "alt_gr": Key.alt_gr,
    "backspace": Key.backspace,
    "caps_lock": Key.caps_lock,
    "cmd": Key.cmd,
    "ctrl": Key.ctrl,
    "delete": Key.delete,
    "down": Key.down,
    "end": Key.end,
    "enter": Key.enter,
    "esc": Key.esc,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    "f13": Key.f13,
    "f14": Key.f14,
    "f15": Key.f15,
    "f16": Key.f16,
    "f17": Key.f17,
    "f18": Key.f18,
    "f19": Key.f19,
    "f20": Key.f20,
    "home": Key.home,
    # "insert": Key.insert,
    "left": Key.left,
    # "menu": Key.menu,
    # "num_lock": Key.num_lock,
    "page_down": Key.page_down,
    "page_up": Key.page_up,
    # "pause": Key.pause,
    # "print_screen": Key.print_screen,
    "right": Key.right,
    # "scroll_lock": Key.scroll_lock,
    "shift": Key.shift,
    "space": Key.space,
    "tab": Key.tab,
    "up": Key.up,
    # 일반 문자 키
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "i",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "x",
    "y": "y",
    "z": "z",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    # 특수 문자
    "exclamation": "!",
    "at": "@",
    "hash": "#",
    "dollar": "$",
    "percent": "%",
    "caret": "^",
    "ampersand": "&",
    "asterisk": "*",
    "left_paren": "(",
    "right_paren": ")",
    "minus": "-",
    "underscore": "_",
    "plus": "+",
    "equals": "=",
    "left_bracket": "[",
    "right_bracket": "]",
    "left_brace": "{",
    "right_brace": "}",
    "backslash": "\\",
    "pipe": "|",
    "semicolon": ";",
    "colon": ":",
    "quote": "'",
    "double_quote": '"',
    "comma": ",",
    "period": ".",
    "less_than": "<",
    "greater_than": ">",
    "slash": "/",
    "question": "?",
    "backtick": "`",
    "tilde": "~",
}

# 역방향 매핑 (값에서 키로)
REVERSE_KEY_MAPPING = {str(v): k for k, v in KEY_MAPPING.items()}


def get_key_from_string(key_string):
    """
    문자열을 받아 해당하는 키를 반환합니다.
    키가 없으면 None을 반환합니다.
    """
    if key_string in KEY_MAPPING:
        return KEY_MAPPING[key_string]
    elif len(key_string) == 1:
        return KeyCode.from_char(key_string)
    else:
        return None


# 사용 예시
if __name__ == "__main__":
    # 특수 키 테스트
    print(get_key_from_string("ctrl"))  # 출력: Key.ctrl

    # 일반 문자 키 테스트
    print(get_key_from_string("a"))  # 출력: KeyCode.from_char('a')

    # 존재하지 않는 키 테스트
    print(get_key_from_string("non_existent"))  # 출력: None

    # 복합 키 시퀀스 예시
    key_sequence = ["ctrl", "alt", "delete", "a", "non_existent"]
    print([get_key_from_string(k) for k in key_sequence])
    # 출력: [Key.ctrl, Key.alt, Key.delete, KeyCode.from_char('a'), None]

    # 역방향 변환 테스트
    keys = [Key.ctrl, Key.alt, Key.delete, KeyCode.from_char("a")]
    # 출력: ['ctrl', 'alt', 'delete', 'a']
