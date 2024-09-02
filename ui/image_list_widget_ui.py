# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'image_list_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QListView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ImageListWidget(object):
    def setupUi(self, ImageListWidget):
        if not ImageListWidget.objectName():
            ImageListWidget.setObjectName(u"ImageListWidget")
        ImageListWidget.resize(349, 266)
        self.verticalLayout = QVBoxLayout(ImageListWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_2 = QGroupBox(ImageListWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.imageFiles = QListWidget(self.groupBox_2)
        self.imageFiles.setObjectName(u"imageFiles")
        self.imageFiles.setFrameShape(QFrame.Shape.Box)
        self.imageFiles.setFrameShadow(QFrame.Shadow.Sunken)
        self.imageFiles.setIconSize(QSize(80, 80))
        self.imageFiles.setTextElideMode(Qt.TextElideMode.ElideLeft)
        self.imageFiles.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerItem)
        self.imageFiles.setGridSize(QSize(0, 82))
        self.imageFiles.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout_2.addWidget(self.imageFiles)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lbImageNumber = QLabel(self.groupBox_2)
        self.lbImageNumber.setObjectName(u"lbImageNumber")

        self.horizontalLayout.addWidget(self.lbImageNumber)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnDeleteFile = QPushButton(self.groupBox_2)
        self.btnDeleteFile.setObjectName(u"btnDeleteFile")
        self.btnDeleteFile.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_5.addWidget(self.btnDeleteFile)

        self.btnDeleteAllFiles = QPushButton(self.groupBox_2)
        self.btnDeleteAllFiles.setObjectName(u"btnDeleteAllFiles")

        self.horizontalLayout_5.addWidget(self.btnDeleteAllFiles)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.btnOpenFolder = QPushButton(self.groupBox_2)
        self.btnOpenFolder.setObjectName(u"btnOpenFolder")

        self.horizontalLayout_5.addWidget(self.btnOpenFolder)

        self.btnToPdf = QPushButton(self.groupBox_2)
        self.btnToPdf.setObjectName(u"btnToPdf")

        self.horizontalLayout_5.addWidget(self.btnToPdf)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addWidget(self.groupBox_2)


        self.retranslateUi(ImageListWidget)

        QMetaObject.connectSlotsByName(ImageListWidget)
    # setupUi

    def retranslateUi(self, ImageListWidget):
        ImageListWidget.setWindowTitle(QCoreApplication.translate("ImageListWidget", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ImageListWidget", u"\uc774\ubbf8\uc9c0 \ubaa9\ub85d", None))
        self.label.setText(QCoreApplication.translate("ImageListWidget", u"\uc774\ubbf8\uc9c0 \ubc88\ud638 : ", None))
        self.lbImageNumber.setText(QCoreApplication.translate("ImageListWidget", u"0", None))
        self.btnDeleteFile.setText(QCoreApplication.translate("ImageListWidget", u"\uc0ad\uc81c", None))
        self.btnDeleteAllFiles.setText(QCoreApplication.translate("ImageListWidget", u"\uc804\uccb4 \uc0ad\uc81c", None))
        self.btnOpenFolder.setText(QCoreApplication.translate("ImageListWidget", u"\ud3f4\ub354 \uc5f4\uae30", None))
        self.btnToPdf.setText(QCoreApplication.translate("ImageListWidget", u"PDF\ub85c \uc800\uc7a5", None))
    # retranslateUi

