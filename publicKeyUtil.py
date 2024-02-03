from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa  

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import traceback

def __save_file(filename, content):  
   f = open(filename, "wb")  
   f.write(content) 
   f.close()

def create_Key_Pair_and_write_to_file(username):
    # generate private key & write to disk  
    private_key = rsa.generate_private_key(  
        public_exponent=65537,  
        key_size=4096,  
        backend=default_backend()  
    )  
    pem = private_key.private_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PrivateFormat.PKCS8,  
        encryption_algorithm=serialization.NoEncryption()  
    )  
    __save_file("keys/" + username + "Private.pem", pem)  
    
    # generate public key  
    public_key = private_key.public_key()  
    pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo  
    )  
    __save_file("keys/" + username + "Public.pem", pem) 

def load_private_key(username):
    with open("keys/" + username + "Private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def load_public_key(username):
    with open("keys/" + username + "Public.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key 

def create_signature_for_message(message, private_Key):
    signature = private_Key.sign(
        message, 
        padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
        hashes.SHA256()
    )
    return signature

def check_if_signature_matches_message(message, public_key, signature):
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
            hashes.SHA256()
        )
        print("Signature valid")
        return True
    except Exception:
        traceback.print_exc()
        print("Signature invalid") 
        return False
