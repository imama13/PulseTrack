"""
Testing Strategy:
This test suite validates the functionality of a Flask and Flask-SocketIO application
that serves a health monitoring dashboard. It ensures that:
1. The main route correctly serves the dashboard.
2. Socket.IO connections can be established.
3. Real-time data emission from the server is functioning as expected.

Each test is isolated, and the `setUp` and `tearDown` methods handle initialization and cleanup for each test.
"""

import unittest
from flask import Flask
from flask_socketio import SocketIO, test_client
from app import app, socketio

class TestHealthMonitor(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by initializing the Flask app test client
        and a Flask-SocketIO test client.
        """
        self.app = app
        self.client = self.app.test_client()  # Test client for HTTP requests
        self.socketio_test_client = socketio.test_client(app)  # Test client for Socket.IO

    def test_index_route(self):
        """
        Test the '/' route to ensure it serves the main dashboard page.
        - Asserts the HTTP status code is 200 (success).
        - Verifies the response contains expected content (e.g., dashboard heading).
        """
        response = self.client.get('/')  # Send a GET request to the main route
        self.assertEqual(response.status_code, 200)  # Assert the route loads successfully
        self.assertIn(b'Health Monitoring Dashboard', response.data)  # Check for expected content

    def test_socketio_connection(self):
        """
        Test that a Socket.IO connection can be successfully established.
        - Uses the Socket.IO test client to assert connection status.
        """
        self.assertTrue(self.socketio_test_client.is_connected())  # Assert the client connects

    def test_real_time_data_emission(self):
        """
        Test that the server emits real-time data via the 'update_stats' event.
        - Connects to the Socket.IO server and listens for emitted events.
        - Verifies that at least one 'update_stats' event is received.
        """
        received = self.socketio_test_client.get_received()  # Get events received by the test client
        self.assertTrue(any(event['name'] == 'update_stats' for event in received))  # Assert the event is emitted

    def tearDown(self):
        """
        Clean up by disconnecting the Socket.IO test client after each test.
        """
        self.socketio_test_client.disconnect()  # Disconnect the test client

if __name__ == "__main__":
    unittest.main()
