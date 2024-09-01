
from PySide6.QtCore import QObject

class QtSingleton(QObject):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QtSingleton, cls).__new__(cls)
            # 여기서 __init__을 호출하지 않습니다.
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
            # 초기화 코드를 여기에 작성합니다.

class AA(QtSingleton):
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'num'):
            self.num = 123

if __name__ == "__main__":
    aa = AA()
    bb = AA()
    print(aa)
    print(bb)
    print(aa.num)
    print(bb.num)

    # id를 통해 같은 객체인지 확인
    print(id(aa) == id(bb))
