import random
import time
import requests

# Function to simulate dummy data
def generate_dummy_data():
    while True:
        # Generate random values for heartbeat (75-90) and oxygen (84-100)
        heartbeat = random.randint(89, 90)
        oxygen = random.randint(93, 100)
        gps = {"latitude": 33.6440950, "longitude": 72.9878090}

        # Combine data
        data = {
            "bpm": heartbeat,
            "oxy": oxygen,
            "lat": gps["latitude"],
            "lon": gps["longitude"],
        }

        # Print or send data
        print(f"Sending data: {data}")

        # Send data to your Flask app
        try:
            response = requests.post("http://127.0.0.1:5001/post_sensor_data", json=data)
            print(f"Response: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")

        # Wait for a short period before sending the next batch
        time.sleep(2)  # Adjust as needed

# Call the function
if __name__ == "__main__":
    generate_dummy_data()
