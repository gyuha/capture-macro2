# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_dlgSetting(object):
    def setupUi(self, dlgSetting):
        if not dlgSetting.objectName():
            dlgSetting.setObjectName(u"dlgSetting")
        dlgSetting.resize(463, 258)
        dlgSetting.setMaximumSize(QSize(463, 258))
        dlgSetting.setSizeGripEnabled(False)
        dlgSetting.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(dlgSetting)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(dlgSetting)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.leMonitorNum = QLineEdit(self.frame)
        self.leMonitorNum.setObjectName(u"leMonitorNum")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leMonitorNum)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.leSameCount = QLineEdit(self.frame)
        self.leSameCount.setObjectName(u"leSameCount")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.leSameCount)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.leMaxPage = QLineEdit(self.frame)
        self.leMaxPage.setObjectName(u"leMaxPage")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.leMaxPage)

        self.leImageCompress = QLineEdit(self.frame)
        self.leImageCompress.setObjectName(u"leImageCompress")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.leImageCompress)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.leImagePath = QLineEdit(self.frame)
        self.leImagePath.setObjectName(u"leImagePath")
        self.leImagePath.setMinimumSize(QSize(0, 22))

        self.horizontalLayout_2.addWidget(self.leImagePath)

        self.btnImagePath = QPushButton(self.frame)
        self.btnImagePath.setObjectName(u"btnImagePath")

        self.horizontalLayout_2.addWidget(self.btnImagePath)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.frame)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btnCancel = QPushButton(dlgSetting)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout.addWidget(self.btnCancel)

        self.btnOk = QPushButton(dlgSetting)
        self.btnOk.setObjectName(u"btnOk")

        self.horizontalLayout.addWidget(self.btnOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(dlgSetting)

        QMetaObject.connectSlotsByName(dlgSetting)
    # setupUi

    def retranslateUi(self, dlgSetting):
        dlgSetting.setWindowTitle(QCoreApplication.translate("dlgSetting", u"\uc124\uc815", None))
        self.label.setText(QCoreApplication.translate("dlgSetting", u"\ubaa8\ub2c8\ud130 \ubc88\ud638", None))
        self.leMonitorNum.setText(QCoreApplication.translate("dlgSetting", u"0", None))
        self.label_2.setText(QCoreApplication.translate("dlgSetting", u"\uc911\ubcf5 \uc774\ubbf8\uc9c0 \uc911\ub2e8", None))
        self.leSameCount.setText(QCoreApplication.translate("dlgSetting", u"3", None))
        self.label_3.setText(QCoreApplication.translate("dlgSetting", u"\uc774\ubbf8\uc9c0 \uc555\ucd95\uc728", None))
        self.label_4.setText(QCoreApplication.translate("dlgSetting", u"\ucd5c\ub300 \ud398\uc774\uc9c0", None))
        self.leMaxPage.setText(QCoreApplication.translate("dlgSetting", u"1500", None))
        self.leImageCompress.setText(QCoreApplication.translate("dlgSetting", u"80", None))
        self.label_5.setText(QCoreApplication.translate("dlgSetting", u"\uc774\ubbf8\uc9c0 \uc800\uc7a5 \uacbd\ub85c", None))
        self.btnImagePath.setText(QCoreApplication.translate("dlgSetting", u"\uc120\ud0dd", None))
        self.btnCancel.setText(QCoreApplication.translate("dlgSetting", u"\ucde8\uc18c", None))
        self.btnOk.setText(QCoreApplication.translate("dlgSetting", u"\ud655\uc778", None))
    # retranslateUi

