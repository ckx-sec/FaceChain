import threading
from time import sleep
from typing import Dict, List, Tuple
from flask import Flask, json, request
from demo import *
#app = Flask(__name__)

serve_datanode = Flask('serve_datanode')
serve_consensus_node = Flask('serve_consensus_node')

this = companynode('127.0.0.1:5000')


class DataNode:
    '''公司节点能看到的数据节点信息'''

    def __init__(self, public_key: str, mpk_hash: str) -> None:
        self.public_key = public_key
        self.mpk_hash = mpk_hash
        self.sk: List[List[float]] = None
        self.training_images_hash: List[str] = None
        self.test_images_hash: List[str] = None
        # self.mpk=find_in_IPFS


TASK_QUEUE_ADDR = '127.0.0.1:9000'
DATANODES: Dict[str, DataNode] = {}
DATANODE_MAX_COUNT = 1
CONSENSUS_NODES: List[consensusnode] = []
# TODO 事先准备好几个共识节点

# TODO 使用更安全的方法结束flask server


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@serve_consensus_node.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@serve_datanode.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@serve_datanode.route('/register', methods=['POST'])
def register_datanode():
    '''把节点信息在company节点记录一下'''
    print('register: '+request.get_data(as_text=True))
    datanode_count = len(DATANODES)
    if datanode_count < DATANODE_MAX_COUNT:
        public_key = request.form['public_key']
        mpk_hash = request.form['mpk_hash']
        DATANODES[public_key] = DataNode(public_key, mpk_hash)

        mpk = find_in_IPFS(None, mpk_hash)  # TODO 实现
        if datanode_count == DATANODE_MAX_COUNT-1:
            this.z = padding_z(this.mpks, 512-len(this.employeelist))
        return 'Success'
    return 'Fail'


@serve_datanode.route('/get_z', methods=['GET'])
def get_z():
    # TODO padding
    if len(DATANODES) == DATANODE_MAX_COUNT:
        return json.dumps({'z': this.z})
    return 'Error\n'


@serve_datanode.route('/submit_sk', methods=['POST'])
def submit_sk():
    public_key = request.form['public_key']
    if public_key in DATANODES:
        sk = request.form['sk']
        DATANODES[public_key].sk = sk
        this.sks.append(sk)
        return 'Success'
    return 'Fail'


@serve_datanode.route('/submit_pic_hash', methods=['POST'])
def submit_pic():
    public_key = request.form['public_key']
    if public_key in DATANODES:
        DATANODES[public_key].training_images_hash = request.form['training_images_hash']
        DATANODES[public_key].test_images_hash = request.form['test_images_hash']
        return 'Success'
    return 'Fail'


@serve_consensus_node.route('/get_test_images_hash', methods=['GET'])
def get_test_images_hash():
    return json.dumps(this.test_images_hash)


@serve_consensus_node.route('/keys', methods=['GET'])
def keys():
    if len(this.sks) == len(this.employeelist):
        return json.dumps({'sks': this.sks, 'sign_sks': this.sign_sks, 'sign_mpks': this.sign_mpks})
    else:
        return 'Fail'


# @app.route('/task', methods=['GET'])
def release_task():
    task = {
        'mpks': this.mpks,
        'training_images_hash': this.train_images_hash,
        'company': [this.public_key, this.ip_addr]
    }
    # TODO 实现
    requests.post(f'http://{TASK_QUEUE_ADDR}/push_back', data=json.dumps(task))
# TODO 改成不定时对共识节点广播task

# TODO 从共识节点接收训练好的模型


if __name__ == '__main__':
    while True:
        t = threading.Thread(
            target=lambda: serve_datanode.run('127.0.0.1', 5000, debug=True,use_reloader=False),
            name='flask_thread')
        t.start()

        # TODO 设置training_images_hash(两堆变成两个)
        # TODO 在某个时刻调用release_task
        sleep(10)
        input('press a key to continue')
        release_task()
        requests.get(f'http://{this.ip_addr}/shutdown')
        sleep(1)

        # TODO 判断停止这一轮的时机
        t = threading.Thread(
            target=lambda: serve_consensus_node.run('127.0.0.1', 5000, debug=True,use_reloader=False),
            name='flask_thread')
        t.start()
        sleep(20)
        input('press a key to continue')
        requests.get(f'http://{this.ip_addr}/shutdown')
