from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Global variables to store sensor data
sensor_data = {
    "heartbeat": 0,
    "oxygen": 0,
    "gps": {"latitude": 0.0, "longitude": 0.0},
}

# Endpoint to receive data from the microcontroller
@app.route('/post_sensor_data', methods=['POST'])
def post_sensor_data():
    global sensor_data
    data = request.json  # Expect JSON data from the microcontroller
    if data:
        sensor_data["heartbeat"] = data.get("heartbeat", 0)
        sensor_data["oxygen"] = data.get("oxygen", 0)
        sensor_data["gps"] = data.get("gps", {"latitude": 0.0, "longitude": 0.0})
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
