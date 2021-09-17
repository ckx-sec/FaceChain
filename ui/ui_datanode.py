# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'datanode.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_DataWidget(object):
    def setupUi(self, DataWidget):
        if not DataWidget.objectName():
            DataWidget.setObjectName(u"DataWidget")
        DataWidget.setEnabled(True)
        DataWidget.resize(577, 681)
        self.verticalLayout_3 = QVBoxLayout(DataWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBoxConnect = QGroupBox(DataWidget)
        self.groupBoxConnect.setObjectName(u"groupBoxConnect")
        self.groupBoxConnect.setEnabled(True)
        self.horizontalLayout = QHBoxLayout(self.groupBoxConnect)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lblCompanyIP = QLabel(self.groupBoxConnect)
        self.lblCompanyIP.setObjectName(u"lblCompanyIP")

        self.horizontalLayout.addWidget(self.lblCompanyIP)

        self.lineEditCompanyIP = QLineEdit(self.groupBoxConnect)
        self.lineEditCompanyIP.setObjectName(u"lineEditCompanyIP")

        self.horizontalLayout.addWidget(self.lineEditCompanyIP)

        self.btnDetectCompanyIP = QPushButton(self.groupBoxConnect)
        self.btnDetectCompanyIP.setObjectName(u"btnDetectCompanyIP")

        self.horizontalLayout.addWidget(self.btnDetectCompanyIP)

        self.btnConnectCompany = QPushButton(self.groupBoxConnect)
        self.btnConnectCompany.setObjectName(u"btnConnectCompany")

        self.horizontalLayout.addWidget(self.btnConnectCompany)


        self.horizontalLayout_6.addWidget(self.groupBoxConnect)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBoxUploadImage = QGroupBox(DataWidget)
        self.groupBoxUploadImage.setObjectName(u"groupBoxUploadImage")
        self.groupBoxUploadImage.setEnabled(False)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBoxUploadImage)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.listViewImages = QListView(self.groupBoxUploadImage)
        self.listViewImages.setObjectName(u"listViewImages")
        self.listViewImages.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout_4.addWidget(self.listViewImages)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btnAddImage = QPushButton(self.groupBoxUploadImage)
        self.btnAddImage.setObjectName(u"btnAddImage")

        self.verticalLayout.addWidget(self.btnAddImage)

        self.btnDeleteImage = QPushButton(self.groupBoxUploadImage)
        self.btnDeleteImage.setObjectName(u"btnDeleteImage")

        self.verticalLayout.addWidget(self.btnDeleteImage)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnUploadImage = QPushButton(self.groupBoxUploadImage)
        self.btnUploadImage.setObjectName(u"btnUploadImage")

        self.verticalLayout.addWidget(self.btnUploadImage)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.horizontalLayout_7.addWidget(self.groupBoxUploadImage)

        self.horizontalLayout_7.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.groupBoxUploadMpk = QGroupBox(DataWidget)
        self.groupBoxUploadMpk.setObjectName(u"groupBoxUploadMpk")
        self.groupBoxUploadMpk.setEnabled(False)
        self.horizontalLayout_5 = QHBoxLayout(self.groupBoxUploadMpk)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btnUploadMpk = QPushButton(self.groupBoxUploadMpk)
        self.btnUploadMpk.setObjectName(u"btnUploadMpk")

        self.horizontalLayout_5.addWidget(self.btnUploadMpk)


        self.horizontalLayout_10.addWidget(self.groupBoxUploadMpk)

        self.groupBoxSendTransaction = QGroupBox(DataWidget)
        self.groupBoxSendTransaction.setObjectName(u"groupBoxSendTransaction")
        self.groupBoxSendTransaction.setEnabled(False)
        self.horizontalLayout_8 = QHBoxLayout(self.groupBoxSendTransaction)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.btnSendTransaction = QPushButton(self.groupBoxSendTransaction)
        self.btnSendTransaction.setObjectName(u"btnSendTransaction")

        self.horizontalLayout_8.addWidget(self.btnSendTransaction)


        self.horizontalLayout_10.addWidget(self.groupBoxSendTransaction)

        self.groupBoxGenerateSk = QGroupBox(DataWidget)
        self.groupBoxGenerateSk.setObjectName(u"groupBoxGenerateSk")
        self.groupBoxGenerateSk.setEnabled(False)
        self.horizontalLayout_9 = QHBoxLayout(self.groupBoxGenerateSk)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.btnGenerateSk = QPushButton(self.groupBoxGenerateSk)
        self.btnGenerateSk.setObjectName(u"btnGenerateSk")

        self.horizontalLayout_9.addWidget(self.btnGenerateSk)


        self.horizontalLayout_10.addWidget(self.groupBoxGenerateSk)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.groupBoxLog = QGroupBox(DataWidget)
        self.groupBoxLog.setObjectName(u"groupBoxLog")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBoxLog)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEditLog = QPlainTextEdit(self.groupBoxLog)
        self.plainTextEditLog.setObjectName(u"plainTextEditLog")

        self.horizontalLayout_11.addWidget(self.plainTextEditLog)


        self.verticalLayout_3.addWidget(self.groupBoxLog)

        self.verticalLayout_3.setStretch(3, 1)
        QWidget.setTabOrder(self.lineEditCompanyIP, self.btnDetectCompanyIP)
        QWidget.setTabOrder(self.btnDetectCompanyIP, self.btnConnectCompany)
        QWidget.setTabOrder(self.btnConnectCompany, self.listViewImages)
        QWidget.setTabOrder(self.listViewImages, self.btnAddImage)
        QWidget.setTabOrder(self.btnAddImage, self.btnDeleteImage)
        QWidget.setTabOrder(self.btnDeleteImage, self.btnUploadImage)
        QWidget.setTabOrder(self.btnUploadImage, self.btnUploadMpk)
        QWidget.setTabOrder(self.btnUploadMpk, self.btnSendTransaction)
        QWidget.setTabOrder(self.btnSendTransaction, self.btnGenerateSk)
        QWidget.setTabOrder(self.btnGenerateSk, self.plainTextEditLog)

        self.retranslateUi(DataWidget)

        QMetaObject.connectSlotsByName(DataWidget)
    # setupUi

    def retranslateUi(self, DataWidget):
        DataWidget.setWindowTitle(QCoreApplication.translate("DataWidget", u"Data node", None))
        self.groupBoxConnect.setTitle(QCoreApplication.translate("DataWidget", u"Connect to company", None))
        self.lblCompanyIP.setText(QCoreApplication.translate("DataWidget", u"Company IP", None))
        self.lineEditCompanyIP.setPlaceholderText(QCoreApplication.translate("DataWidget", u"127.0.0.1:4001", None))
        self.btnDetectCompanyIP.setText(QCoreApplication.translate("DataWidget", u"Detect", None))
        self.btnConnectCompany.setText(QCoreApplication.translate("DataWidget", u"Connect", None))
        self.groupBoxUploadImage.setTitle(QCoreApplication.translate("DataWidget", u"Upload images", None))
        self.btnAddImage.setText(QCoreApplication.translate("DataWidget", u"Add", None))
        self.btnDeleteImage.setText(QCoreApplication.translate("DataWidget", u"Delete", None))
        self.btnUploadImage.setText(QCoreApplication.translate("DataWidget", u"Upload", None))
        self.groupBoxUploadMpk.setTitle(QCoreApplication.translate("DataWidget", u"Upload mpk to IPFS", None))
        self.btnUploadMpk.setText(QCoreApplication.translate("DataWidget", u"Upload", None))
        self.groupBoxSendTransaction.setTitle(QCoreApplication.translate("DataWidget", u"Send transactions", None))
        self.btnSendTransaction.setText(QCoreApplication.translate("DataWidget", u"Send", None))
        self.groupBoxGenerateSk.setTitle(QCoreApplication.translate("DataWidget", u"Generate sk", None))
        self.btnGenerateSk.setText(QCoreApplication.translate("DataWidget", u"Generate", None))
        self.groupBoxLog.setTitle(QCoreApplication.translate("DataWidget", u"Log", None))
    # retranslateUi

