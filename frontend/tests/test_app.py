import pytest
from unittest.mock import patch
import mongomock
from pymongo import MongoClient
import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import app from the parent directory

@pytest.fixture
def client():
    """Fixture for the Flask test client with mocked MongoDB."""
    with patch('app.MongoClient', return_value=mongomock.MongoClient()) as mocked_client:
        with app.test_client() as client:
            # Get a reference to the mocked database and collection
            db = mocked_client()['sensor_database']
            collection = db['sensor_data']
            # Reset database state
            collection.delete_many({})
            collection.insert_one({
                "heartbeat": 80,
                "oxygen": 99,
                "gps": {"latitude": 33.6440950, "longitude": 72.9878090},
            })
            yield client

def test_get_sensor_data(client):
    """Test retrieving sensor data."""
    # Make a GET request to fetch sensor data
    response = client.get('/get_sensor_data')

    # Assertions for the response
    assert response.status_code == 200
    assert response.json["heartbeat"] == 75  # Check initial heartbeat value
    assert response.json["oxygen"] == 90  # Check initial oxygen value
    assert response.json["gps"] == {"latitude": 33.645, "longitude": 72.988}

def test_post_sensor_data(client):
    """Test posting new sensor data."""
    # New data to send to the POST endpoint
    new_data = {
        "bpm": 75,
        "oxy": 90,
        "lat": 33.6450000,
        "lon": 72.9880000,
    }
    # Make a POST request to update sensor data
    response = client.post('/post_sensor_data', json=new_data)

    # Assertions for the POST response
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["message"] == "Data received and stored in MongoDB!"

    # Verify that the data was updated by fetching it again
    response = client.get('/get_sensor_data')
    assert response.status_code == 200
    assert response.json["heartbeat"] == 75  # Updated heartbeat value
    assert response.json["oxygen"] == 90  # Updated oxygen value
    assert response.json["gps"] == {"latitude": 33.6450000, "longitude": 72.9880000}