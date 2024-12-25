from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables to store sensor data
sensor_data = {
    "heartbeat": 80,
    "oxygen": 99,
    "gps": {"latitude": 33.6440950, "longitude": 72.9878090},
}

# Endpoint to receive data from the microcontroller
@app.route('/post_sensor_data', methods=['POST'])
def post_sensor_data():
    global sensor_data
    data = request.json  # Expect JSON data from the microcontroller
    if data:
        sensor_data["heartbeat"] = data.get("bpm", 0)
        sensor_data["oxygen"] = data.get("oxy", 0)
        lat = data.get("lat", 0.0)  # Get 'lat' from the JSON
        lon = data.get("lon", 0.0)  # Get 'lon' from the JSON
        sensor_data["gps"] = {"latitude": lat, "longitude": lon}
        return jsonify({"status": "success", "message": "Data received successfully!"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

# Endpoint to provide data to the frontend
@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify(sensor_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
