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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QDialog,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_SettingDialog(object):
    def setupUi(self, SettingDialog):
        if not SettingDialog.objectName():
            SettingDialog.setObjectName(u"SettingDialog")
        SettingDialog.resize(431, 345)
        SettingDialog.setMaximumSize(QSize(500, 400))
        SettingDialog.setSizeGripEnabled(False)
        SettingDialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(SettingDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(SettingDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.cbMonitorNum = QComboBox(self.frame)
        self.cbMonitorNum.setObjectName(u"cbMonitorNum")
        self.cbMonitorNum.setMinimumSize(QSize(200, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cbMonitorNum)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.sbSameCount = QSlider(self.frame)
        self.sbSameCount.setObjectName(u"sbSameCount")
        self.sbSameCount.setMinimumSize(QSize(200, 0))
        self.sbSameCount.setValue(3)
        self.sbSameCount.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_5.addWidget(self.sbSameCount)

        self.lbSameCount = QLabel(self.frame)
        self.lbSameCount.setObjectName(u"lbSameCount")
        self.lbSameCount.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_5.addWidget(self.lbSameCount)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.sbMaxPage = QSpinBox(self.frame)
        self.sbMaxPage.setObjectName(u"sbMaxPage")
        self.sbMaxPage.setMinimumSize(QSize(100, 0))
        self.sbMaxPage.setMinimum(100)
        self.sbMaxPage.setMaximum(5000)
        self.sbMaxPage.setValue(1500)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sbMaxPage)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.leImagePath = QLineEdit(self.frame)
        self.leImagePath.setObjectName(u"leImagePath")
        self.leImagePath.setMinimumSize(QSize(200, 22))

        self.horizontalLayout_2.addWidget(self.leImagePath)

        self.btnImagePath = QPushButton(self.frame)
        self.btnImagePath.setObjectName(u"btnImagePath")
        self.btnImagePath.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.btnImagePath)


        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lePdfPath = QLineEdit(self.frame)
        self.lePdfPath.setObjectName(u"lePdfPath")
        self.lePdfPath.setMinimumSize(QSize(200, 22))

        self.horizontalLayout_3.addWidget(self.lePdfPath)

        self.btnPdfPath = QPushButton(self.frame)
        self.btnPdfPath.setObjectName(u"btnPdfPath")

        self.horizontalLayout_3.addWidget(self.btnPdfPath)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_3)

        self.sbImageCompress = QSpinBox(self.frame)
        self.sbImageCompress.setObjectName(u"sbImageCompress")
        self.sbImageCompress.setMinimumSize(QSize(100, 0))
        self.sbImageCompress.setMinimum(50)
        self.sbImageCompress.setMaximum(100)
        self.sbImageCompress.setValue(85)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.sbImageCompress)

        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.sbImageSize = QSpinBox(self.frame)
        self.sbImageSize.setObjectName(u"sbImageSize")
        self.sbImageSize.setMinimumSize(QSize(100, 0))
        self.sbImageSize.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.sbImageSize.setMinimum(500)
        self.sbImageSize.setMaximum(6000)
        self.sbImageSize.setValue(2000)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.sbImageSize)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_8)

        self.sbWheel = QSpinBox(self.frame)
        self.sbWheel.setObjectName(u"sbWheel")
        self.sbWheel.setMinimum(-100)
        self.sbWheel.setMaximum(100)
        self.sbWheel.setSingleStep(10)
        self.sbWheel.setValue(-1)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.sbWheel)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.rbLeft = QRadioButton(self.frame)
        self.bgSwipeDirection = QButtonGroup(SettingDialog)
        self.bgSwipeDirection.setObjectName(u"bgSwipeDirection")
        self.bgSwipeDirection.addButton(self.rbLeft)
        self.rbLeft.setObjectName(u"rbLeft")
        self.rbLeft.setChecked(True)

        self.horizontalLayout_4.addWidget(self.rbLeft)

        self.rbRight = QRadioButton(self.frame)
        self.bgSwipeDirection.addButton(self.rbRight)
        self.rbRight.setObjectName(u"rbRight")

        self.horizontalLayout_4.addWidget(self.rbRight)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.formLayout.setLayout(8, QFormLayout.FieldRole, self.horizontalLayout_4)


        self.verticalLayout.addLayout(self.formLayout)


        self.verticalLayout_2.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btnCancel = QPushButton(SettingDialog)
        self.btnCancel.setObjectName(u"btnCancel")

        self.horizontalLayout.addWidget(self.btnCancel)

        self.btnOk = QPushButton(SettingDialog)
        self.btnOk.setObjectName(u"btnOk")

        self.horizontalLayout.addWidget(self.btnOk)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        QWidget.setTabOrder(self.leImagePath, self.btnImagePath)
        QWidget.setTabOrder(self.btnImagePath, self.btnCancel)
        QWidget.setTabOrder(self.btnCancel, self.btnOk)

        self.retranslateUi(SettingDialog)

        self.btnOk.setDefault(True)


        QMetaObject.connectSlotsByName(SettingDialog)
    # setupUi

    def retranslateUi(self, SettingDialog):
        SettingDialog.setWindowTitle(QCoreApplication.translate("SettingDialog", u"\uc124\uc815", None))
        self.label.setText(QCoreApplication.translate("SettingDialog", u"\ubaa8\ub2c8\ud130 \ubc88\ud638", None))
        self.label_2.setText(QCoreApplication.translate("SettingDialog", u"\uc911\ubcf5 \uc774\ubbf8\uc9c0 \uc911\ub2e8", None))
        self.lbSameCount.setText(QCoreApplication.translate("SettingDialog", u"10", None))
        self.label_4.setText(QCoreApplication.translate("SettingDialog", u"\ucd5c\ub300 \ud398\uc774\uc9c0", None))
        self.label_5.setText(QCoreApplication.translate("SettingDialog", u"\uc774\ubbf8\uc9c0 \uc800\uc7a5 \uacbd\ub85c", None))
        self.btnImagePath.setText(QCoreApplication.translate("SettingDialog", u"\uc120\ud0dd", None))
        self.label_6.setText(QCoreApplication.translate("SettingDialog", u"PDF \uc800\uc7a5\uacbd\ub85c", None))
        self.btnPdfPath.setText(QCoreApplication.translate("SettingDialog", u"\uc120\ud0dd", None))
        self.label_3.setText(QCoreApplication.translate("SettingDialog", u"\uc774\ubbf8\uc9c0 \uc555\ucd95\uc728", None))
        self.sbImageCompress.setSuffix(QCoreApplication.translate("SettingDialog", u"%", None))
        self.label_7.setText(QCoreApplication.translate("SettingDialog", u"\uc774\ubbf8\uc9c0 \ucd5c\ub300 \uc0ac\uc774\uc988", None))
        self.sbImageSize.setSuffix(QCoreApplication.translate("SettingDialog", u"px", None))
        self.label_8.setText(QCoreApplication.translate("SettingDialog", u"\ub9c8\uc6b0\uc2a4 \ud720 \uac12", None))
        self.label_9.setText(QCoreApplication.translate("SettingDialog", u"\uc2a4\uc640\uc774\ud504 \ubc29\ud5a5", None))
        self.rbLeft.setText(QCoreApplication.translate("SettingDialog", u"Left", None))
        self.rbRight.setText(QCoreApplication.translate("SettingDialog", u"Right", None))
        self.btnCancel.setText(QCoreApplication.translate("SettingDialog", u"\ucde8\uc18c", None))
        self.btnOk.setText(QCoreApplication.translate("SettingDialog", u"\ud655\uc778", None))
    # retranslateUi

