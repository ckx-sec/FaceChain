import re
import threading
import time
from typing import List
import requests
from demo import Block, consensusnode, create_genesis_block, find_in_IPFS
from flask import Flask, json, request

app = Flask(__name__)
before_verify = Flask('train')
after_verify = Flask('verify')

this = consensusnode('localhost:6000')
COMPANY_NODES=[]
BLOCKCHAIN: list[Block] = [create_genesis_block(COMPANY_NODES[0].public_key)]
BLOCK_CACHE: list[Block] = []
TASKLIST: list = []
TASK_QUEUE_ADDR = ''
CONSENSUS_NODE_ADDR = []

# status=''
#

# 大列表 记录所有共识节点信息

# 开一个线程留意公司节点发的task


# 出块
# 验证
# 得出结果，少数服从多数


# @app.route('/consensus', methods=['POST'])
# def consensus():
#     block: Block = json.loads(request.get_data(
#         as_text=True), object_hook=Block.from_dict)
#     BLOCK_CACHE.append(block)
#     return 'Success'


'''
@app.route('/task', methods=['GET', 'POST'])
def handle_task():
    if request.method == 'GET':
        return TASKLIST[0]
    elif request.method == 'POST':
        task = json.loads(request.form['task'])
        TASKLIST.append(task)
'''


@before_verify.route('/block_cache', methods=['GET', 'POST'])
def handle_cache():
    if request.method == 'GET':
        return json.dumps(BLOCK_CACHE)
    elif request.method == 'POST':
        block = json.loads(request.get_data(as_text=True),
                           object_hook=Block.from_dict)
        BLOCK_CACHE.append(block)


# TODO 使用更安全的方法结束flask server
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@before_verify.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@after_verify.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@after_verify.route('/blockchain', methods=['GET', 'POST'])
def handle_blockchain():
    if request.method == 'GET':
        return json.dumps(BLOCKCHAIN)
    elif request.method == 'POST':
        block = json.loads(request.get_data(as_text=True),
                           object_hook=Block.from_dict)
        BLOCK_CACHE.append(block)


def generate_block(blockchain: list[Block]):
    LAST_BLOCK = blockchain[-1]
    index = LAST_BLOCK.index
    company_public_key, company_ip_addr = LAST_BLOCK.task['company']
    mpks_hash = LAST_BLOCK.task['mpks_hash']
    train_images_hash = LAST_BLOCK.task['training_images_hash']
    last_hash = LAST_BLOCK.hash

    """
    wait for sks(同步关键)
    """
    while True:
        try:
            keys = requests.get(f'{company_ip_addr}/keys').json()
        except ValueError:
            time.sleep(1)
            continue
        break

    sks = keys['sks']
    sign_sks = keys['sign_sks']
    sign_mpks = keys['sign_mpks']

    mpks = find_in_IPFS(this, mpks_hash)
    train_images = find_in_IPFS(this, train_images_hash)
    acc, model = this.train_model(
        sks, sign_sks, mpks, sign_mpks, train_images)
    """
    task receive from tasklist
    """
    task = requests.get(f'{TASK_QUEUE_ADDR}/get_front').json()
    new_block = Block(index+1, time.time(), {'node': this.public_key, 'acc': acc,
                                             'model': model, 'company': company_public_key}, task, last_hash)
    """
    send to other nodes /DP-Face/new_blocks
    """
    BLOCK_CACHE.append(new_block)
    return new_block, company_ip_addr


def get_winner(company_ip: str):
    max_acc = {'acc': -1}
    block_cache_list: list[Block] = BLOCK_CACHE
    """
    receive the block_cache_list
    """
    while True:
        try:
            test_images_hash = requests.get(
                f'{company_ip}/get_test_images_hash').json()
        except ValueError:
            time.sleep(1)
            continue
        break

    # test_images_hash = ''
    """
    get the test_images_hash
    """
    test_images = find_in_IPFS(this, test_images_hash)
    for new_block in block_cache_list:
        acc = this.vertify_model(new_block.model['model'], test_images)
        if acc > max_acc['acc']:
            max_acc = new_block

    """
    broadcast the vertify_block to consensusnodelist
    """
    BLOCKCHAIN.append(max_acc) # TODO 直接放进BLOCKCHAIN还是待会收到所有共识节点的结果挑一个最好的放进BLOCKCHAIN
    return max_acc


if __name__ == '__main__':
    while True:

        # 训练，出块
        t = threading.Thread(
            target=lambda: before_verify.run('127.0.0.1', 6000, debug=True,use_reloader=False),
            name='before_verify_thread')
        new_block, company_addr = generate_block(BLOCKCHAIN)
        t.start()
        for addr in CONSENSUS_NODE_ADDR:
            requests.post(f'{addr}/block_cache', data=json.dumps(new_block))
        time.sleep(10)
        requests.get('127.0.0.1:6000/shutdown')

        # 验证
        t = threading.Thread(
            target=lambda: after_verify.run('127.0.0.1', 6000, debug=True,use_reloader=False),
            name='after_verify_thread')
        get_winner(company_addr)
        t.start()
        for addr in CONSENSUS_NODE_ADDR:
            requests.post(f'{addr}/blockchain', data=json.dumps(new_block))
        time.sleep(10)
        requests.get('127.0.0.1:6000/shutdown')

        # TODO 把最好的块挑出来单独放进链尾

        # TODO 

