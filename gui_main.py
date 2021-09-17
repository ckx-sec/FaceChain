import threading
from consensusnode import ConsensusNode, replace_print
from companynode import CompanyNode
import csv
import time
from typing import List
from IPFS.transfer import store_in_IPFS
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from ui import (Ui_RegistryWidget, Ui_DataWidget,
                Ui_CompanyWidget, Ui_ConsensusWidget)
from config.node_config import read_in_companyinfo, write_in_companyinfo, write_in_consensusinfo
from datanode import DataNode
import requests


class RegisterWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_RegistryWidget()
        self.ui.setupUi(self)
        self.ui.btnGo.clicked.connect(self.go)

        self.data_widget = None
        self.company_widget = None
        self.consensus_widget = None

    @Slot()
    def go(self):
        choice = self.ui.comboBox.currentIndex()
        nodename = self.ui.lineEditNodename.text()
        ip: str = self.ui.lineEditIP.text()
        port: str = None
        try:
            port = int(self.ui.lineEditPort.text())
        except Exception as e:
            print(e)
        if not nodename or not ip or not port:
            QMessageBox.information(
                self, 'Information incompelete', 'Please check your input.')
        else:
            print(f'choice:{choice} {self.ui.comboBox.currentText()}')
            print(f'name:{nodename}')
            print(f'ip:{ip}')
            print(f'port:{port}')
            # 0 datanode
            # 1 companynode
            # 2 consensusnode
            if choice == 0:
                self.data_widget = DataWidget(nodename, ip, port)
                self.data_widget.show()
            elif choice == 1:
                self.company_widget = CompanyWidget(nodename, ip, port)
                self.company_widget.show()
            elif choice == 2:
                self.consensus_widget = ConsensusWidget(nodename, ip, port)
                self.consensus_widget.show()
            self.close()


class DataWidget(QWidget):
    def __init__(self, name, ip, port, parent=None) -> None:
        super().__init__(parent)
        self.ui = Ui_DataWidget()
        self.ui.setupUi(self)
        self.node = None
        self.nodename: str = name
        self.port: int = port

        self.images: List[List[List[float]]] = []
        self.imagesModel = None

        self.ui.btnDetectCompanyIP.clicked.connect(self.detect_company_ip)
        self.ui.btnConnectCompany.clicked.connect(self.connect_company)
        self.ui.btnUploadMpk.clicked.connect(self.upload_mpk)

        self.ui.btnAddImage.clicked.connect(self.add_image)
        self.ui.btnDeleteImage.clicked.connect(self.delete_image)
        self.ui.btnUploadImage.clicked.connect(self.upload_images)

        self.ui.btnSendTransaction.clicked.connect(self.send_transaction)
        self.ui.btnGenerateSk.clicked.connect(self.generate_sk)

        # self.center()

    def log(self, message: str):
        self.ui.plainTextEditLog.appendPlainText(f'{time.asctime()} {message}')

    @Slot()
    def detect_company_ip(self):
        for line in read_in_companyinfo():
            self.ui.plainTextEditLog.appendPlainText(line)

    @Slot()
    def connect_company(self):
        assert self.nodename and self.port
        if not self.node:
            self.company_ip = self.ui.lineEditCompanyIP.text()
            self.node = DataNode(self.nodename, self.port, self.company_ip)
            self.node.serve()
        self.log("Connecting...")
        try:
            res = requests.post(f"http://{self.node.company_addr}/DP-Face/get_employee", json={
                "name": self.node.name,
                "public_key": self.node.public_key,
                "port": self.node.port
            })
            self.log(f'Response:\n{res.text}')
            self.ui.groupBoxUploadImage.setEnabled(True)
        except Exception as e:
            # self.log(traceback.format_exc())
            self.log(str(e))

            # temp
            self.ui.groupBoxUploadImage.setEnabled(True)

    @Slot()
    def add_image(self):
        files: List[str] = QFileDialog.getOpenFileNames(self,
                                                        caption="Select one or more images",
                                                        filter="Images (*.csv)")[0]
        # filter="Images (*.png *.xpm *.jpg)")
        if not self.imagesModel:
            self.imagesModel = QStringListModel()
            self.ui.listViewImages.setModel(self.imagesModel)
        stringList = self.imagesModel.stringList()
        for file in files:
            if file not in stringList:
                stringList.append(file)
        self.imagesModel.setStringList(stringList)

    @Slot()
    def delete_image(self):
        for index in reversed(sorted(self.ui.listViewImages.selectedIndexes())):
            index: QModelIndex
            self.imagesModel.removeRow(index.row())
            # self.ui.listWidgetImages.removeItemWidget(item)

    @Slot()
    def upload_images(self):
        for filename in self.imagesModel.stringList():
            image = []
            for row in csv.reader(open(filename)):
                image.append(list(map(lambda x: float(x), row)))
            # w.append([j for j in range(512)])
            self.images.append(image)
        try:
            self.node.get_image_hash()
            self.log('Successfully uploaded images')
            self.ui.groupBoxUploadMpk.setEnabled(True)
        except Exception as e:
            self.log(str(e))

    @Slot()
    def upload_mpk(self):
        self.node.mpk_hash = store_in_IPFS(self.node.public_key, self.node.mpk)
        if self.node.mpk_hash != '':
            self.log('Successfully uploaded mpk')
        else:
            self.log('Failed to upload mpk')
        self.ui.groupBoxSendTransaction.setEnabled(True)

    @Slot()
    def send_transaction(self):
        info = (f'From: {self.node.public_key}\n' +
                f'Private Key: {self.node.private_key}\n' +
                f'To: {self.node.company_public_key}\n' +
                f'MPK_hash: {self.node.mpk_hash}\n' +
                f'Training_Images_hash: {self.node.train_images_hash}\n' +
                f'Test_Images_hash: {self.node.test_images_hash}')
        choice = QMessageBox.question(
            self, 'Attention', f'Are you sure to send transaction to this company?\n{info}')
        if choice == QMessageBox.Yes:
            self.node.send_transaction()
            self.ui.groupBoxGenerateSk.setEnabled(True)

    @Slot()
    def generate_sk(self):
        self.log("Please wait for getting z")
        while(len(self.node.z) != 512):
            time.sleep(1)
        self.node.send_sk()
        self.log("Successfully sent sk")


