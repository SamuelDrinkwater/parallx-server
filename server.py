import io
import os
import time
import urllib
import requests
from flask import Flask, request

app = Flask(__name__)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def current_milli_time():
    return round(time.time() * 1000)
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    os.system('killall ngrok')
    shutdown_server()
    return 'Server shutting down...'

@app.route('/process', methods=['POST'])
def process_image():
    photo_url = request.json['url']
    photo_file = requests.get(photo_url, allow_redirects=True)
    open('photo_to_process.jpeg', 'wb').write(photo_file.content)

    os.system(f"python ./autozoom.py --in photo_to_process.jpeg --out ./results/{current_milli_time()}.mp4")

    return "done"

@app.route('/')
def index():
    return "Hello Canva 👋"

if __name__ == '__main__':
    app.run()
