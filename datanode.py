from enum import Enum
from typing import List, Union
from flask import Flask, abort, request
from flask.json import jsonify
import requests
import sys
import numpy as np
import ecdsa
import base64
import random
import time
import json
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from crypto.imageIPE import *
from IPFS.transfer import *
from instruction import *
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'handlers': {'wsgi': {
        'class': 'logging.NullHandler',
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


class DataNode:

    def __init__(self, name: str, port: int, company_addr: str):
        """
        Give a ip_addr,company_addr to create a wallet
        """
        self.port = port
        self.name = name
        self.company_addr = company_addr
        self.company_name = ''
        self.company_public_key = ''
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()
        self.mpk, self.msk = self.generate_DPIPE_keys()
        # images encrypt
        self.images = []
        self.train_images: list[tuple] = []
        self.test_images: list[tuple] = []
        self.sk = []
        # transaction hash
        self.mpk_hash = ''
        self.train_images_hash = ''
        self.test_images_hash = ''
        # wait for receive
        self.z = []

        self.server = Flask(__name__)

        @self.server.route('/DP-Face/get_z', methods=['POST'])
        def get_z():
            request_data = json.loads(request.get_data().decode('utf-8'))
            self.z = request_data['z']
            if self.z != '':
                print("[ Successfully get z from company ]")
                return jsonify(request_data)
            else:
                print("[ There are some error to get z from company ]")
                return jsonify(request_data)

        @self.server.route('/DP-Face/get_company_pk', methods=['POST'])
        def get_company_pk():
            request_data = json.loads(request.get_data().decode('utf-8'))
            self.company_name = request_data['company_name']
            self.company_public_key = request_data['company_public_key']
            print("[ get the company info ]")
            return jsonify(request_data)

    def serve(self):
        self.flask_thread = threading.Thread(target=lambda: self.server.run(
            host='0.0.0.0', port=self.port))
        self.flask_thread.daemon = True
        self.flask_thread.start()

    def stop(self):
        pass

    def generate_ECDSA_keys(self):
        """
        To generate Wallet key-pairs 

        Return public_key(base64) and private_key
        """
        sk = ecdsa.SigningKey.generate(
            curve=ecdsa.SECP256k1)  # this is your sign (private key)
        private_key = sk.to_string().hex()  # convert your private key to hex
        vk = sk.get_verifying_key()  # this is your verification key (public key)
        public_key = vk.to_string().hex()
        public_key = base64.b64encode(bytes.fromhex(public_key))

        filename = "./wallet/datanode/{}.txt".format(self.name)
        with open(filename, "w+") as f:
            f.write(
                "Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print(
            "\n[ Your new address and private key are now in the file {0} ]".format(filename))
        return public_key.decode(), private_key

    def generate_DPIPE_keys(self, g=1.0001):
        """
        To generate Inner-Product-Encryption key-pairs

        Return mpk,msk
        """
        msk = s = [random.random() for _ in range(512)]
        mpk = h = [pow(g, si) for si in s]
        return mpk, msk

    def sign_ECDSA_msg(self):
        # Get timestamp, round it, make it into a string and encode it to bytes
        message = str(round(time.time()))
        bmessage = message.encode()
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(
            self.private_key), curve=ecdsa.SECP256k1)
        signature = base64.b64encode(sk.sign(bmessage))
        return signature, message

    def upload_images(self):
        """
        To upload the images

        Return boolean
        """
        for p in range(10):
            image = []
            f = csv.reader(open('./images/feature{}.csv'.format(p)))
            for row in f:
                image.append(list(map(lambda x: float(x), row)))
            #w.append([j for j in range(512)])
            self.images.append(image)
        return True

    def classify_images_set(self, images):
        """
        classify then with train set and test set

        Return boolean 
        """
        self.train_images = images[:8]
        self.test_images = images[8:10]
        return True

    def encrypt_images(self,):
        """
        To do DP and Inner-Product-Encrypt (image is 18*512 Matrix)

        Return a 18*512 Matrix encrypted_image
        """
        encrypt_images: list[tuple] = []
        u1 = np.random.random()
        u2 = np.random.random()
        for image in self.images:
            image_DP = laplace_mech(image, u1, u2)
            print("[DP Done.]")
            ct0, ctx = encrypt(image_DP, self.mpk)
            print("[Encrypt image Done.]")
            encrypt_images.append((ct0, ctx))

        return encrypt_images

    def get_image_hash(self):
        # encrypt images
        encrypt_images = self.encrypt_images()
        # classify
        self.classify_images_set(encrypt_images)
        # store in IPFS
        self.test_images_hash = store_in_IPFS(
            self.public_key, self.test_images)
        self.train_images_hash = store_in_IPFS(
            self.public_key, self.train_images)

    def send_transaction(self):
        if len(self.private_key) == 64:
            signature, message = self.sign_ECDSA_msg()
            miner_url = read_in_consensusinfo()
            for consensusnode in miner_url:
                url = f'http://{consensusnode}/DP-Face/txion'
                payload = {"from": self.public_key,
                           "to": self.company_public_key,
                           "mpk_hash": self.mpk_hash,
                           "test_images_hash": self.test_images_hash,
                           "train_images_hash": self.train_images_hash,
                           "signature": signature.decode(),
                           "message": message}
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)

            url = f"http://{self.company_addr}/DP-Face/collect_hash"
            payload = {"public_key": self.public_key,
                       "mpk_hash": self.mpk_hash,
                       "test_images_hash": self.test_images_hash,
                       "train_images_hash": self.train_images_hash
                       }
            headers = {"Content-Type": "application/json"}
            res = requests.post(url, json=payload, headers=headers)
            print(res.text)
        else:
            print("Wrong address or key length! Verify and try again.")

    def send_sk(self):
        if self.z != []:
            self.sk = keyGenerate(self.z, self.msk)
            sk = self.sk
            # TODO 加密传输信息
            url = f"http://{self.company_addr}/DP-Face/collect_sk"
            payload = {"datanode_public_key": self.public_key, "sk": self.sk}
            headers = {"Content-Type": "application/json"}

            res = requests.post(url, json=payload, headers=headers)
            print(res.text)
        else:
            print("[ z is empty ]")


