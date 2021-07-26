import sys
import os
import re
import threading
import time
from typing import List
import requests
from models import Block, companynode, consensusnode, create_genesis_block, find_in_IPFS
from flask import Flask, json, request

app = Flask(__name__)
before_verify = Flask('train')
after_verify = Flask('verify')

this = consensusnode('127.0.0.1:6000')
COMPANY_NODES = [companynode('127.0.0.1:5000')]
BLOCKCHAIN: list[Block] = [create_genesis_block(COMPANY_NODES[0].public_key)]
# BLOCKCHAIN[0].task['company_ip'] = COMPANY_NODES[0].ip_addr
BLOCKCHAIN[0].task['company'][1] = COMPANY_NODES[0].ip_addr
BLOCK_CACHE: list[Block] = []
TASKLIST: list = []
TASK_QUEUE_ADDR = '127.0.0.1:9000'
CONSENSUS_NODE_ADDR = ['127.0.0.1:6001', '127.0.0.1:6002']
PORT = sys.argv[1]
CONSENSUS_NODE_ADDR.remove(f'127.0.0.1:{PORT}')

# 自己出的块
MY_BLOCK:Block=None

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
        # block = json.loads(request.get_data(as_text=True),
        #                    object_hook=Block.from_dict)
        block = Block.from_dict(json.loads(request.get_data(as_text=True)))
        BLOCK_CACHE.append(block)
    return 'Success'


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
        # block = json.loads(request.get_data(as_text=True),
        #                    object_hook=Block.from_dict)
        block = Block.from_dict(json.loads(request.get_data(as_text=True)))
        BLOCK_CACHE.append(block)
    return 'Success'


def generate_block(blockchain: list[Block]):
    LAST_BLOCK = blockchain[-1]
    index = LAST_BLOCK.index
    company_public_key = LAST_BLOCK.task['company'][0]
    company_ip_addr = LAST_BLOCK.task['company'][1]
    mpks_hash = LAST_BLOCK.task['mpks_hash']
    train_images_hash = LAST_BLOCK.task['training_images_hash']
    last_hash = LAST_BLOCK.hash

    """
    wait for sks(同步关键)
    """
    while True:
        try:
            resp = requests.get(f'http://{company_ip_addr}/keys')
            print("resp: "+resp.text)
            keys = resp.json()
        except ValueError as e:
            print(e)
            print('generate block fail.retry...')
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
    task = requests.get(f'http://{TASK_QUEUE_ADDR}/get_front').json()
    new_block = Block(index+1, time.time(), {'node': this.public_key, 'acc': acc,
                                             'model': model, 'company': [company_public_key,company_ip_addr]}, task, last_hash)
    """
    send to other nodes /DP-Face/new_blocks
    """
    global MY_BLOCK
    MY_BLOCK = new_block
    BLOCK_CACHE.append(new_block)
    return new_block, company_ip_addr


def get_winner(company_ip: str):
    max_acc = -1
    block_cache_list: list[Block] = BLOCK_CACHE
    """
    receive the block_cache_list
    """
    while True:
        try:
            test_images_hash = requests.get(
                f'http://{company_ip}/get_test_images_hash').json()
        except ValueError as e:
            print(e)
            print('get winner fail.retry...')
            time.sleep(1)
            continue
        break

    # test_images_hash = ''
    """
    get the test_images_hash
    """
    test_images = find_in_IPFS(this, test_images_hash)
    best_block: Block = None
    for new_block in block_cache_list:
        print(type(new_block.model))
        acc = this.vertify_model(new_block.model['model'], test_images)
        if acc > max_acc:
            max_acc = new_block.model['acc']
            best_block = new_block
    
    if MY_BLOCK.hash==best_block.hash:
        hand_over(new_block.model['model'],company_ip)

    """
    broadcast the vertify_block to consensusnodelist
    """
    BLOCKCHAIN.append(
        best_block)  # TODO 直接放进BLOCKCHAIN还是待会收到所有共识节点的结果挑一个最好的放进BLOCKCHAIN
    BLOCK_CACHE.clear()
    return best_block

def hand_over(model,addr):
    requests.post(f'http://{addr}/submit_model',data=json.dumps(model))

if __name__ == '__main__':
    while True:

        # 训练，出块
        t = threading.Thread(
            target=lambda: before_verify.run(
                '127.0.0.1', int(PORT), debug=True, use_reloader=False),
            name='before_verify_thread')
        new_block, company_addr = generate_block(BLOCKCHAIN)
        t.start()
        for addr in CONSENSUS_NODE_ADDR:
            while True:
                try:
                    requests.post(
                        f'http://{addr}/block_cache', data=json.dumps(new_block.__dict__))
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue
                break
        time.sleep(10)
        requests.get(f'http://127.0.0.1:{PORT}/shutdown')

        time.sleep(1)

        # 验证
        t = threading.Thread(
            target=lambda: after_verify.run('127.0.0.1', int(
                PORT), debug=True, use_reloader=False),
            name='after_verify_thread')
        get_winner(company_addr)
        t.start()
        for addr in CONSENSUS_NODE_ADDR:
            while True:
                try:
                    requests.post(
                        f'http://{addr}/blockchain', data=json.dumps(new_block.__dict__))
                except Exception as e:
                    print(e)
                    time.sleep(1)
                    continue
                break
        time.sleep(10)
        requests.get(f'http://127.0.0.1:{PORT}/shutdown')

        # TODO 把最好的块挑出来单独放进链尾

        # TODO 


        time.sleep(2)
