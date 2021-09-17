from flask.json import jsonify
import ecdsa
import base64
import random
import time
from flask import Flask, request
import json
import requests
import threading
from crypto.imageIPE import *
from IPFS.transfer import *
from instruction import *
from blockchain import *
from logging.config import dictConfig
'''
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
'''

company = Flask(__name__)


class CompanyNode:
    # TODO datanode数量
    def __init__(self, name, ip_addr, employee_count):
        self.name = name
        self.ip_addr = ip_addr
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()

        self.employeelist = []
        self.mpks_hash = []
        self.mpks = []
        self.z = []
        self.sks = []
        self.train_images_hash_list = []
        self.test_images_hash_list = []
        self.task = {}
        self.flag = False
        self.model = ''

        self.server = Flask(__name__)

        @self.server.route('/DP-Face/get_employee', methods=['POST'])
        def get_employee():
            request_data = request.json
            self.employeelist.append({
                "name": request_data['name'],
                "public_key": request_data['public_key'],
                "url": f"{request.remote_addr}:{request_data['port']}"
            })
            payload = {
                "company_name": self.name,
                "company_public_key": self.public_key
            }
            res = requests.post(
                f"http://{request.remote_addr}:{request.json['port']}/DP-Face/get_company_pk", json=payload)
            # print(res.text)
            return f"[ Welcome to my company {self.name} ]"

        @self.server.route('/DP-Face/collect_hash', methods=['POST'])
        def collect_hash():
            request_data = json.loads(request.get_data().decode('utf-8'))
            self.mpks_hash.append(request_data['mpk_hash'])
            self.train_images_hash_list.append(
                request_data['train_images_hash'])
            self.test_images_hash_list.append(
                request_data['test_images_hash'])
            return "[ Receive your hashs successfully ]"

        @self.server.route('/DP-Face/collect_sk', methods=['POST'])
        def collect_sk():
            request_data = json.loads(request.get_data().decode('utf-8'))
            self.sks.append(
                {"public_key": request_data['datanode_public_key'], "sk": request_data['sk']})
            return "[ Receive your sk successfully ]"

        @self.server.route('/DP-Face/issue_sk', methods=['POST'])
        def issue_sk():
            request_data = json.loads(request.get_data().decode('utf-8'))
            if request_data == self.task:
                return json.dumps(self.sks)
            else:
                return "[ Ask sk False ]"

        @self.server.route('/DP-Face/release_test_hash', methods=['POST'])
        def release_test_hash():
            request_data = json.loads(request.get_data().decode('utf-8'))
            if request_data == self.task:
                return json.dumps(self.test_images_hash_list)
            else:
                return "[ Ask sk False ]"

        @self.server.route('/DP-Face/get_model', methods=['POST'])
        def get_model():
            model = json.loads(request.get_data().decode('utf-8'))
            print("[ Get the model ]")
            print(f"[ From: {model['name']} ]")
            print(f"[ Public Key: {model['public_key']} ]")

            self.model = model
            # miner_url = read_in_consensusinfo()
            # for node_url in miner_url:
            #     url = f"http://{node_url}/DP-Face/flag"
            #     payload = {"flag":True}
            #     headers = {"Content-Type": "application/json"}
            #     requests.post(url, json=payload, headers=headers)
            return "[ Receive successfully ]"
            # return "[ Refuse ]"

    def serve(self):
        self.flask_thread = threading.Thread(target=lambda: self.server.run(
            host='0.0.0.0', port=self.ip_addr.split(':')[1]))
        self.flask_thread.daemon = True
        self.flask_thread.start()

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

        filename = "./wallet/companynode/{}.txt".format(self.name)
        with open(filename, "w+") as f:
            f.write(
                "Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print(
            "\n[ Your new address and private key are now in the file {0} ]".format(filename))
        return public_key.decode(), private_key

    def sign_ECDSA_msg(self):
        # Get timestamp, round it, make it into a string and encode it to bytes
        message = str(round(time.time()))
        bmessage = message.encode()
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(
            self.private_key), curve=ecdsa.SECP256k1)
        signature = base64.b64encode(sk.sign(bmessage))
        return signature, message

    def get_the_mpks(self):
        if len(self.mpks_hash) == len(self.employeelist):
            print('[ mpks are collected completely ]')
            for hash in self.mpks_hash:
                self.mpks.append(find_in_IPFS(hash))
            if len(self.employeelist) == len(self.mpks):
                print('[ Successfully find all mpks ]')
                return True
            else:
                # empty the mpks
                self.mpks = []
                print('[ Have something wrong. Rollback... ]')
                return False
        else:
            print('[ mpks are not enough ]')
            return False

    def padding_to_z(self, g=1.0001):
        self.get_the_mpks()
        num = len(self.mpks)
        pad_num = 512-num
        tmp = []
        for i in self.mpks:
            tmp.append(i['data'])
        self.mpks = tmp
        self.z = tmp

        for _ in range(pad_num):
            pad_msk = s = [random.random() for _ in range(512)]
            pad_mpk = [pow(g, si) for si in s]
            self.z.append(pad_mpk)
        print(f"len(z):{len(self.z)}")
        if(len(self.z) == 512):
            return True
        else:
            print("[ z padding error. Rollback... ]")
            self.z = []
            return False

    def broadcast_z(self):
        if (len(self.z) == 512):
            for employee in self.employeelist:
                employee_url = employee['url']
                url = f"http://{employee_url}/DP-Face/get_z"
                payload = {
                    "company_public_key": self.public_key,
                    "z": self.z
                }
                headers = {"Content-Type": "application/json"}
                res = requests.post(url, json=payload, headers=headers)
                # print(res.text)
            return True
        else:
            print("[ z has some error ]")
            return False

    def release_task(self):
        """
        Package the mpks and train_images_hash_list to task

        """
        self.task = {
            'company_ip': self.ip_addr,
            'company': self.name,
            'mpks': self.mpks,
            'train_images_hash_list': self.train_images_hash_list,
            'z': self.z
        }
        signature, message = self.sign_ECDSA_msg()
        miner_url = read_in_consensusinfo()
        for node_url in miner_url:
            url = f"http://{node_url}/DP-Face/tasks"
            payload = {"from": self.name,
                       "to": "network",
                       "task": self.task,
                       "signature": signature.decode(),
                       "message": message}
            headers = {"Content-Type": "application/json"}
            res = requests.post(url, json=payload, headers=headers)
            print(res.text)

        return True

    def set_employee_count(self, employee_count: int):
        self.employee_count = employee_count


