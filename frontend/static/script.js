// Variables for the map
let map, marker;

// Function to initialize the map
function initMap(lat, lng) {
    // Initialize the map and set the initial view
    map = L.map('map').setView([lat, lng], 15); // Adjust zoom level as needed
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add a marker at the initial location
    marker = L.marker([lat, lng]).addTo(map);
}

// Function to update the map location
function updateMap(lat, lng) {
    // Update the map's center
    if (map) {
        map.setView([lat, lng]);

        // Update the marker's position
        if (marker) {
            marker.setLatLng([lat, lng]);
        }
    }
}

async function fetchSensorData() {
    try {
        // DOM elements
        const heartbeatElem = document.getElementById("heartbeat");
        const oxygenElem = document.getElementById("oxygen");
        const alertElement = document.getElementById("alert");
        const alertSound = document.getElementById("alertSound");
        const response = await fetch('/get_sensor_data');
        const data = await response.json();
        console.log("Received Data:", data);
        let bpm = parseInt(data.heartbeat);
        let oxy = parseInt(data.oxygen);

        // Update UI elements with received data
        document.getElementById("heartbeat").textContent = `${data.heartbeat}`;
        document.getElementById("oxygen").textContent = `${data.oxygen}`;

        // Add data to chart
        const chart = Chart.getChart("statsChart");
        if (chart) {
            // Add new data
            chart.data.labels.push(new Date().toLocaleTimeString());
            chart.data.datasets[0].data.push(data.heartbeat);
            chart.data.datasets[1].data.push(data.oxygen);

            chart.update();
            // Maintain a sliding window of 12 values
            if (chart.data.labels.length > 12) {
                chart.data.labels.shift(); // Remove the oldest label
                chart.data.datasets[0].data.shift(); // Remove the oldest heartbeat value
                chart.data.datasets[1].data.shift(); // Remove the oldest oxygen value
            }
        }

        // Update map location
        updateMap(data.gps.latitude, data.gps.longitude);

        // Trigger alerts for critical values
        if (bpm < 60 || bpm > 150 || oxy < 85) {
            if (alertElement.classList.contains("hidden")) {
                alertElement.classList.remove("hidden");
            }
            try {
                alertSound.play();
            } catch (error) {
                console.error("Audio playback failed:", error);
            }
        } else {
            alertElement.classList.add("hidden");
            alertSound.pause();
            alertSound.currentTime = 0;
        }
    } catch (error) {
        console.error("Error fetching sensor data:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Initialize the map with default coordinates
    initMap(33.6440950, 72.9878090);

    // Initialize the chart
    const ctx = document.getElementById("statsChart").getContext("2d");
    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [], // Timestamps
            datasets: [
                {
                    label: "Heartbeat (bpm)",
                    data: [],
                    borderColor: "red",
                    backgroundColor: "rgba(255, 0, 0, 0.2)",
                    fill: true,
                },
                {
                    label: "Oxygen Level (%)",
                    data: [],
                    borderColor: "blue",
                    backgroundColor: "rgba(0, 0, 255, 0.2)",
                    fill: true,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display: true, text: "Time" },
                },
                y: {
                    title: { display: true, text: "Value" },
                },
            },
        },
    });

    fetchSensorData();
    // Fetch sensor data every 5 seconds
    setInterval(fetchSensorData, 5000);
});

module.exports = { fetchSensorData };