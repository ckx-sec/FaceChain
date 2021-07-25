from __future__ import annotations
import hashlib
from typing import Any, Dict
import ecdsa
import base64
import random
import time
import requests
import numpy as np

# images setting
TRAIN = 8
TEST = 2
ALL = TRAIN + TEST


class node:
    def __init__(self):
        self.public_key, self.private_key = self.generate_ECDSA_keys()

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
        return public_key.decode(), private_key


class datanode(node):
    def __init__(self, ip_addr, company_addr):
        """
        Give a ip_addr,company_addr to create a wallet
        """
        self.ip_addr = ip_addr
        self.company_addr = company_addr
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()
        # encrypt algothrim
        self.mpk, self.msk = self.generate_DPIPE_keys()
        self.train_images = ''
        self.test_images = ''
        self.sk = []
        # transaction hash
        self.mpk_hash = ''
        self.training_images_hash = ''
        self.test_images_hash = ''
        # wait for receive
        self.company_public_key = ''
        self.z = []

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

        filename = "./datanode_wallet/{}.txt".format(self.ip_addr)
        with open(filename, "w+") as f:
            f.write(
                "Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print(
            "Your new address and private key are now in the file {0}".format(filename))
        return public_key.decode(), private_key

    def generate_DPIPE_keys(self, g=1.0001):
        """
        To generate Inner-Product-Encryption key-pairs

        Return mpk,msk
        """
        msk = s = [random.random() for _ in range(512)]
        mpk = h = [pow(g, si) for si in s]
        return mpk, msk

    def get_images(self, images):
        """
        To upload the images and change into matrix, classify then with train set and test set

        Return boolean 
        """
        self.train_images = images[:TRAIN]
        self.test_images = images[TRAIN:ALL]
        return True

    def encrypt_images(self, images):
        """
        To do DP and Inner-Product-Encrypt (image is 18*512 Matrix)

        Return a 18*512 Matrix encrypted_image
        """
        encrypted_images = []
        for image in images:
            encrypted_image = laplace_mech(image)
            encrypted_images.append(encrypted_image)

        return encrypted_images

    def send_to_company(self, data, company: companynode):
        """
        To send mpk to its company. Wait for z

        Return boolean
        """
        return True

    def get_z(self, company: companynode):
        """
        Get z from its company.

        Return boolean
        """
        self.z = company.z
        return True

    def compute_sk(self):
        """
        Compute sk
        """
        s = np.array(self.msk)
        z = np.array(self.z)
        self.sk = list(np.matmul(s, z))
        return self.sk


class companynode(node):
    def __init__(self, ip_addr):
        """
        Give a ip_addr to create a wallet
        """
        self.ip_addr = ip_addr
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()
        # add employee
        self.employeelist: list[datanode] = []
        # task
        self.mpks_hash = []
        self.train_images_hash = []
        self.test_images_hash = []
        # collect
        self.mpks = []
        self.sign_mpks = []
        self.z = []
        self.sks = []
        self.sign_sks = []

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

        filename = "./companynode_wallet/{}.txt".format(self.ip_addr)
        with open(filename, "w+") as f:
            f.write(
                "Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print(
            "Your new address and private key are now in the file {0}".format(filename))
        return public_key.decode(), private_key

    def get_mpk_hash(self, node: datanode):
        """
        To get mpk from his employee

        Return boolean
        """
        self.mpks_hash.append(node.mpk_hash)
        return True

    def get_sk(self, node: datanode):
        """
        To get sk from his employee

        Return boolean
        """
        self.sks.append(node.sk)
        self.sign_sks.append(node.public_key)
        return True

    def issue_task(self, tasklist: list):
        """
        Package the mpks and training_images_hash to task

        Return current tasklist
        """
        task = {
            'mpks': self.mpks,
            'training_images_hash': self.train_images_hash,
            'company': [self.public_key, self.ip_addr]
        }
        tasklist.append(task)

        return tasklist


