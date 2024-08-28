# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from app.widgets.command_widget import CommandWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1143, 942)
        self.actionOpen_O = QAction(MainWindow)
        self.actionOpen_O.setObjectName(u"actionOpen_O")
        self.actionSave_S = QAction(MainWindow)
        self.actionSave_S.setObjectName(u"actionSave_S")
        self.actionSave_as_A = QAction(MainWindow)
        self.actionSave_as_A.setObjectName(u"actionSave_as_A")
        self.actionExit_Q = QAction(MainWindow)
        self.actionExit_Q.setObjectName(u"actionExit_Q")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pre_command_widget = CommandWidget(self.centralwidget)
        self.pre_command_widget.setObjectName(u"pre_command_widget")
        self.pre_command_widget.setMinimumSize(QSize(0, 111))

        self.verticalLayout.addWidget(self.pre_command_widget)

        self.command_widget = CommandWidget(self.centralwidget)
        self.command_widget.setObjectName(u"command_widget")
        self.command_widget.setMinimumSize(QSize(0, 111))

        self.verticalLayout.addWidget(self.command_widget)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lsFiles = QListWidget(self.groupBox_2)
        self.lsFiles.setObjectName(u"lsFiles")
        self.lsFiles.setFrameShape(QFrame.Box)
        self.lsFiles.setFrameShadow(QFrame.Sunken)
        self.lsFiles.setIconSize(QSize(80, 120))
        self.lsFiles.setTextElideMode(Qt.ElideLeft)
        self.lsFiles.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.lsFiles.setGridSize(QSize(0, 120))
        self.lsFiles.setViewMode(QListView.ListMode)

        self.verticalLayout_2.addWidget(self.lsFiles)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnDeleteFile_2 = QPushButton(self.groupBox_2)
        self.btnDeleteFile_2.setObjectName(u"btnDeleteFile_2")
        self.btnDeleteFile_2.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_5.addWidget(self.btnDeleteFile_2)

        self.btnDeleteAllFiles_2 = QPushButton(self.groupBox_2)
        self.btnDeleteAllFiles_2.setObjectName(u"btnDeleteAllFiles_2")

        self.horizontalLayout_5.addWidget(self.btnDeleteAllFiles_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.btnToPdf_2 = QPushButton(self.groupBox_2)
        self.btnToPdf_2.setObjectName(u"btnToPdf_2")

        self.horizontalLayout_5.addWidget(self.btnToPdf_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 3)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lbPreview = QLabel(self.groupBox_3)
        self.lbPreview.setObjectName(u"lbPreview")
        self.lbPreview.setSizeIncrement(QSize(0, 0))
        font = QFont()
        font.setBold(False)
        self.lbPreview.setFont(font)
        self.lbPreview.setAutoFillBackground(True)

        self.verticalLayout_4.addWidget(self.lbPreview)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnCapture = QPushButton(self.groupBox_3)
        self.btnCapture.setObjectName(u"btnCapture")
        self.btnCapture.setMinimumSize(QSize(60, 0))
        self.btnCapture.setFont(font)

        self.horizontalLayout.addWidget(self.btnCapture)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.btnStop = QPushButton(self.groupBox_3)
        self.btnStop.setObjectName(u"btnStop")
        self.btnStop.setMinimumSize(QSize(50, 0))
        self.btnStop.setFont(font)

        self.horizontalLayout.addWidget(self.btnStop)

        self.btnStart = QPushButton(self.groupBox_3)
        self.btnStart.setObjectName(u"btnStart")
        self.btnStart.setMinimumSize(QSize(50, 0))
        self.btnStart.setFont(font)

        self.horizontalLayout.addWidget(self.btnStart)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.verticalLayout_4.setStretch(0, 1)

        self.horizontalLayout_2.addWidget(self.groupBox_3)

        self.horizontalLayout_2.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1143, 24))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionOpen_O)
        self.menu.addAction(self.actionSave_S)
        self.menu.addAction(self.actionSave_as_A)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit_Q)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\ucea1\uccd0 \ub9e4\ud06c\ub85c", None))
        self.actionOpen_O.setText(QCoreApplication.translate("MainWindow", u"Open(&O)", None))
        self.actionSave_S.setText(QCoreApplication.translate("MainWindow", u"Save(&S)", None))
        self.actionSave_as_A.setText(QCoreApplication.translate("MainWindow", u"Save as... (&A)", None))
        self.actionExit_Q.setText(QCoreApplication.translate("MainWindow", u"Exit(&Q)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0 \ubaa9\ub85d", None))
        self.btnDeleteFile_2.setText(QCoreApplication.translate("MainWindow", u"\uc0ad\uc81c", None))
        self.btnDeleteAllFiles_2.setText(QCoreApplication.translate("MainWindow", u"\uc804\uccb4 \uc0ad\uc81c", None))
        self.btnToPdf_2.setText(QCoreApplication.translate("MainWindow", u"PDF\ub85c \uc800\uc7a5", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0", None))
        self.lbPreview.setText("")
        self.btnCapture.setText(QCoreApplication.translate("MainWindow", u"\ucea1\uccd0", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc9c0 (F2)", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791 (F1)", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

