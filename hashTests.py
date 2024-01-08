import hashlib
import io
import hmac

""" string = "Test"
print(hashlib.sha256(string.encode()).hexdigest()) """
buffer = io.BytesIO(b"3.gif")
mac1 = hmac.HMAC(b"key", digestmod=hashlib.sha512)
digest = hashlib.file_digest(buffer, lambda: mac1)
print(digest.hexdigest())