class consensusnode(node):
    def __init__(self, ip_addr):
        """
        Give a ip_addr to create a wallet
        """
        self.ip_addr = ip_addr
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()

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

        filename = "./consensusnode_wallet/{}.txt".format(self.ip_addr)
        with open(filename, "w+") as f:
            f.write(
                "Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print(
            "Your new address and private key are now in the file {0}".format(filename))
        return public_key.decode(), private_key

    def send_to_company(self, company: companynode):

        pass

    def train_model(self, sks, sign_sks, mpks, sign_mpks, train_images):
        """
        Train model

        Return acc,model
        """
        acc = -1
        model = 'model1'
        acc = random.random()
        return acc, model

    def vertify_model(self, test_images, model):
        """
        Vertify model

        Return acc
        """
        acc = -1
        acc = random.random()
        return acc

    def generate_block(self, blockchain: list[Block]):
        LAST_BLOCK = blockchain[-1]
        index = LAST_BLOCK.index
        company_public_key = LAST_BLOCK.task['company']
        mpks_hash = LAST_BLOCK.task['mpks_hash']
        train_images_hash = LAST_BLOCK.task['training_images_hash']
        last_hash = LAST_BLOCK.hash

        """
        wait for sks(同步关键)
        """
        for i in COMPANY_NODES:
            if(i.public_key == company_public_key):
                sign_sks = i.sign_sks
                sks = i.sks
                sign_mpks = i.sign_mpks
        mpks = find_in_IPFS(self, mpks_hash)
        train_images = find_in_IPFS(self, train_images_hash)
        acc, model = self.train_model(
            sks, sign_sks, mpks, sign_mpks, train_images)
        """
        task receive from tasklist
        """
        task = TASKLIST[0]
        new_block = Block(index+1, time.time(), {'node': self.public_key, 'acc': acc,
                          'model': model, 'company': company_public_key}, task, last_hash)
        """
        send to other nodes /DP-Face/new_blocks
        """
        BLOCK_CACHE.append(new_block)
        return new_block

    def get_winner(self):
        max_acc = {'acc': -1}
        block_cache_list: list[Block] = BLOCK_CACHE
        """
        receive the block_cache_list
        """
        test_images_hash = ''
        """
        get the test_images_hash
        """
        test_images = find_in_IPFS(self, test_images_hash)
        for new_block in block_cache_list:
            acc = self.vertify_model(new_block.model['model'], test_images)
            if acc > max_acc['acc']:
                max_acc = new_block

        """
        broadcast the vertify_block to consensusnodelist
        """
        return max_acc

    def hand_over(self, block: Block):
        self.send_to_company(block.model['company'])


class Block:
    def __init__(self, index, timestamp, model, task, previous_hash):
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.
        Args:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (json): Data to be logged.
            previous_hash(str): String representing previous block unique hash.
        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (json): Data to be logged.
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.
        """
        self.index:int = index
        self.timestamp = timestamp
        self.model = model
        self.task = task
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256."""
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.model) +
                   str(self.task) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

    @staticmethod
    def from_dict(d: Dict[str, Any]):
        block = Block(None, None, None, None, None)
        block.__dict__ = d
        return block

# blockchain


def create_genesis_block(public_key):
    return Block(0, time.time(), {'node': '', 'acc': -1, 'model': '', 'company': ''}, {'company': public_key, 'mpks_hash': '', 'training_images_hash': ''}, '0')


def collect_sks(company_address):
    for company in COMPANY_NODES:
        if(company.public_key == company_address):
            for employee in company.employeelist:
                employee.send_sk_to_companynode()
            return True
    print("can't find the company address:{}".format(company.public_key))
    return False


def issue_sks(public_key):
    for company in COMPANY_NODES:
        if(company.public_key == public_key):
            if company.sks:
                for consensus in CONSENSUS_NODES:
                    company.send_sks_to_consensusnode(consensus)
                return True
            print("the company {}' sks not exist\n".format(company.public_key))
            return False
    print("can't find the company address:{}".format(company.public_key))
    return False


