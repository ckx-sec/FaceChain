from time import sleep
from flask import Flask
# from demo import *
from models import *
import requests
import sys

name=sys.argv[1]
# TODO 补上ip
this = datanode(f'datanode_{name}', 'localhost:5000')

# TODO 处理图片
this.training_images_hash = store_in_IPFS(this, this.train_images)
this.test_images_hash = store_in_IPFS(this, this.test_images)

# TODO 加密

# TODO 传进ipfs
this.mpk_hash = store_in_IPFS(this, this.mpk)
print(this.mpk_hash)

resp = requests.post(f'http://{this.company_addr}/register', data={
    'public_key': this.public_key, 'mpk_hash': this.mpk_hash})
assert resp.text == 'Success'

while True:
    try:
        resp = requests.get(f'http://{this.company_addr}/get_z')
        this.z = resp.json()['z']
        print('z: ', len(this.z))
    except ValueError as e:
        # print(e)
        sleep(1)
        continue
    break


this.compute_sk()
resp = requests.post(f'http://{this.company_addr}/submit_sk', data={'public_key':this.public_key,'sk': this.sk})
assert resp.text == 'Success'

resp = requests.post(f'http://{this.company_addr}/submit_pic_hash', data={ # 加上public key
                     'public_key':this.public_key,'training_images_hash': this.training_images_hash, 'test_images_hash': this.test_images_hash})
assert resp.text == 'Success'
