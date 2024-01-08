import hashlib
import io 
import hmac

class Block:
    #MercleRoot?
    def __init__(self, index, timestamp, data, prevHash):
        self.index = index 
        self.timestamp = timestamp
        self.filename = data
        self.prevHash = prevHash

        self.hash = self.calcHash()
    
    def calcHash(self):
        """ buffer = io.BytesIO(b data.str())
        mac1 = hmac.HMAC(b"key", digestmod=hashlib.sha512)
        digest = hashlib.file_digest(buffer, lambda: mac1) """ 
        pass

#Permissioned = nur der Private Key Owner darf Blöcke Hinzufügen
#-> Was ist wenn der Ursprungsblock etwas enthält das nur der Owner entschlüsseln kann?
#Was ist mit den Mercle Trees
#Wo speichere ich diese Blockchain ? Bzw. wo lade Ich eine bereits erstellte?
class Blockchain:
    def __init__(self) -> None:
        pass

    def createBlockZero(self):
        pass

    def getLatestBlock(self):
        pass 

    def addNewBlock(self, newBlock):
        pass 
    
    #of What? That the Blockchain owner is rightous?
    def checkValidity(self):
        pass