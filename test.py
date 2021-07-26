from demo import Block
import time

b = Block(0, time.time(), {'node': '', 'acc': -1, 'model': '', 'company': ''}, {'company': 'asdfasdf','company_ip':'', 'mpks_hash': '', 'training_images_hash': ''}, '0')
print(b.__dict__)