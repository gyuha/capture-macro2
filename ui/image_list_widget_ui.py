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
    QHBoxLayout, QListView, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ImageListWidget(object):
    def setupUi(self, ImageListWidget):
        if not ImageListWidget.objectName():
            ImageListWidget.setObjectName(u"ImageListWidget")
        ImageListWidget.resize(456, 415)
        self.verticalLayout = QVBoxLayout(ImageListWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_2 = QGroupBox(ImageListWidget)
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


        self.retranslateUi(ImageListWidget)

        QMetaObject.connectSlotsByName(ImageListWidget)
    # setupUi

    def retranslateUi(self, ImageListWidget):
        ImageListWidget.setWindowTitle(QCoreApplication.translate("ImageListWidget", u"Form", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ImageListWidget", u"\uc774\ubbf8\uc9c0 \ubaa9\ub85d", None))
        self.btnDeleteFile_2.setText(QCoreApplication.translate("ImageListWidget", u"\uc0ad\uc81c", None))
        self.btnDeleteAllFiles_2.setText(QCoreApplication.translate("ImageListWidget", u"\uc804\uccb4 \uc0ad\uc81c", None))
        self.btnToPdf_2.setText(QCoreApplication.translate("ImageListWidget", u"PDF\ub85c \uc800\uc7a5", None))
    # retranslateUi

