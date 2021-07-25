from flask import Flask, json, request
from demo import *


app = Flask(__name__)

BLOCKCHAIN: list[Block] = [create_genesis_block(COMPANY_NODES[0].public_key)]
BLOCK_CACHE: list[Block] = []
TASKLIST: list = []


@app.route('/task/get', method=['GET','POST'])
def handle_task():
    if request.method=='GET':
        return TASKLIST[0]
    elif request.method=='POST':
        task = json.loads(request.form['task'])
        TASKLIST.append(task)


@app.route('/block_cache', method=['GET', 'POST'])
def handle_cache():
    if request.method == 'GET':
        return json.dumps(BLOCK_CACHE)
    elif request.method == 'POST':
        block = json.loads(request.get_data(as_text=True),
                           object_hook=Block.from_dict)
        BLOCK_CACHE.append(block)


@app.route('/blockchain', method=['GET', 'POST'])
def handle_blockchain():
    if request.method == 'GET':
        return json.dumps(BLOCKCHAIN)
    elif request.method == 'POST':
        block = json.loads(request.get_data(as_text=True),
                           object_hook=Block.from_dict)
        BLOCK_CACHE.append(block)