def register():
    companynode_intro()
    print("            ==================              ")
    print("           |     register     |             ")
    print("            ==================              ")
    print("============================================")
    name = input('Please input your name: ')
    port = input('Please input web port: ')
    print("============================================")
    companynode = CompanyNode(name, f'127.0.0.1:{port}')
    print('[ Success for creating accounts ]\n\n')
    write_in_companyinfo(f"{companynode.name} : {companynode.ip_addr}")
    return companynode


def init():
    response = None
    while response not in ["1", "2", "3", "4", "5", "6"]:
        print("            ==================              ")
        print("           |    application   |             ")
        print("            ==================              ")
        response = input("""============================================
What do you want to do?
1. Collect your employees' info and share your public key
2. Collect your employees' hash(transactions)
3. Send z to your employees,and get sk
4. Issue task and wait for broadcast sks
5. Get the model
6. Quit
============================================\nchoose: """)

        if response == '1':
            print("[ collecting employees info... ]")
            while(len(companynode.employeelist) < 1):
                time.sleep(5)
            print("[ Success. ]")
            print(f"[ Totally number is {len(companynode.employeelist)}]")

        elif response == '2':
            print("[ hashs are not sent to you.Please wait for some time ]")
            while(len(companynode.mpks_hash) != len(companynode.employeelist)):
                time.sleep(5)
            print(f"len(mpks_hash):{len(companynode.mpks_hash)},len(train_images_hash_list):{len(companynode.train_images_hash_list)},len(test_images_hash_list):{len(companynode.test_images_hash_list)}")
            if(len(companynode.mpks_hash) == len(companynode.train_images_hash_list) == len(companynode.test_images_hash_list)):
                print("[ Success for collecting all the hashs ]")
            else:
                print("[ hashs are not enough. Rollback... ]")
                companynode.mpks_hash = []
                companynode.train_images_hash_list = []
                companynode.test_images_hash_list = []

        elif response == "3":

            if(companynode.padding_to_z()):
                print("[ Broadcast to the employees ]")
                if(companynode.broadcast_z()):
                    print("[ Broadcast success. Wait for sk ]")
                    while(len(companynode.sks) != len(companynode.employeelist)):
                        time.sleep(5)
                    print("[ sks have collected successfully ]")
                else:
                    print("[ Broadcast error ]")
            else:
                print("[ Please pad z again ]")

        elif response == "4":
            if(companynode.release_task()):
                print("[ Successfully release the tasks ]")

            else:
                print("[ Release tasks error ]")
        elif response == "5":
            print("[ Wait ]")
            while(companynode.model == ''):
                time.sleep(5)
            print("[ Successfully receive ]")
        else:
            pass
        response = None


if __name__ == "__main__":
    companynode = register()
    p = companynode.ip_addr.split(':')
    threading.Thread(target=lambda: company.run(
        host=p[0], port=int(p[1]))).start()
    # company.run(host=p[0], port=int(p[1]))
    init()
