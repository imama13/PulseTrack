from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['sensor_data_db']  # Database name
collection = db['sensor_data']  # Collection name

# Endpoint to receive data from the microcontroller
@app.route('/post_sensor_data', methods=['POST'])
def post_sensor_data():
    data = request.json  # Expect JSON data from the microcontroller
    if data:
        # Insert data into MongoDB
        collection.insert_one({
            "heartbeat": data.get("bpm", 0),
            "oxygen": data.get("oxy", 0),
            "gps": {
                "latitude": data.get("lat", 0.0),
                "longitude": data.get("lon", 0.0),
            }
        })
        return jsonify({"status": "success", "message": "Data received and stored in MongoDB!"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

# Endpoint to provide data to the frontend
@app.route('/get_sensor_data', methods=['GET'])
def get_sensor_data():
    # Get the latest document from MongoDB
    latest_data = collection.find_one(sort=[("_id", -1)])
    if latest_data:
        # Remove MongoDB's internal ID field (_id) for JSON compatibility
        latest_data.pop("_id", None)
        return jsonify(latest_data)
    return jsonify({"status": "error", "message": "No data available"}), 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
