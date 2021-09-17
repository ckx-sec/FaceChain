# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'companynode.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_CompanyWidget(object):
    def setupUi(self, CompanyWidget):
        if not CompanyWidget.objectName():
            CompanyWidget.setObjectName(u"CompanyWidget")
        CompanyWidget.resize(348, 565)
        self.verticalLayout_3 = QVBoxLayout(CompanyWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBoxSetEmployeeNumber = QGroupBox(CompanyWidget)
        self.groupBoxSetEmployeeNumber.setObjectName(u"groupBoxSetEmployeeNumber")
        self.horizontalLayout = QHBoxLayout(self.groupBoxSetEmployeeNumber)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox = QSpinBox(self.groupBoxSetEmployeeNumber)
        self.spinBox.setObjectName(u"spinBox")

        self.horizontalLayout.addWidget(self.spinBox)

        self.btnSetEmployeeNumber = QPushButton(self.groupBoxSetEmployeeNumber)
        self.btnSetEmployeeNumber.setObjectName(u"btnSetEmployeeNumber")

        self.horizontalLayout.addWidget(self.btnSetEmployeeNumber)

        self.horizontalLayout.setStretch(0, 1)

        self.verticalLayout_3.addWidget(self.groupBoxSetEmployeeNumber)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBoxCheck = QGroupBox(CompanyWidget)
        self.groupBoxCheck.setObjectName(u"groupBoxCheck")
        self.groupBoxCheck.setEnabled(False)
        self.verticalLayout_2 = QVBoxLayout(self.groupBoxCheck)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnCheck = QPushButton(self.groupBoxCheck)
        self.btnCheck.setObjectName(u"btnCheck")

        self.verticalLayout_2.addWidget(self.btnCheck)


        self.horizontalLayout_7.addWidget(self.groupBoxCheck)

        self.groupBoxCollect = QGroupBox(CompanyWidget)
        self.groupBoxCollect.setObjectName(u"groupBoxCollect")
        self.groupBoxCollect.setEnabled(False)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBoxCollect)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnCollect = QPushButton(self.groupBoxCollect)
        self.btnCollect.setObjectName(u"btnCollect")

        self.horizontalLayout_2.addWidget(self.btnCollect)


        self.horizontalLayout_7.addWidget(self.groupBoxCollect)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.groupBoxSendZ = QGroupBox(CompanyWidget)
        self.groupBoxSendZ.setObjectName(u"groupBoxSendZ")
        self.groupBoxSendZ.setEnabled(False)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBoxSendZ)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnSendZ = QPushButton(self.groupBoxSendZ)
        self.btnSendZ.setObjectName(u"btnSendZ")

        self.horizontalLayout_5.addWidget(self.btnSendZ)


        self.horizontalLayout_10.addWidget(self.groupBoxSendZ)

        self.groupBoxReleaseTask = QGroupBox(CompanyWidget)
        self.groupBoxReleaseTask.setObjectName(u"groupBoxReleaseTask")
        self.groupBoxReleaseTask.setEnabled(False)
        self.horizontalLayout_8 = QHBoxLayout(self.groupBoxReleaseTask)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btnReleaseTask = QPushButton(self.groupBoxReleaseTask)
        self.btnReleaseTask.setObjectName(u"btnReleaseTask")

        self.horizontalLayout_8.addWidget(self.btnReleaseTask)


        self.horizontalLayout_10.addWidget(self.groupBoxReleaseTask)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.groupBoxReceiveModel = QGroupBox(CompanyWidget)
        self.groupBoxReceiveModel.setObjectName(u"groupBoxReceiveModel")
        self.groupBoxReceiveModel.setEnabled(False)
        self.horizontalLayout_9 = QHBoxLayout(self.groupBoxReceiveModel)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btnReceiveModel = QPushButton(self.groupBoxReceiveModel)
        self.btnReceiveModel.setObjectName(u"btnReceiveModel")

        self.horizontalLayout_9.addWidget(self.btnReceiveModel)


        self.verticalLayout_3.addWidget(self.groupBoxReceiveModel)

        self.groupBoxLog = QGroupBox(CompanyWidget)
        self.groupBoxLog.setObjectName(u"groupBoxLog")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBoxLog)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEditLog = QPlainTextEdit(self.groupBoxLog)
        self.plainTextEditLog.setObjectName(u"plainTextEditLog")

        self.horizontalLayout_11.addWidget(self.plainTextEditLog)


        self.verticalLayout_3.addWidget(self.groupBoxLog)

        QWidget.setTabOrder(self.spinBox, self.btnSetEmployeeNumber)
        QWidget.setTabOrder(self.btnSetEmployeeNumber, self.btnCheck)
        QWidget.setTabOrder(self.btnCheck, self.btnCollect)
        QWidget.setTabOrder(self.btnCollect, self.btnSendZ)
        QWidget.setTabOrder(self.btnSendZ, self.btnReleaseTask)
        QWidget.setTabOrder(self.btnReleaseTask, self.btnReceiveModel)
        QWidget.setTabOrder(self.btnReceiveModel, self.plainTextEditLog)

        self.retranslateUi(CompanyWidget)

        QMetaObject.connectSlotsByName(CompanyWidget)
    # setupUi

    def retranslateUi(self, CompanyWidget):
        CompanyWidget.setWindowTitle(QCoreApplication.translate("CompanyWidget", u"Company node", None))
        self.groupBoxSetEmployeeNumber.setTitle(QCoreApplication.translate("CompanyWidget", u"Set employee number", None))
        self.btnSetEmployeeNumber.setText(QCoreApplication.translate("CompanyWidget", u"Apply", None))
        self.groupBoxCheck.setTitle(QCoreApplication.translate("CompanyWidget", u"Check Employees", None))
        self.btnCheck.setText(QCoreApplication.translate("CompanyWidget", u"Check", None))
        self.groupBoxCollect.setTitle(QCoreApplication.translate("CompanyWidget", u"Collect hash", None))
        self.btnCollect.setText(QCoreApplication.translate("CompanyWidget", u"Collect", None))
        self.groupBoxSendZ.setTitle(QCoreApplication.translate("CompanyWidget", u"Send z && get sk", None))
        self.btnSendZ.setText(QCoreApplication.translate("CompanyWidget", u"Send", None))
        self.groupBoxReleaseTask.setTitle(QCoreApplication.translate("CompanyWidget", u"Release Task", None))
        self.btnReleaseTask.setText(QCoreApplication.translate("CompanyWidget", u"Release", None))
        self.groupBoxReceiveModel.setTitle(QCoreApplication.translate("CompanyWidget", u"Receive model", None))
        self.btnReceiveModel.setText(QCoreApplication.translate("CompanyWidget", u"Receive", None))
        self.groupBoxLog.setTitle(QCoreApplication.translate("CompanyWidget", u"Log", None))
    # retranslateUi

