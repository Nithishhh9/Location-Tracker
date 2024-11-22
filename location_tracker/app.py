from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
   
DATA_FILE = 'device_locations.json'

def load_device_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error decoding JSON, initializing empty data.")
            return {}
    return {}

def save_device_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('update_location')
def handle_location_update(data):
    device_name = data['device_name']
    location = data['location']
       
    device_data = load_device_data()
    device_data[device_name] = location
    save_device_data(device_data)
       
    socketio.emit('location_updated', device_data, broadcast=True)

if __name__ == '__main__':
   socketio.run(app, debug=True)