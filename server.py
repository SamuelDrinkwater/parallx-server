import io
import os
import time
import urllib
import requests
from flask import Flask, request, jsonify
from google.cloud import storage
from firebase import Firebase

config = {
  "apiKey": "AIzaSyAqU56OY_ouMU9Ih7qay2CCm0Lo8wd1oyE",
  "authDomain": "parallax-bc3d4.firebaseapp.com",
  "projectId": "parallax-bc3d4",
  "databaseURL": "https://parallax-bc3d4.firebaseio.com",
  "storageBucket": "parallax-bc3d4.appspot.com",
  "messagingSenderId": "293903582317",
  "appId": "1:293903582317:web:494ad78f1ceee7b3732b64"
}
firebase = Firebase(config)
storage = firebase.storage()


app = Flask(__name__)

def build_download_url(filename, token):
  return f"https://firebasestorage.googleapis.com/v0/b/parallax-bc3d4.appspot.com/o/{filename}?alt=media&token={token}"

def upload_to_firebase(filename):
  file_path = f"./results/{filename}"
  file_node = storage.child(filename)
  result = file_node.put(file_path)
  url = build_download_url(result["name"], result["downloadTokens"])
  return url

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def current_milli_time():
    return round(time.time() * 1000)

@app.route('/')
def index():
    return "Hello Canva 👋"

@app.route('/upload-test')
def upload():
  url = upload_to_firebase("doublestrike.jpg")
  return jsonify(url=url)

@app.route('/process', methods=['POST'])
def process_image():
    photo_url = request.json['url']
    photo_file = requests.get(photo_url, allow_redirects=True)
    open('photo_to_process.jpeg', 'wb').write(photo_file.content)

    file_name = f"{current_milli_time()}.mp4"
    os.system(f"python ./autozoom.py --in photo_to_process.jpeg --out ./results/{file_name}")

    url = upload_to_firebase(file_name)
    return jsonify(url=url)

@app.route('/shutdown', methods=['GET'])
def shutdown():
    os.system('killall ngrok')
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run()
