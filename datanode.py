import requests
import time
import base64
import ecdsa
from flask import Flask
from flask import request

app = Flask(__name__)


class datanode:
    def __init__(self, ip_addr):
        """
        Give a ip_addr to create a wallet
        """
        self.ip_addr = ip_addr
        # personal wallet
        self.public_key = ''
        self.private_key = ''
        # encrypt algothrim
        self.mpk = []
        self.msk = []
        # transaction hash
        self.mpk_hash = ''
        self.training_images_hash = ''
        self.test_images_hash = ''
        # wait for receive
        self.company_public_key = ''
        self.z = []

    def generate_DPIPE_keys(self):
        """
        To generate Inner-Product-Encryption key-pairs
        
        Return mpk,msk
        """
        mpk = []
        msk = []
        return mpk, msk

    def generate_ECDSA_keys(self):
        """
        To generate Wallet key-pairs 

        Return public_key(base64) and private_key
        """
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)  # this is your sign (private key)
        private_key = sk.to_string().hex()  # convert your private key to hex
        vk = sk.get_verifying_key()  # this is your verification key (public key)
        public_key = vk.to_string().hex()
        public_key = base64.b64encode(bytes.fromhex(public_key))

        filename = "/wallet/{}.txt".format(self.ip_addr)
        with open(filename, "w") as f:
            f.write("Private key: {0}\nWallet address / Public key: {1}".format(private_key, public_key.decode()))
        print("Your new address and private key are now in the file {0}".format(filename))
        return public_key.decode(), private_key

    def image_encrypt(self,image):
        """
        To do DP and Inner-Product-Encrypt
        (image is 18*512 Matrix)
        """
        encrypted_image = []
        return encrypted_image

    def choice(self):
        response = None
        while response not in ["1", "2", "3", "4", "5"]:
            response = input("""What do you want to do?
            1. Generate new wallet and store the mpk in IPFS
            2. Upload the encrypted image and store the images in IPFS
            3. Send transactions
            4. Check transactions
            5. Quit\n""")
        if response == '1':
            # Generate new wallet
            self.public_key, self.private_key = self.generate_ECDSA_keys()
            self.mpk, self.msk = self.generate_DPIPE_keys()
            self.mpk_hash = self.store_in_IPFS(self.mpk)
        elif response == '2':
            if self.mpk and self.msk:
                upload = []  # images
                encrypted_images = self.image_encrypt(upload, self.mpk)
                self.training_images_hash = self.store_in_IPFS(
                    encrypted_images[:8])
                self.test_images_hash = self.store_in_IPFS(
                    encrypted_images[8:])
            else:
                print("mpk and msk is not exist.")
        elif response == "3":
            if self.public_key != '' and self.private_key != '':
                addr_from = self.public_key
                private_key = self.private_key
                addr_to = "companynode"
                mpk_hash = self.mpk_hash
                training_images_hash = self.training_images_hash
                test_images_hash = self.test_images_hash
                print("From: {0}\nPrivate Key: {1}\nTo: {2}\nMPK_hash: {3}\nTraining_Images_hash: {4}\nTest_Images_hash: {5}\n".format(
                    addr_from, private_key, addr_to, mpk_hash, training_images_hash, test_images_hash))
                response = input("y/n\n")
                if response.lower() == "y":
                    send_transaction(addr_from, private_key, addr_to,
                                     mpk_hash, training_images_hash, test_images_hash)
            else:
                print("public_key/wallet address and private_key is not exist.")
        elif response == "4":
            self.check_transactions()
        else:
            quit()

    



    def sign_ECDSA_msg(private_key,message):
        """
        Sign the message to be sent
        """
        # # Get timestamp, round it, make it into a string and encode it to bytes
        # message = str(round(time.time()))
        bmessage = message.encode()
        sk = ecdsa.SigningKey.from_string(
            bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        signature = base64.b64encode(sk.sign(bmessage))
        return signature, message

    

    def store_in_IPFS(thing):
        """
        IPFS
        """
        return hash_value

    def send_transaction(addr_from, private_key, addr_to, mpk_hash, training_images_hash, test_images_hash):
        """Sends your transaction to different nodes. Once any of the nodes manage
        to mine a block, your transaction will be added to the blockchain. Despite
        that, there is a low chance your transaction gets canceled due to other nodes
        having a longer chain. So make sure your transaction is deep into the chain
        before claiming it as approved!
        """
        if len(private_key) == 64:
            signature, message = sign_ECDSA_msg(private_key)
            url = 'http://localhost:5000/txion'
            payload = {"from": addr_from,
                       "to": addr_to,
                       "mpk_hash": mpk_hash,
                       "training_images_hash": training_images_hash,
                       "test_images_hash": test_images_hash,
                       "signature": signature.decode(),
                       "message": message}
            headers = {"Content-Type": "application/json"}

            res = requests.post(url, json=payload, headers=headers)
            print(res.text)
        else:
            print("Wrong address or key length! Verify and try again.")

    def check_transactions():
        """Retrieve the entire blockchain. With this you can check your
        wallets balance. If the blockchain is to long, it may take some time to load.
        """
        res = requests.get('http://localhost:5000/blocks')
        print(res.text)

    def pull_company_public_key(self):
        """
        pull from company
        """
        pass

    def pull_z(self):
        """
        pull from company
        """
        pass

    def generate_sk(self):
        """
        To use msk and z to generate the sk
        then send it to the company 
        """
        pass
node = datanode()

@app.route('/DP-Face/<employee_name>/public_key', method=['GET','POST'])
def pull_company_public_key():
    if request.method == 'POST':
        pass

@app.route('/DP-Face/<employee_name>/z', method=['GET','POST'])
def pull_company_z():
    if request.method == 'POST':
        request.form['asdf']
        pass

if __name__ == '__main__':
    print("===========Datanode===========")
    node = datanode()
    node.choice()
    input("Press ENTER to exit...")
