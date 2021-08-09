# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'VAS_MENU.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1253, 866)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName(u"actionLogout")
        self.actionAnalysis_Sections = QAction(MainWindow)
        self.actionAnalysis_Sections.setObjectName(u"actionAnalysis_Sections")
        self.actionConstruction_Rehab_History = QAction(MainWindow)
        self.actionConstruction_Rehab_History.setObjectName(u"actionConstruction_Rehab_History")
        self.actionConst_Rehab_Layer_Detail = QAction(MainWindow)
        self.actionConst_Rehab_Layer_Detail.setObjectName(u"actionConst_Rehab_Layer_Detail")
        self.actionProject = QAction(MainWindow)
        self.actionProject.setObjectName(u"actionProject")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionsplit = QAction(MainWindow)
        self.actionsplit.setObjectName(u"actionsplit")
        self.actionContents = QAction(MainWindow)
        self.actionContents.setObjectName(u"actionContents")
        self.actionVCRH_VCRLD_VPROJ = QAction(MainWindow)
        self.actionVCRH_VCRLD_VPROJ.setObjectName(u"actionVCRH_VCRLD_VPROJ")
        self.actionEdit_Layers = QAction(MainWindow)
        self.actionEdit_Layers.setObjectName(u"actionEdit_Layers")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1253, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionAnalysis_Sections)
        self.menuView.addAction(self.actionVCRH_VCRLD_VPROJ)
        self.menuView.addAction(self.actionConstruction_Rehab_History)
        self.menuView.addAction(self.actionConst_Rehab_Layer_Detail)
        self.menuView.addAction(self.actionProject)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionEdit_Layers)
        self.menuHelp.addAction(self.actionContents)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PVMT_SNAP editor", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionLogout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.actionAnalysis_Sections.setText(QCoreApplication.translate("MainWindow", u"Analysis Sections", None))
        self.actionConstruction_Rehab_History.setText(QCoreApplication.translate("MainWindow", u"Construction Rehab History", None))
        self.actionConst_Rehab_Layer_Detail.setText(QCoreApplication.translate("MainWindow", u"Const Rehab Layer Detail", None))
        self.actionProject.setText(QCoreApplication.translate("MainWindow", u"Project", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionsplit.setText(QCoreApplication.translate("MainWindow", u"Split", None))
        self.actionContents.setText(QCoreApplication.translate("MainWindow", u"Contents", None))
        self.actionVCRH_VCRLD_VPROJ.setText(QCoreApplication.translate("MainWindow", u"VCRH_VCRLD_VPROJ", None))
        self.actionEdit_Layers.setText(QCoreApplication.translate("MainWindow", u"Edit Layers", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

