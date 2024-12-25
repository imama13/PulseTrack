import pytest
from flask import Flask
from flask.testing import FlaskClient
import sys
import os
# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import app from the parent directory

# Global variable to store sensor data (this should match the one in the app)
sensor_data = {
    "heartbeat": 80,
    "oxygen": 99,
    "gps": {"latitude": 33.6440950, "longitude": 72.9878090},
}

@pytest.fixture
def client():
    """Fixture for the Flask test client."""
    with app.test_client() as client:
        # Reset the sensor_data before each test to ensure the correct initial state
        global sensor_data
        sensor_data = {
            "heartbeat": 80,
            "oxygen": 99,
            "gps": {"latitude": 33.6440950, "longitude": 72.9878090},
        }
        yield client

def test_get_sensor_data(client):
    # First, get the sensor data from the endpoint
    response = client.get('/get_sensor_data')

    # Assert that the response status is 200 (success)
    assert response.status_code == 200
    assert response.json["heartbeat"] == 80  # Default value
    assert response.json["oxygen"] == 99  # Default value
    assert response.json["gps"] == {"latitude": 33.6440950, "longitude": 72.9878090}

def test_post_sensor_data(client):
    # Send new sensor data to the endpoint
    new_data = {
        "bpm": 75,
        "oxy": 90,
        "lat": 33.6450000,
        "lon": 72.9880000,
    }
    response = client.post('/post_sensor_data', json=new_data)

    # Assert that the response status is 200 (success)
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Data received successfully!"

    # Now check if the data is updated
    response = client.get('/get_sensor_data')
    assert response.json["heartbeat"] == 75
    assert response.json["oxygen"] == 90
    assert response.json["gps"] == {"latitude": 33.6450000, "longitude": 72.9880000}