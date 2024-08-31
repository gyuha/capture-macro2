# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'command_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_CommandWidget(object):
    def setupUi(self, CommandWidget):
        if not CommandWidget.objectName():
            CommandWidget.setObjectName(u"CommandWidget")
        CommandWidget.resize(600, 304)
        CommandWidget.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(CommandWidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox = QGroupBox(CommandWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.macroTable = QTableWidget(self.groupBox)
        if (self.macroTable.columnCount() < 4):
            self.macroTable.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.macroTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.macroTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.macroTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.macroTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.macroTable.setObjectName(u"macroTable")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.macroTable.sizePolicy().hasHeightForWidth())
        self.macroTable.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(False)
        self.macroTable.setFont(font)
        self.macroTable.setRowCount(0)
        self.macroTable.verticalHeader().setVisible(True)
        self.macroTable.verticalHeader().setHighlightSections(True)

        self.verticalLayout.addWidget(self.macroTable)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnCommandInsert = QPushButton(self.groupBox)
        self.btnCommandInsert.setObjectName(u"btnCommandInsert")

        self.horizontalLayout_4.addWidget(self.btnCommandInsert)

        self.btnCommandAdd = QPushButton(self.groupBox)
        self.btnCommandAdd.setObjectName(u"btnCommandAdd")

        self.horizontalLayout_4.addWidget(self.btnCommandAdd)

        self.btnCommandRemove = QPushButton(self.groupBox)
        self.btnCommandRemove.setObjectName(u"btnCommandRemove")

        self.horizontalLayout_4.addWidget(self.btnCommandRemove)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.groupBox)


        self.retranslateUi(CommandWidget)

        QMetaObject.connectSlotsByName(CommandWidget)
    # setupUi

    def retranslateUi(self, CommandWidget):
        CommandWidget.setWindowTitle(QCoreApplication.translate("CommandWidget", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("CommandWidget", u"\uc218\ud589", None))
        ___qtablewidgetitem = self.macroTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("CommandWidget", u"\uba85\ub839\uc5b4", None));
        ___qtablewidgetitem1 = self.macroTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("CommandWidget", u"\uac12", None));
        ___qtablewidgetitem2 = self.macroTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("CommandWidget", u"\ub3d9\uc791", None));
        ___qtablewidgetitem3 = self.macroTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("CommandWidget", u"\ub3d9\uc7912", None));
        self.btnCommandInsert.setText(QCoreApplication.translate("CommandWidget", u"\uba85\ub839\uc5b4 \uc0bd\uc785", None))
        self.btnCommandAdd.setText(QCoreApplication.translate("CommandWidget", u"\uba85\ub839\uc5b4 \ucd94\uac00", None))
        self.btnCommandRemove.setText(QCoreApplication.translate("CommandWidget", u"\uba85\ub839\uc5b4 \uc0ad\uc81c", None))
    # retranslateUi

