// Establish a connection with the server using Socket.IO
const socket = io();

// DOM elements
const heartbeatElem = document.getElementById("heartbeat");
const oxygenElem = document.getElementById("oxygen");

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
    map.setView([lat, lng]);

    // Update the marker's position
    if (marker) {
        marker.setLatLng([lat, lng]);
    }
}

// Handle real-time updates from the server
socket.on("update_stats", (data) => {
    // Update DOM elements
    heartbeatElem.textContent = `${data.heartbeat} bpm`;
    oxygenElem.textContent = `${data.oxygen}%`;

    // Add new data to the chart
    const timestamp = data.timestamp; // Expecting timestamp in "HH:mm:ss" format
    chart.data.labels.push(timestamp);
    chart.data.datasets[0].data.push(data.heartbeat);
    chart.data.datasets[1].data.push(data.oxygen);

    // Keep the chart within the current day's data
    if (chart.data.labels.length > 288) { // 288 points = 24 hours (5-second intervals)
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
        chart.data.datasets[1].data.shift();
    }

    chart.update();

    // Update or initialize the map
    if (map) {
        updateMap(data.gps.latitude, data.gps.longitude);
    } else {
        initMap(data.gps.latitude, data.gps.longitude);
    }
});

// Handle loading the full day's data when the page loads
socket.on("load_history", (history) => {
    chart.data.labels = history.timestamps;
    chart.data.datasets[0].data = history.heartbeat;
    chart.data.datasets[1].data = history.oxygen;
    chart.update();

    // Set the initial map location if available
    if (history.gps && history.gps.length > 0) {
        const lastCoords = history.gps[history.gps.length - 1];
        initMap(lastCoords.latitude, lastCoords.longitude);
    }
});


// Initialize the map with default coordinates
initMap(33.642125, 72.991072); 

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