def register():
    datanode_intro()
    print("            ==================              ")
    print("           |     register     |             ")
    print("            ==================              ")
    print("============================================")
    name = input('Please input your name: ')
    port = input('Please input web port: ')
    company_addr = input('Please input the company ip_addr belonged: ')
    print("============================================")
    datanode = DataNode(name, f'127.0.0.1:{port}', company_addr)
    print('[ Success for creating accounts ]\n\n')
    return datanode


def init(datanode: DataNode):
    response = None
    while response not in ["1", "2", "3", "4", "5"]:
        print("            ==================              ")
        print("           |    application   |             ")
        print("            ==================              ")
        response = input("""============================================
What do you want to do?
1. Connect with company to send pk
2. Store the mpk in IPFS
3. Upload the encrypted image and store the images in IPFS
4. Send transactions (give companynode the hash)
5. Wait for z and then send sk back
6. Quit
============================================\nchoose: """)

        if response == '1':
            try:
                url = f"http://{datanode.company_addr}/DP-Face/get_employee"
                payload = {
                    "name": datanode.name,
                    "public_key": datanode.public_key,
                    "port": datanode.port
                }
                res = requests.post(url, json=payload)
                print(res.text)
            except:
                print("[ send datanode_info error]")

        elif response == '2':
            datanode.mpk_hash = store_in_IPFS(
                datanode.public_key, datanode.mpk)
            if datanode.mpk_hash != '':
                print('[ Success for storing the mpk ]')
            else:
                print('[ Store mpk Error. Rollback... ]')

        elif response == '3':
            if(datanode.upload_images()):
                print('[ Success for uploading images ]')
                datanode.get_image_hash()
                if datanode.test_images_hash != '' and datanode.train_images_hash != '':
                    print('[ Success for storing the test and train hash ]')
                else:
                    print('[ Store images Error. Rollback... ]')
                    datanode.test_images_hash = ''
                    datanode.train_images_hash = ''
            else:
                print('[ Upload images error ]')

        elif response == "4":
            if datanode.company_public_key == '':
                print('[ Have no company belong to now ]')

            else:
                print("============================================")
                print("From: {0}\nPrivate Key: {1}\nTo: {2}\nMPK_hash: {3}\nTraining_Images_hash: {4}\nTest_Images_hash: {5}".format(
                    datanode.public_key, datanode.private_key, datanode.company_public_key, datanode.mpk_hash, datanode.train_images_hash, datanode.test_images_hash))
                print("============================================")
                response = input("y/n\n")
                if response.lower() == "y":
                    datanode.send_transaction()

        elif response == "5":
            print("[ Please wait for getting z ]")
            while(len(datanode.z) != 512):
                time.sleep(5)
            datanode.send_sk()
            print("[ sk send successfully ]")
        else:
            pass

        response = None


if __name__ == "__main__":
    datanode = register()
    datanode.serve()
    init(datanode)
