# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'consensusnode.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ConsensusWidget(object):
    def setupUi(self, ConsensusWidget):
        if not ConsensusWidget.objectName():
            ConsensusWidget.setObjectName(u"ConsensusWidget")
        ConsensusWidget.resize(508, 422)
        self.verticalLayout = QVBoxLayout(ConsensusWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(ConsensusWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btnShowInfo = QPushButton(self.groupBox)
        self.btnShowInfo.setObjectName(u"btnShowInfo")

        self.verticalLayout_2.addWidget(self.btnShowInfo)

        self.btnMine = QPushButton(self.groupBox)
        self.btnMine.setObjectName(u"btnMine")

        self.verticalLayout_2.addWidget(self.btnMine)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBoxLog = QGroupBox(ConsensusWidget)
        self.groupBoxLog.setObjectName(u"groupBoxLog")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBoxLog)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEditLog = QPlainTextEdit(self.groupBoxLog)
        self.plainTextEditLog.setObjectName(u"plainTextEditLog")

        self.horizontalLayout_11.addWidget(self.plainTextEditLog)


        self.verticalLayout.addWidget(self.groupBoxLog)


        self.retranslateUi(ConsensusWidget)

        QMetaObject.connectSlotsByName(ConsensusWidget)
    # setupUi

    def retranslateUi(self, ConsensusWidget):
        ConsensusWidget.setWindowTitle(QCoreApplication.translate("ConsensusWidget", u"Consensus node", None))
        self.groupBox.setTitle(QCoreApplication.translate("ConsensusWidget", u"Operation", None))
        self.btnShowInfo.setText(QCoreApplication.translate("ConsensusWidget", u"Show information", None))
        self.btnMine.setText(QCoreApplication.translate("ConsensusWidget", u"Mine", None))
        self.groupBoxLog.setTitle(QCoreApplication.translate("ConsensusWidget", u"Log", None))
    # retranslateUi

