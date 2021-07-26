from flask import Flask, request

TASK_QUEUE = []

app = Flask(__name__)


@app.route('/push_back', methods=['POST'])
def push_back():
    TASK_QUEUE.append(request.get_json(force=True))
    return 'Success'


@app.route('/get_front', methods=['GET'])
def get_front():
    return TASK_QUEUE[0]


@app.route('/pop_front', methods=['GET'])
def pop_front():
    if len(TASK_QUEUE) == 1:
        return TASK_QUEUE[0]
    else:
        return TASK_QUEUE.pop(0)


app.run('127.0.0.1', 9000)
