import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QListWidget, QTableWidget, QWidget
from qt_material import apply_stylesheet

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

apply_stylesheet(app, theme="dark_teal.xml")  # 스타일 적용


def initUi(self):
    self.setWindowTitle("pyqt6 위젯적용 테스트")
    self.setGeometry(1000, 10, 500, 500)

    # 레이아웃 및 라벨설정
    layout = self.layout
    layout.addWidget(QLabel("🧑🏻‍💻 WSCODE 수강생을 선택하시오"))

    # 리스트 위젯
    self.name_listwidget = QListWidget()
    self.name_listwidget.addItems(sorted(self.df["이름"]))
    self.layout.addWidget(self.name_listwidget)

    # 테이블 위젯
    self.table_widget = QTableWidget()
    self.table_widget.setColumnCount(self.df.shape[1])
    layout.addWidget(QLabel("📋 수강생 성적관리 "))
    layout.addWidget(self.table_widget)

    widget = QWidget()
    widget.setLayout(layout)
    self.setCentralWidget(widget)


initUi(window)
window.show()
app.exec_()
