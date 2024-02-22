from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa  

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import hashlib

import os

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

def load_public_key_with_filepath(filepath):
    with open(filepath, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key

def write_Signature_To_File(message, username, blockchain_Name):
    if not ( os.path.exists('keys/' + username + "Private.pem") and os.path.exists('keys/' + username + "Public.pem") ):
        print("KeyPair Not Found, Generating")
        create_Key_Pair_and_write_to_file(username)
    signature = create_signature_for_message(message, load_private_key(username))
    writer = open("blockchains/" + blockchain_Name[:-4] + username + ".cert", "wb")
    writer.write(signature)
    writer.close()

def load_Signature_From_File(signature_Name):
    reader = open(signature_Name, "rb")
    signature = reader.read()
    return signature

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
        #print("Signature valid")
        return True
    except Exception:
        traceback.print_exc()
        print("Signature invalid") 
        return False

def get_SHA256_Hash_from_File(file_Name):
        hash = hashlib.sha256()
        fileInputHash = open(file_Name, "rb")
        while True:
            data = fileInputHash.read(4096)
            if not data:
                break 
            hash.update(data)
        fileInputHash.close()
        return hash.hexdigest()

def get_SHA512_Hash_from_File(file_Name):
        hash = hashlib.sha512()
        fileInputHash = open(file_Name, "rb")
        while True:
            data = fileInputHash.read(4096)
            if not data:
                break 
            hash.update(data)
        fileInputHash.close()
        return hash.hexdigest()

def encrypt_Message_With_Public_key(message, public_key):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_Message_With_Private_key(cipher, private_key):
    message = private_key.decrypt(
        cipher,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return message



#test = get_SHA512_Hash_from_File("keys/AlicePublic.pem")
#print(test)


#message = get_SHA256_Hash_from_File("blockchains/Winterexpo.txt").encode()
#print(message)
#test = encrypt_Message_With_Public_key(message, load_public_key("Winterexpo"))
#test2 = decrypt_Message_With_Private_key(test, load_private_key("Winterexpo"))
#print(test2.decode())
#write_Signature_To_File(message, "Alice", "BlenderGuruDonut")
#signature = load_Signature_From_File("blockchains/WinterexpoWinterexpo.cert")
#print(check_if_signature_matches_message(message,load_public_key("Winterexpo"), signature))
