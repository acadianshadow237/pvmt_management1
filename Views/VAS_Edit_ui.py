# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VAS_Edit_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_VAS_EditForm(QWidget):
    def setupUi(self, VAS_EditForm):
        if not VAS_EditForm.objectName():
            VAS_EditForm.setObjectName(u"VAS_EditForm")
        VAS_EditForm.setWindowModality(Qt.WindowModal)
        VAS_EditForm.resize(1019, 560)
        self.verticalLayout_2 = QVBoxLayout(VAS_EditForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.labelCounty = QLabel(VAS_EditForm)
        self.labelCounty.setObjectName(u"labelCounty")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCounty.sizePolicy().hasHeightForWidth())
        self.labelCounty.setSizePolicy(sizePolicy)
        self.labelCounty.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setPointSize(12)
        self.labelCounty.setFont(font)

        self.horizontalLayout.addWidget(self.labelCounty)

        self.countytextEdit = QTextEdit(VAS_EditForm)
        self.countytextEdit.setObjectName(u"countytextEdit")
        self.countytextEdit.setMaximumSize(QSize(16777215, 30))
        self.countytextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.countytextEdit)

        self.labelRoute = QLabel(VAS_EditForm)
        self.labelRoute.setObjectName(u"labelRoute")
        sizePolicy.setHeightForWidth(self.labelRoute.sizePolicy().hasHeightForWidth())
        self.labelRoute.setSizePolicy(sizePolicy)
        self.labelRoute.setMaximumSize(QSize(16777215, 30))
        self.labelRoute.setFont(font)

        self.horizontalLayout.addWidget(self.labelRoute)

        self.routetextEdit = QTextEdit(VAS_EditForm)
        self.routetextEdit.setObjectName(u"routetextEdit")
        self.routetextEdit.setMaximumSize(QSize(16777215, 30))
        self.routetextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.routetextEdit)

        self.labelCounty_2 = QLabel(VAS_EditForm)
        self.labelCounty_2.setObjectName(u"labelCounty_2")
        sizePolicy.setHeightForWidth(self.labelCounty_2.sizePolicy().hasHeightForWidth())
        self.labelCounty_2.setSizePolicy(sizePolicy)
        self.labelCounty_2.setMaximumSize(QSize(16777215, 30))
        self.labelCounty_2.setFont(font)

        self.horizontalLayout.addWidget(self.labelCounty_2)

        self.fromtextEdit = QTextEdit(VAS_EditForm)
        self.fromtextEdit.setObjectName(u"fromtextEdit")
        self.fromtextEdit.setMaximumSize(QSize(16777215, 30))
        self.fromtextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.fromtextEdit)

        self.labelDirection = QLabel(VAS_EditForm)
        self.labelDirection.setObjectName(u"labelDirection")
        sizePolicy.setHeightForWidth(self.labelDirection.sizePolicy().hasHeightForWidth())
        self.labelDirection.setSizePolicy(sizePolicy)
        self.labelDirection.setMaximumSize(QSize(16777215, 30))
        self.labelDirection.setFont(font)

        self.horizontalLayout.addWidget(self.labelDirection)

        self.totextEdit = QTextEdit(VAS_EditForm)
        self.totextEdit.setObjectName(u"totextEdit")
        self.totextEdit.setMaximumSize(QSize(16777215, 30))
        self.totextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.totextEdit)

        self.labelCounty_3 = QLabel(VAS_EditForm)
        self.labelCounty_3.setObjectName(u"labelCounty_3")
        sizePolicy.setHeightForWidth(self.labelCounty_3.sizePolicy().hasHeightForWidth())
        self.labelCounty_3.setSizePolicy(sizePolicy)
        self.labelCounty_3.setMaximumSize(QSize(16777215, 30))
        self.labelCounty_3.setFont(font)

        self.horizontalLayout.addWidget(self.labelCounty_3)

        self.pasidtextEdit = QTextEdit(VAS_EditForm)
        self.pasidtextEdit.setObjectName(u"pasidtextEdit")
        self.pasidtextEdit.setMaximumSize(QSize(16777215, 30))
        self.pasidtextEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.pasidtextEdit)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 2)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 2)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 2)
        self.horizontalLayout.setStretch(8, 1)
        self.horizontalLayout.setStretch(9, 4)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.vastableWidget = QTableWidget(VAS_EditForm)
        self.vastableWidget.setObjectName(u"vastableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.vastableWidget.sizePolicy().hasHeightForWidth())
        self.vastableWidget.setSizePolicy(sizePolicy1)
        self.vastableWidget.setFont(font)

        self.verticalLayout.addWidget(self.vastableWidget)

        self.buttonBox = QDialogButtonBox(VAS_EditForm)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 60)

        self.retranslateUi(VAS_EditForm)
        self.buttonBox.accepted.connect(VAS_EditForm.show)

        QMetaObject.connectSlotsByName(VAS_EditForm)
    # setupUi

    def retranslateUi(self, VAS_EditForm):
        VAS_EditForm.setWindowTitle(QCoreApplication.translate("VAS_EditForm", u"Analysis Section Edit", None))
        self.labelCounty.setText(QCoreApplication.translate("VAS_EditForm", u"County:", None))
        self.labelRoute.setText(QCoreApplication.translate("VAS_EditForm", u"Route:", None))
        self.labelCounty_2.setText(QCoreApplication.translate("VAS_EditForm", u"From:", None))
        self.labelDirection.setText(QCoreApplication.translate("VAS_EditForm", u"To", None))
        self.labelCounty_3.setText(QCoreApplication.translate("VAS_EditForm", u"<html><head/><body><p align=\"center\">PAS ID:</p></body></html>", None))
    # retranslateUi

