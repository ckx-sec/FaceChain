with open('./config/company_info.txt', 'w') as file:
    file.write('')
with open('./config/consensus_info.txt', 'w') as file:
    file.write('')

import os

folder_path = './wallet/datanode/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.system('rm -rf %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_path = './wallet/companynode/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.system('rm -rf %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_path = './wallet/consensusnode/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.system('rm -rf %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_path = './blockchain/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.system('rm -rf %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

folder_path = './IPFS/database/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.system('rm -rf %s' % file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))