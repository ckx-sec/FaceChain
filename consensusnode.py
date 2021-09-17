from instruction import consensusnode_intro
import ecdsa
import base64
import requests
import json
import threading
from flask import Flask, request, jsonify
from blockchain import *
from crypto.imageIPE import *
from IPFS.transfer import *
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


def replace_print(func):
    return
    global print
    print = func


consensus = Flask(__name__)


class ConsensusNode():

    def __init__(self, name: str, ip_addr: str):
        """
        Give a ip_addr to create a wallet
        """
        self.name = name
        self.ip_addr = ip_addr
        # personal wallet
        self.public_key, self.private_key = self.generate_ECDSA_keys()
        self.blockchain: list[Block] = [create_genesis_block()]
        self.node_pending_transactions = []
        self.tasklist = []
        self.unvertify_models = []
        self.partner = []

        self.server = Flask(__name__)

        @self.server.route('/DP-Face/model', methods=['POST'])
        def get_model():
            unvertify_model_json = json.loads(
                request.get_data().decode('utf-8'))
            print("[ New model ]")
            print("[ FROM: {0} ]".format(unvertify_model_json['name']))
            unvertify_model = Block(int(unvertify_model_json['mined_block']['index']), float(
                unvertify_model_json['mined_block']['timestamp']), unvertify_model_json['mined_block']['data'], unvertify_model_json['mined_block']['previous_hash'])
            self.unvertify_models.append(unvertify_model)
            return "[ Success send model ]"

        @self.server.route('/DP-Face/blocks', methods=['GET'])
        def get_blocks():
            chain_to_send = self.blockchain
            # Converts our blocks into dictionaries so we can send them as json objects later
            chain_to_send_json = []
            for block in chain_to_send:
                block = {
                    "index": str(block.index),
                    "timestamp": str(block.timestamp),
                    "data": block.data,
                    "previous_hash": block.previous_hash,
                    "hash": block.hash
                }
                chain_to_send_json.append(block)

            # Send our chain to whomever requested it
            chain_to_send = json.dumps(chain_to_send_json, sort_keys=True)
            return chain_to_send

        @self.server.route('/DP-Face/txion', methods=['GET', 'POST'])
        def transaction():
            if request.method == 'POST':
                # On each new POST request, we extract the transaction data
                new_txion = json.loads(request.get_data().decode('utf-8'))
                # Then we add the transaction to our list
                if self.validate_signature(new_txion['from'], new_txion['signature'], new_txion['message']):
                    self.node_pending_transactions.append(new_txion)
                    # Because the transaction was successfully
                    # submitted, we log it to our console
                    print("[ New transaction ]")
                    print("  FROM: {0} ".format(new_txion['from']))
                    print("  TO: {0} ".format(new_txion['to']))
                    print("  MPK_HASH: {0} ".format(new_txion['mpk_hash']))
                    print("  TRAIN_IMAGES_HASH: {0} ".format(
                        new_txion['train_images_hash']))
                    print("  TEST_IMAGES_HASH: {0} ".format(
                        new_txion['test_images_hash']))
                    # Then we let the client know it worked out
                    return "[ Transaction submission successful ]"
                else:
                    return "[ Transaction submission failed. Wrong signature ]"
            # Send pending transactions to the mining process
            elif request.method == 'GET' and request.args.get("update") == self.public_key:
                pending = json.dumps(
                    self.node_pending_transactions, sort_keys=True)
                # Empty transaction list
                self.node_pending_transactions[:] = []
                return pending

        @self.server.route('/DP-Face/tasks', methods=['POST'])
        def append_task():
            task = json.loads(request.get_data().decode('utf-8'))
            print(f"[ Get the task ]")
            task_json = {
                'company': task['task']['company'],
                'company_ip': task['task']['company_ip'],
                'mpks': task['task']['mpks'],
                'train_images_hash_list': task['task']['train_images_hash_list'],
                'z': task['task']['z']
            }
            self.tasklist.append(task_json)
            return "[ Send task successfully ]"

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

        filename = "./wallet/consensusnode/{}.txt".format(self.name)
        with open(filename, "w+") as f:
            f.write("[ Private key: {0}\nWallet address / Public key: {1} ]".format(
                private_key, public_key.decode()))
        print(
            "[ Your new address and private key are now in the file {0} ]".format(filename))
        return public_key.decode(), private_key

    def validate_signature(self, public_key, signature, message: str):
        """Verifies if the signature is correct. This is used to prove
        it's you (and not someone else) trying to do a transaction with your
        address. Called when a user tries to submit a new transaction.
        """
        public_key = (base64.b64decode(public_key)).hex()
        signature = base64.b64decode(signature)
        vk = ecdsa.VerifyingKey.from_string(
            bytes.fromhex(public_key), curve=ecdsa.SECP256k1)
        # Try changing into an if/else statement as except is too broad.
        try:
            return vk.verify(signature, message.encode())
        except:
            return False

    def update_blockchain(self):
        filename = "./blockchain/consensusnode-{}.txt".format(self.name)
        with open(filename, "w+") as f:
            for block in self.blockchain:
                f.write("{}".format(block.print_line()))
        print("[ Blockchain update successfully ]".format(filename))

    def update_tasklist(self):
        if self.tasklist != []:
            self.tasklist.pop(0)
        print(f"[ Now, {len(self.tasklist)} tasks leaves ]")

    def consensus(self, ip_addr):
        # Get the blocks from other nodes
        other_chains: list[list[Block]] = find_new_chains(ip_addr)
        # If our chain isn't longest, then we store the longest chain
        blockchain_cache = self.blockchain
        longest_chain = blockchain_cache
        for chain in other_chains:
            if len(longest_chain) < len(chain):
                longest_chain = chain
        # If the longest chain wasn't ours, then we set our chain to the longest
        if longest_chain == blockchain_cache:
            # Keep searching for proof
            return False
        else:
            # Give up searching proof, update chain and start over again
            blockchain_cache = longest_chain
            return blockchain_cache

    def proof_of_work(self, last_block: Block):

        keymd5 = last_block.hash[0:6]
        print(f"[ Task: {keymd5} ]")
        start_time = time.time()
        i = random.randint(10000, 10000000)
        while not (md5(str(i))[0:6] == keymd5):
            i = i+1
            # Check if any node found the solution every 10 seconds
            if int((time.time()-start_time) % 10) == 0:
                # If any other node got the proof, stop searching
                time.sleep(1)
                new_blockchain = self.consensus(self.ip_addr)
                if new_blockchain:
                    # (False: another node got proof first, new blockchain)
                    return False, new_blockchain
        # Once that number is found, we can return it as a proof of our work
        return i, blockchain

    def proof_of_learning(self, last_block: Block):
        self.train_model(last_block)
        print("[ Collect unvertify models... ]")
        while(len(self.unvertify_models) < len(self.partner)):
            pass
        max_block = self.vertify_model(last_block)

        if not max_block:
            new_blockchain = self.consensus(self.ip_addr)
            return False, new_blockchain

        else:
            return max_block, blockchain

    def mine(self):
        self.load_miner_urls()
        print("============================================")
        print("[ Tasklist ]")
        for i in self.tasklist:
            print(f"[ Task ]")
            print(f"[ Name: {i['company']} ]")
            print(f"[ IP: {i['company_ip']} ]")
        print("============================================")
        last_block = self.blockchain[-1]
        last_task = last_block.data['task']
        if last_task == None:
            proof = self.proof_of_work(last_block)
            if not proof[0]:
                print("[ Find from others ]")
                self.blockchain = proof[1]
                print(
                    f"[ Now the blockchain recorded length is {len(self.blockchain)} ]")
                self.update_blockchain()
                print("[ This turn is finish ]")
                print("============================================")
            else:
                print("[ I find successfully ]")
                mined_block = self.generate_block(proof[0], last_block)
                self.blockchain.append(mined_block)
                print(
                    f"[ Now the blockchain recorded length is {len(self.blockchain)} ]")
                self.update_blockchain()
                print("[ This turn is finish ]")
                print("============================================")
        else:
            proof = self.proof_of_learning(last_block)
            if not proof[0]:
                self.blockchain = proof[1]
                print(
                    f"[ Now the blockchain recorded length is {len(self.blockchain)} ]")
                self.update_blockchain()
                print("[ This turn is finish ]")
                print("============================================")
            else:

                print(
                    f"[ Now the blockchain recorded length is {len(self.blockchain)} ]")
                self.update_blockchain()
                print("[ This turn is finish ]")
                print("============================================")

    def train_model(self, last_block: Block):
        print("[ Start training...]")
        last_task = last_block.data['task']
        if self.tasklist == []:
            pass
        else:
            if last_task == self.tasklist[0]:
                self.tasklist.pop(0)
        print(last_task['company'])
        company_addr = last_task['company_ip']
        decrypt_images_list = self.decrypt_train_images(
            company_addr, last_task)
        ###########
        use = decrypt_images_list
        acc = random.random()
        model = (acc, self.public_key)
        ###########
        mined_block = self.generate_block(model, last_block)
        self.send_train_model(mined_block)

    def vertify_model(self, last_block: Block):
        print("[ Start vertifying... ]")
        last_task = last_block.data['task']
        company_addr = last_task['company_ip']
        decrypt_images_list = self.decrypt_test_images(company_addr, last_task)
        ##########
        use = decrypt_images_list
        block_list: list[Block] = self.unvertify_models
        max_acc = -1
        max_block: Block = None
        for block in block_list:
            model = block.data['model']
            acc = model[0]
            if acc > max_acc:
                max_block = block
                max_acc = acc
        ##########
        print("[ Get the final model ]")
        print("[ model ]")
        print(f"[ public key: {max_block.data['model'][1]} ]")
        print(f"[ acc: {max_block.data['model'][0]} ]")
        if max_block.data['model'][1] == self.public_key:
            print("[ I find successfully ]")
            self.blockchain.append(max_block)
            self.send_to_company(max_block.data['model'], company_addr)
            self.unvertify_models = []
            return max_block
        else:
            print("[ Find from others ]")
            print("[ Please wait for 10 seconds ]")
            time.sleep(10)
            self.unvertify_models = []
            return False

    def generate_block(self, model, last_block: Block):
        NODE_PENDING_TRANSACTIONS = requests.get(
            url='http://'+self.ip_addr + '/DP-Face/txion', params={'update': self.public_key}).content
        NODE_PENDING_TRANSACTIONS = json.loads(NODE_PENDING_TRANSACTIONS)
        if self.tasklist != []:
            task = self.tasklist[0]
            self.update_tasklist()
        else:
            task = None
        new_block_data = {
            "model": model,
            "task": task,
            "transactions": list(NODE_PENDING_TRANSACTIONS)
        }
        new_block_index = last_block.index + 1
        new_block_timestamp = time.time()
        last_block_hash = last_block.hash
        # Empty transaction list
        NODE_PENDING_TRANSACTIONS = []
        # Now create the new block
        mined_block = Block(new_block_index, new_block_timestamp,
                            new_block_data, last_block_hash)

        return mined_block

    def decrypt_train_images(self, company_addr, task):
        sks = self.get_sks(company_addr, task)
        z = task['z']
        decrypt_images = []
        decrypt_images_list: list[list] = []
        train_images_hash_list = task['train_images_hash_list']
        for train_images_hash in train_images_hash_list:
            train_images = find_in_IPFS(train_images_hash)
            for sk in sks:
                if sk['public_key'] == train_images['public_key']:
                    for train_image in train_images['data']:
                        decrypt_image = decrypt(
                            train_image[0], train_image[1], sk['sk'], z)
                        decrypt_images.append(decrypt_image)
            decrypt_images_list.append(decrypt_images)
        return decrypt_images_list

    def decrypt_test_images(self, company_addr, task):
        sks = self.get_sks(company_addr, task)
        test_images_hash_list = self.get_test_hash(company_addr, task)
        z = task['z']
        decrypt_images = []
        decrypt_images_list: list[list] = []
        test_images_hash_list = test_images_hash_list
        for test_images_hash in test_images_hash_list:
            test_images = find_in_IPFS(test_images_hash)
            for sk in sks:
                if sk['public_key'] == test_images['public_key']:
                    for test_image in test_images['data']:
                        decrypt_image = decrypt(
                            test_image[0], test_image[1], sk['sk'], z)
                        decrypt_images.append(decrypt_image)
            decrypt_images_list.append(decrypt_images)
        return decrypt_images_list

    def get_test_hash(self, company_addr, task):
        res = requests.post(url='http://'+company_addr+'/DP-Face/release_test_hash',
                            json=task, headers={"Content-Type": "application/json"}).content
        test_images_hash_list = json.loads(res)
        return test_images_hash_list

    def get_sks(self, company_addr, task):
        print("[ Ask for sks... ]")
        res = requests.post(url='http://'+company_addr+'/DP-Face/issue_sk',
                            json=task, headers={"Content-Type": "application/json"}).content
        sks = json.loads(res)
        print("[ Get sks successfully ]")
        return sks

    def send_train_model(self, mined_block: Block):
        mined_block_json = {
            "index": str(mined_block.index),
            "timestamp": str(mined_block.timestamp),
            "data": mined_block.data,
            "previous_hash": mined_block.previous_hash,
            "hash": mined_block.hash
        }
        model = {"name": self.name, "public_key": self.public_key,
                 "mined_block": mined_block_json}
        for node_url in self.partner:
            requests.post(url='http://'+node_url+'/DP-Face/model', json=model,
                          headers={"Content-Type": "application/json"}).content

    def send_to_company(self, model, company_ip):
        requests.post(url='http://'+company_ip+'/DP-Face/get_model', json={
                      "name": self.name, "public_key": self.public_key, "model": model}).content

    def load_miner_urls(self):
        self.partner = read_in_consensusinfo()
        print('[ Current partner list: ]')
        print(self.partner)

    def show_information(self):
        info = "============================================\n"
        info += f"[ NAME: {self.name} ]\n"
        info += f"[ IP_ADDRESS: {self.ip_addr} ]\n"
        info += "============================================\n"
        info += f"[ BLOCKCHAIN ]\n"
        for block in self.blockchain:
            info += "[ BLOCK ]\n"
            info += f"  INDEX: {block.index}\n"
            info += f"  TIMESTAMP: {block.timestamp}\n"
            info += f"  DATA: {block.data} ]\n"
            info += f"  Previous Hash: {block.previous_hash}\n"
            info += f"  Hash: {block.hash}\n"
        info += "============================================\n"
        info += f"[ TASKLIST ]\n"
        i = 1
        for task in self.tasklist:
            info += f"[ TASK {i}]\n"
            info += f"[ Company: {task['task']['company']} ]\n"
            i = i+1
        info += "============================================"
        return info


def register():
    consensusnode_intro()
    print("            ==================              ")
    print("           |     register     |             ")
    print("            ==================              ")
    print("============================================")
    name = input('Please input your name: ')
    port = input('Please input web port: ')
    print("============================================")
    consensusnode = ConsensusNode(name, f'127.0.0.1:{port}')
    print('[ Success for creating accounts ]')
    write_in_consensusinfo(f"{consensusnode.ip_addr}")
    consensusnode.update_blockchain()
    return consensusnode


def init():
    response = None
    while response not in ["1", "2", "3", "4"]:
        print("            ==================              ")
        print("           |    application   |             ")
        print("            ==================              ")
        response = input("""============================================
What do you want to do?
1. Show information
2. Mine 
3. Quit
============================================\nchoose: """)

        if response == '1':
            print(consensusnode.show_information())
        elif response == '2':
            while(True):
                consensusnode.mine()
        else:
            pass
        response = None


if __name__ == '__main__':
    consensusnode = register()
    p = consensusnode.ip_addr.split(':')
    threading.Thread(target=lambda: consensus.run(
        host=p[0], port=int(p[1]))).start()
    # company.run(host=p[0], port=int(p[1]))
    init()