# IPFS
def store_in_IPFS(node: node, data):
    """
    To store the data into IPFS

    Return address hash
    """
    data = {'public_key': node.public_key, 'data': data}

    hash_data = hashlib.sha256(b"123").hexdigest()
    return hash_data


def find_in_IPFS(node: node, data_hash):
    """
    To use hash to find data

    Return data(json)
    """
    a = hashlib.sha256().update(b"adsdads")
    b = [random.random() for _ in range(512)]
    data = {'public_key': a, 'data': b}

    return data


# DP algothrim
def noisyCount(sensitivety, epsilon):
    beta = sensitivety/epsilon
    u1 = np.random.random()
    u2 = np.random.random()
    if u1 <= 0.5:
        n_value = -beta*np.log(1.-u2)
    else:
        n_value = beta*np.log(u2)
    # print(n_value)
    return n_value


def laplace_mech(data, sensitivety=1, epsilon=4):
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] += noisyCount(sensitivety, epsilon)
    return data

# Inner-Product-Encryption


def padding_z(z: list, n, r=1):
    for i in range(1, n+1):
        z.append([(random.random()-0.5)*r for _ in range(512)])
    return z


BLOCKCHAIN: list[Block] = []
BLOCK_CACHE: list[Block] = []
TASKLIST: list = []
# consensusnode list
CONSENSUS_NODES: list[consensusnode] = []
# companynode list
COMPANY_NODES: list[companynode] = []


if __name__ == '__main__':
    """
    Step 1: register node list
    """
    for i in range(1):
        consensus = consensusnode(i+1)
        CONSENSUS_NODES.append(consensus)
    for i in range(1):
        company = companynode(i+1)
        COMPANY_NODES.append(company)
    for i in COMPANY_NODES:
        for j in range(1, 14):
            employee = datanode(j, i.ip_addr)
            i.employeelist.append(employee)
    print("register finish")

    """
    Step 2: initial blockchain
    """
    BLOCKCHAIN = [create_genesis_block(COMPANY_NODES[0].public_key)]

    """
    Step 3: datanode upload images,mpk
    """
    for i in COMPANY_NODES:
        for j in i.employeelist:
            j.mpk_hash = store_in_IPFS(j, j.mpk_hash)
            j.training_images_hash = store_in_IPFS(j, j.train_images)
            j.test_images_hash = store_in_IPFS(j, j.test_images)

    """
    Step 4: datanode send mpk_hash, train_image_hash to company
            companynode receive mpks, padding to 512*512 matrix called z, then send to datanode back
            datanode receive z, compute sk, send to companynode back
    """
    for i in COMPANY_NODES:
        for j in i.employeelist:
            i.get_mpk_hash(j)
        # collect all mpks
        for k in i.mpks_hash:
            node_mpk = find_in_IPFS(i, k)
            i.mpks.append(node_mpk['data'])
            i.sign_mpks.append(node_mpk['public_key'])

    # companynode pad mpks to z
    for i in COMPANY_NODES:
        i.z = padding_z(i.mpks, 512-len(i.employeelist))

    # datanode get z
    for i in COMPANY_NODES:
        for j in i.employeelist:
            j.get_z(i)

    # datanode compute sk
    for i in COMPANY_NODES:
        for j in i.employeelist:
            j.compute_sk()

    # companynode collect sks
    for i in COMPANY_NODES:
        for j in i.employeelist:
            i.get_sk(j)

    """
    Step 5: companynode issue task
    """
    for i in COMPANY_NODES:
        TASKLIST = i.issue_task(TASKLIST)

    """
    Step 6: consensusnode mine and broadcast to others
    """
    for i in CONSENSUS_NODES:
        i.generate_block(BLOCKCHAIN)

    for i in CONSENSUS_NODES:
        block: Block = i.get_winner()
    BLOCKCHAIN.append(block)
    """
    Step 7: the winner node hand over to the task owner
    """
    for i in CONSENSUS_NODES:
        i.hand_over(block)

    """
    Step 8: tasklist update
    """
    del(TASKLIST[0])

    print("Finish one turn")
