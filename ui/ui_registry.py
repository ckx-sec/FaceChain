# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registry.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RegistryWidget(object):
    def setupUi(self, RegistryWidget):
        if not RegistryWidget.objectName():
            RegistryWidget.setObjectName(u"RegistryWidget")
        RegistryWidget.resize(253, 234)
        self.verticalLayout = QVBoxLayout(RegistryWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblType = QLabel(RegistryWidget)
        self.lblType.setObjectName(u"lblType")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblType)

        self.comboBox = QComboBox(RegistryWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.lblNodename = QLabel(RegistryWidget)
        self.lblNodename.setObjectName(u"lblNodename")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblNodename)

        self.lineEditNodename = QLineEdit(RegistryWidget)
        self.lineEditNodename.setObjectName(u"lineEditNodename")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditNodename)

        self.lblPort = QLabel(RegistryWidget)
        self.lblPort.setObjectName(u"lblPort")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblPort)

        self.lineEditPort = QLineEdit(RegistryWidget)
        self.lineEditPort.setObjectName(u"lineEditPort")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEditPort)

        self.lblIP = QLabel(RegistryWidget)
        self.lblIP.setObjectName(u"lblIP")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblIP)

        self.lineEditIP = QLineEdit(RegistryWidget)
        self.lineEditIP.setObjectName(u"lineEditIP")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEditIP)


        self.verticalLayout.addLayout(self.formLayout)

        self.btnGo = QPushButton(RegistryWidget)
        self.btnGo.setObjectName(u"btnGo")

        self.verticalLayout.addWidget(self.btnGo)

        QWidget.setTabOrder(self.comboBox, self.lineEditNodename)
        QWidget.setTabOrder(self.lineEditNodename, self.lineEditIP)
        QWidget.setTabOrder(self.lineEditIP, self.lineEditPort)
        QWidget.setTabOrder(self.lineEditPort, self.btnGo)

        self.retranslateUi(RegistryWidget)

        QMetaObject.connectSlotsByName(RegistryWidget)
    # setupUi

    def retranslateUi(self, RegistryWidget):
        RegistryWidget.setWindowTitle(QCoreApplication.translate("RegistryWidget", u"Registry", None))
        self.lblType.setText(QCoreApplication.translate("RegistryWidget", u"Type", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("RegistryWidget", u"Data node", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("RegistryWidget", u"Company node", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("RegistryWidget", u"Consensus node", None))

        self.lblNodename.setText(QCoreApplication.translate("RegistryWidget", u"Nodename", None))
        self.lineEditNodename.setPlaceholderText(QCoreApplication.translate("RegistryWidget", u"dat1", None))
        self.lblPort.setText(QCoreApplication.translate("RegistryWidget", u"Port", None))
        self.lineEditPort.setPlaceholderText(QCoreApplication.translate("RegistryWidget", u"3001", None))
        self.lblIP.setText(QCoreApplication.translate("RegistryWidget", u"IP", None))
        self.lineEditIP.setPlaceholderText(QCoreApplication.translate("RegistryWidget", u"127.0.0.1", None))
        self.btnGo.setText(QCoreApplication.translate("RegistryWidget", u"Go!", None))
    # retranslateUi

