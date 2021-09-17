import hashlib
import json
def store_in_IPFS(public_key, data):
    """
    To store the data into IPFS

    Return address hash or null
    """
    data = {'public_key': public_key, 'data': data}

    hash_data = hashlib.sha256(str(data).encode()).hexdigest()

    if hash_data != '':
        filename = "./IPFS/database/{}.txt".format(hash_data)
        with open(filename, "w") as f:
            f.write(json.dumps(data))
        return hash_data
    else:
        print("[ Store in IPFS Error ]")
        return ''

def find_in_IPFS(data_hash):
    """
    To use hash to find data

    Return data(json)
    """
    if data_hash!='':
        filename = "./IPFS/database/{}.txt".format(data_hash)
        with open(filename, "r") as f:
            data = f.read()
            data = json.loads(data)
        if data != {}:
            return data
        else:
            print("[ Find in IPFS Error ]")
            return ''
    else:
        return "[ hash is empty ]"

