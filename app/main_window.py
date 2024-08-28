from PySide6.QtWidgets import QMainWindow, QVBoxLayout

from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.pre_command_widget = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect signals to slots
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.ui.pre_command_widget.ui.groupBox.setTitle("사전 수행")
        self.ui.command_widget.ui.groupBox.setTitle("수행")

        # File buttons
        self.ui.btnDeleteFile_2.clicked.connect(self.on_delete_file)
        self.ui.btnDeleteAllFiles_2.clicked.connect(self.on_delete_all_files)
        self.ui.btnToPdf_2.clicked.connect(self.on_to_pdf)

        # Capture and control buttons
        self.ui.btnCapture.clicked.connect(self.on_capture)
        self.ui.btnStop.clicked.connect(self.on_stop)
        self.ui.btnStart.clicked.connect(self.on_start)
        # self.ui.btnStart.setStyleSheet('background-color: #1BA1E2;color: white;')

        # Menu actions
        self.ui.actionOpen_O.triggered.connect(self.on_open)
        self.ui.actionSave_S.triggered.connect(self.on_save)
        self.ui.actionSave_as_A.triggered.connect(self.on_save_as)
        self.ui.actionExit_Q.triggered.connect(self.close)

    def on_delete_file(self):
        # TODO: Implement delete file logic
        pass

    def on_delete_all_files(self):
        # TODO: Implement delete all files logic
        pass

    def on_to_pdf(self):
        # TODO: Implement to PDF logic
        pass

    def on_capture(self):
        # TODO: Implement capture logic
        pass

    def on_stop(self):
        # TODO: Implement stop logic
        pass

    def on_start(self):
        # TODO: Implement start logic
        pass

    def on_open(self):
        # TODO: Implement open file logic
        pass

    def on_save(self):
        # TODO: Implement save logic
        pass

    def on_save_as(self):
        # TODO: Implement save as logic
        pass
