
from flask import Flask, request, render_template, make_response
import os, pickle, base64
import logging
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

logging.basicConfig(filename="./app.log", level=logging.DEBUG) #logging
app = Flask(__name__)
app.secret_key = os.urandom(32) # AES key 생성
AES_KEY = "36f6d9a966c4478c73af4fde2f813212"  # 256-bit key for AES


FLAG = open('./flag.txt', 'r').read() # Flag is "./flag.txt" !!


INFO = ['name', 'userid', 'password']

def encrypt(data):
    cipher = AES.new(AES_KEY.encode(), AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    cipher = AES.new(AES_KEY.encode(), AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_vsession', methods=['GET', 'POST']) # 직렬화
def create_vsession():
    if request.method == 'GET':
        return render_template('create_vsession.html')
    elif request.method == 'POST':
        info = {}
        for _ in INFO:
            info[_] = request.form.get(_, '')
        try:
            data = base64.b64encode(encrypt(pickle.dumps(info))).decode('utf8') # pickle.dumps한 것을 바이트 타입에서 문자열로 변환
            return render_template('create_vsession.html', data=data)
        except:
            return "wrong!"
    else:
        return "wrong"

@app.route('/check_vsession', methods=['GET', 'POST']) # 역직렬화
def check_vsession():
    if request.method == 'GET':
        return render_template('check_vsession.html')
    elif request.method == 'POST':
        try:
            vsession = request.form.get('session', '')
            info = pickle.loads(decrypt(base64.b64decode(vsession))) # 문자열을 바이트로 디코딩하고 이걸 역직렬화하여 원래 데이터로 변환.(이때 취약점 발생)
            logging.debug(f"아이피 {request.remote_addr}가 check_session을 시도함. {info}")
            res = make_response(render_template('check_vsession.html', info=info))
            res.headers.set('X-AES-KEY', f"{AES_KEY}")
            return res
        except:
            return "wrong"
    else:
        return "wrong"

app.run(host='0.0.0.0', port=8000)
