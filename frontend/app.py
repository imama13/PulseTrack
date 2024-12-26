from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread, Event
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

<<<<<<< Updated upstream
# Thread control
thread = None
thread_stop_event = Event()
=======
# Global variables to store sensor data
sensor_data = {
    "heartbeat": 88,
    "oxygen": 91,
    "gps": {"latitude": 33.6440950, "longitude": 72.9878090},
}
>>>>>>> Stashed changes

# Background task to simulate data emission
def emit_data():
    while not thread_stop_event.is_set():
        heartbeat = random.randint(60, 100)  # Simulate heartbeat
        oxygen = random.randint(90, 100)    # Simulate oxygen level
        gps_coords = {"latitude": 37.7749, "longitude": -122.4194}  # Simulate GPS coords

        # Emit data to frontend
        socketio.emit('update_stats', {
            "heartbeat": heartbeat,
            "oxygen": oxygen,
            "gps": gps_coords,
            "timestamp": time.strftime("%H:%M:%S"),  # Current time
        })
        time.sleep(5)  # Simulate data update interval

@socketio.on('connect')
def handle_connection():
    global thread
    if thread is None:
        thread_stop_event.clear()
        thread = Thread(target=emit_data)
        thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('disconnect')
def handle_disconnect():
    global thread
    thread_stop_event.set()
    thread = None

if __name__ == '__main__':
    socketio.run(app, debug=True)