class CompanyWidget(QWidget):
    def __init__(self, name, ip, port, parent=None):
        super().__init__(parent)
        self.ui = Ui_CompanyWidget()
        self.ui.setupUi(self)

        self.node = CompanyNode(name, f'{ip}:{port}', 0)
        write_in_companyinfo(f"{self.node.name} : {self.node.ip_addr}")

        self.ui.btnSetEmployeeNumber.clicked.connect(self.set_employee_count)
        self.ui.btnCheck.clicked.connect(self.check_nodes)
        self.ui.btnCollect.clicked.connect(self.collect_hash)
        self.ui.btnSendZ.clicked.connect(self.send_z)
        self.ui.btnReleaseTask.clicked.connect(self.release_task)
        self.ui.btnReceiveModel.clicked.connect(self.receive_model)
        # self.center()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def log(self, message: str):
        self.ui.plainTextEditLog.appendPlainText(f'{time.asctime()} {message}')

    @Slot()
    def set_employee_count(self):
        self.node.set_employee_count(self.ui.spinBox.value())
        self.node.serve()
        self.ui.groupBoxCheck.setEnabled(True)

    @Slot()
    def check_nodes(self):
        self.log("Collecting employees info...")
        while(len(self.node.employeelist) < self.node.employee_count):
            time.sleep(1)
        self.log("Success.")
        self.ui.groupBoxCollect.setEnabled(True)

    @Slot()
    def collect_hash(self):
        self.log("Waiting for employees...")
        while(len(self.node.mpks_hash) != len(self.node.employeelist)):
            time.sleep(1)
        if(len(self.node.mpks_hash) == len(self.node.train_images_hash_list) == len(self.node.test_images_hash_list)):
            self.log("Success.")
            self.ui.groupBoxSendZ.setEnabled(True)
        else:
            self.log("Failure.")
            print("[ hashs are not enough. Rollback... ]")
            self.node.mpks_hash = []
            self.node.train_images_hash_list = []
            self.node.test_images_hash_list = []

    @Slot()
    def send_z(self):
        if(self.node.padding_to_z()):
            self.log("Broadcasting to employees")
            if(self.node.broadcast_z()):
                self.log("Success. Waiting for sk")
                while(len(self.node.sks) != len(self.node.employeelist)):
                    time.sleep(1)
                self.log("Success.")
            else:
                self.log("[ Broadcast error ]")
        else:
            self.log("[ Please pad z again ]")
        self.ui.groupBoxReleaseTask.setEnabled(True)

    @Slot()
    def release_task(self):
        if(self.node.release_task()):
            self.log("Release task: Success")
        else:
            self.log("Release tasks error")
        self.ui.groupBoxReceiveModel.setEnabled(True)

    @Slot()
    def receive_model(self):
        self.log("Waiting for model")
        QApplication.processEvents()
        while(self.node.model == ''):
            time.sleep(1)
        self.log("Success.")
        self.log("Model data:")
        self.log(str(self.node.model))


class ConsensusWidget(QWidget):
    def __init__(self, name, ip, port, parent=None):
        super().__init__(parent)
        replace_print(self.log)
        self.ui = Ui_ConsensusWidget()
        self.ui.setupUi(self)
        self.node = ConsensusNode(name, f'{ip}:{port}')

        write_in_consensusinfo(f"{self.node.ip_addr}")
        self.node.update_blockchain()

        self.ui.btnShowInfo.clicked.connect(self.show_info)
        self.ui.btnMine.clicked.connect(self.mine)

        self.node.serve()

        # self.center()

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def log(self, message: str):
        self.ui.plainTextEditLog.appendPlainText(f'{time.asctime()} {message}')

    @Slot()
    def show_info(self):
        self.log(self.node.show_information())

    @Slot()
    def mine(self):
        def _mine():
            while True:
                self.node.mine()
        self.mine_thread = threading.Thread(target=_mine)
        self.mine_thread.setDaemon(True)
        self.mine_thread.start()
        self.ui.btnMine.setDisabled(True)


if __name__ == '__main__':
    app = QApplication([])
    w = RegisterWidget()
    w.show()
    app.exec_()
