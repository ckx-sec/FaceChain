import ecdsa
import base64

class node:
    def __init__(self):
        self.public_key,self.private_key = self.generate_ECDSA_keys()
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
        return public_key.decode(), private_key

