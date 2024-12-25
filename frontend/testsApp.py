import unittest
from flask import Flask
from flask_socketio import SocketIO, test_client
from app import app, socketio

class TestHealthMonitor(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.socketio_test_client = socketio.test_client(app)

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health Monitoring Dashboard', response.data)

    def test_socketio_connection(self):
        self.assertTrue(self.socketio_test_client.is_connected())

    def test_real_time_data_emission(self):
        # Connect to SocketIO and listen for `update_stats`
        received = self.socketio_test_client.get_received()
        self.assertTrue(any(event['name'] == 'update_stats' for event in received))

    def tearDown(self):
        self.socketio_test_client.disconnect()

if __name__ == "__main__":
    unittest.main()
