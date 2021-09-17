import hashlib
import time
import requests
import json
from config.node_config import *
from flask import Flask, request

blockchain = Flask(__name__)


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        """Returns a new Block object. Each block is "chained" to its previous
        by calling its unique hash.
        Args:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (str): Data to be logged.
            previous_hash(str): String representing previous block unique hash.
        Attrib:
            index (int): Block number.
            timestamp (int): Block creation timestamp.
            data (json): mpk_hash and images_hash
            previous_hash(str): String representing previous block unique hash.
            hash(str): Current block unique hash.
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """Creates the unique hash for the block. It uses sha256."""
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.timestamp) +
                   str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

    def print_line(self):
        if self.data['task']:
            task = self.data['task']['company']
        else:
            task = None
        return ('\nindex: '+str(self.index) + '\ntimestamp: ' + str(self.timestamp) + '\ntask: ' + str(task) + '\nprevious_hash: '+str(self.previous_hash) + '\nhash: '+str(self.hash)+'\n')


def create_genesis_block():
    """To create each block, it needs the hash of the previous one. First
    block has no previous, so it must be created manually (with index zero
     and arbitrary previous hash)"""
    return Block(0, 0.0, {
        "model": 1,
        "task": None,
        "transactions": None
    },
        "c4ca423")


def find_new_chains(url):
    # Get the blockchains of every other node
    other_chains: list[list[Block]] = []
    miner_url = read_in_consensusinfo()
    for node_url in miner_url:
        if node_url == url:
            continue
        else:
            # Get their chains using a GET request
            blockchain_json: list = json.loads(requests.get(
                url='http://'+node_url + "/DP-Face/blocks").content)
            # Convert the JSON object to a Python dictionary
            # block = json.loads(block)
            # Verify other node block is correct
            blockchain = []
            for block_json in blockchain_json:
                block = Block(int(block_json['index']), float(
                    block_json['timestamp']), block_json['data'], block_json['previous_hash'])
                blockchain.append(block)
                # if block.hash==block_json['hash']:
                #     blockchain.append(block)
                # else:
                #     print("wrong")
            validated = validate_blockchain(blockchain)
            if validated:
                # Add it to our list
                other_chains.append(blockchain)
    return other_chains


def validate_blockchain(block: list[Block]):
    """Validate the submitted chain. If hashes are not correct, return false
    block(str): json
    """
    if(type(block[-1].data['model']) == int):
        if(md5(block[-1].data['model'])[0:6] == (block[-1].previous_hash)[0:6]):
            return True
    else:
        return True


def md5(s):  # 计算MD5字符串
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()
