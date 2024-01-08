import base64
from PIL import Image
import io

imageFileObj = open("media/Screenshots/test2.png", "rb")
imageBinaryBytes = imageFileObj.read()
imageBinary = base64.b64encode(imageBinaryBytes)
imageFileObj.close()

blockchainWrite = open("blockchains/bchain.txt", "wb")
blockchainWrite.write(imageBinary)
blockchainWrite.close()

""" imageFileObj = open("media/Screenshots/test.png", "rb")
imageBinaryBytes = imageFileObj.read()
imageBinary = base64.b64encode(imageBinaryBytes)
imageFileObj.close()

blockchainWrite = open("blockchains/bchain.txt", "a")
blockchainWrite.write("\n")
blockchainWrite.close()

blockchainWrite = open("blockchains/bchain.txt", "ab")
blockchainWrite.write(imageBinary)
blockchainWrite.close() """

blockchainRead = open("blockchains/bchain.txt", "rb")
blockchainBytes = blockchainRead.read().splitlines()
pngBytes = base64.b64decode(blockchainBytes[0])
blockchainRead.close()


imageStream = io.BytesIO(pngBytes) 
imageFile = Image.open(imageStream)
imageFile.save("media/Screenshots/ReadFromFile.png") 
imageFile.close()