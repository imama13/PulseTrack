from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Simulate real-time sensor data
@socketio.on('connect')
def handle_connection():
    while True:
        # Simulate sensor data
        heartbeat = random.randint(60, 100)  # Example value  replace with requests!!!!!!!!!!!!!!!!!!
        oxygen = random.randint(90, 100)    # Example value
        gps_coords = {"latitude": 37.7749, "longitude": -122.4194}  # Example coords
        
        # Emit data to frontend
        socketio.emit('update_stats', {
            "heartbeat": heartbeat,
            "oxygen": oxygen,
            "gps": gps_coords,
        })
        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
