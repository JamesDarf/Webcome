from flask import Flask, request, render_template, redirect
import os, pickle, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
app.secret_key = os.urandom(32)
AES_KEY = "tc112bplbHKUxq6+COt7XSYMyRHWqFqQzV+O6lO9lHgSNf/rt+1dnkXtlSZ6PcNW"  # 256-bit key for AES

try:
    FLAG = open('./flag.txt', 'r').read() # Flag is here!!
except:
    FLAG = '[**FLAG**]'

INFO = ['name', 'userid', 'password']

def encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_session', methods=['GET', 'POST'])
def create_session():
    if request.method == 'GET':
        return render_template('create_session.html')
    elif request.method == 'POST':
        info = {}
        for _ in INFO:
            info[_] = request.form.get(_, '')
        
        # Serialize and encrypt
        pickled_data = pickle.dumps(info)
        encrypted_data = encrypt(pickled_data)
        
        # Encode to base64 for safe transmission
        encoded_data = base64.b64encode(encrypted_data).decode('utf8')
        
        return render_template('create_session.html', data=encoded_data)

@app.route('/check_session', methods=['GET', 'POST'])
def check_session():
    if request.method == 'GET':
        return render_template('check_session.html')
    elif request.method == 'POST':
        session = request.form.get('session', '')
        
        try:
            # Decode from base64 and decrypt
            encrypted_data = base64.b64decode(session)
            decrypted_data = decrypt(encrypted_data)
            
            # Deserialize
            info = pickle.loads(decrypted_data)
            
            return render_template('check_session.html', info=info)
        except Exception as e:
            return render_template('check_session.html', error="Invalid session data")
        
# robots.txt
@app.route('/robots.txt')
def robot_to_root():
    return "User-agent: *\nDisallow: /index\nAES_KEY = tc112bplbHKUxq6+COt7XSYMyRHWqFqQzV+O6lO9lHgSNf/rt+1dnkXtlSZ6PcNW"
# robot....robot....

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)