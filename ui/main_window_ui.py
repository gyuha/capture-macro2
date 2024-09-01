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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

from app.widgets.command_widget import CommandWidget
from app.widgets.image_list_widget import ImageListWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(924, 905)
        self.actionSettingDialog = QAction(MainWindow)
        self.actionSettingDialog.setObjectName(u"actionSettingDialog")
        self.actionExit_Q = QAction(MainWindow)
        self.actionExit_Q.setObjectName(u"actionExit_Q")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(900, 0))
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pre_command_widget = CommandWidget(self.centralwidget)
        self.pre_command_widget.setObjectName(u"pre_command_widget")
        self.pre_command_widget.setMinimumSize(QSize(150, 111))

        self.verticalLayout.addWidget(self.pre_command_widget)

        self.command_widget = CommandWidget(self.centralwidget)
        self.command_widget.setObjectName(u"command_widget")
        self.command_widget.setMinimumSize(QSize(0, 111))

        self.verticalLayout.addWidget(self.command_widget)

        self.image_list_widget = ImageListWidget(self.centralwidget)
        self.image_list_widget.setObjectName(u"image_list_widget")
        self.image_list_widget.setMinimumSize(QSize(150, 300))

        self.verticalLayout.addWidget(self.image_list_widget)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 3)
        self.verticalLayout.setStretch(2, 5)

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

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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

        self.horizontalLayout_2.setStretch(0, 4)
        self.horizontalLayout_2.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 924, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionSettingDialog)
        self.menu.addAction(self.actionSave)
        self.menu.addSeparator()
        self.menu.addAction(self.actionExit_Q)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\ucea1\uccd0 \ub9e4\ud06c\ub85c", None))
        self.actionSettingDialog.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.actionSettingDialog.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSettingDialog.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit_Q.setText(QCoreApplication.translate("MainWindow", u"Exit(&Q)", None))
#if QT_CONFIG(shortcut)
        self.actionExit_Q.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save(&S)", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uc774\ubbf8\uc9c0", None))
        self.lbPreview.setText("")
        self.btnCapture.setText(QCoreApplication.translate("MainWindow", u"\ucea1\uccd0", None))
        self.btnStop.setText(QCoreApplication.translate("MainWindow", u"\uc815\uc9c0 (F2)", None))
        self.btnStart.setText(QCoreApplication.translate("MainWindow", u"\uc2dc\uc791 (F1)", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c", None))
    # retranslateUi

