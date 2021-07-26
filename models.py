from __future__ import annotations
import hashlib
from typing import Any, Dict
import ecdsa
import base64
import random
import time
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
        print(f'msk: {len(self.msk)}, z: {len(self.z)}')
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


def create_genesis_block(public_key):
    # return Block(0, time.time(), {'node': '', 'acc': -1, 'model': '', 'company': ''}, {'company': public_key,'company_ip':'', 'mpks_hash': '', 'training_images_hash': ''}, '0')
    return Block(0, time.time(), {'node': '', 'acc': -1, 'model': '', 'company': ''}, {'company': [public_key,''], 'mpks_hash': '', 'training_images_hash': ''}, '0')


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
    a = hashlib.sha256(b'adsads').hexdigest()
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

