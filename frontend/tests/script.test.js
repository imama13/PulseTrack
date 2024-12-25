const { fetchSensorData } = require('../static/script.js');

// Mock fetch globally
global.fetch = jest.fn();

// Mock the alert sound (audio element)
const mockAlertSound = {
    play: jest.fn().mockResolvedValue(undefined), // Returning a resolved promise for play()
    pause: jest.fn(),
    currentTime: 0,
    paused: true,
};

// Mock the map and related methods (for `setView`, `marker.setLatLng`, etc.)
global.L = {
    map: jest.fn().mockReturnValue({
        setView: jest.fn(), // Mocking `setView` method
        addLayer: jest.fn(),
        removeLayer: jest.fn(),
        marker: jest.fn().mockReturnValue({
            setLatLng: jest.fn(), // Mock `setLatLng` for marker update
        }),
    }),
};

// Mock Chart.js and its methods
global.Chart = jest.fn().mockImplementation(() => ({
    update: jest.fn(),
    data: {
        labels: [],
        datasets: [
            {
                data: [],
            },
            {
                data: [],
            },
        ],
    },
}));

// Mock getChart function for Chart.js
global.Chart.getChart = jest.fn().mockReturnValue({
    update: jest.fn(),
    data: {
        labels: [],
        datasets: [
            {
                data: [],
            },
            {
                data: [],
            },
        ],
    },
});

beforeEach(() => {
    // Reset the DOM structure before each test
    document.body.innerHTML = `
        <div id="alert" class="hidden"></div>
        <span id="heartbeat">--</span>
        <span id="oxygen">--</span>
        <canvas id="statsChart"></canvas>
        <audio id="alertSound"></audio>
    `;

    // Mock `getElementById` to return correct DOM elements
    jest.spyOn(document, 'getElementById').mockImplementation((id) => {
        if (id === 'alertSound') return mockAlertSound;
        return document.querySelector(`#${id}`);
    });

    jest.useFakeTimers(); // Use fake timers for interval control
    fetch.mockClear();
    mockAlertSound.play.mockClear();
    mockAlertSound.pause.mockClear();
});

afterEach(() => {
    jest.clearAllTimers();
    jest.resetAllMocks();
    jest.restoreAllMocks();
});

describe('fetchSensorData', () => {
    let mockResponse;

    beforeEach(() => {
        mockResponse = {
            gps: { latitude: 33.642125, longitude: 72.991072 },
            heartbeat: 80,
            oxygen: 95,
        };
    });

    it('updates the UI with fetched data', async () => {
        fetch.mockResolvedValueOnce({
            json: jest.fn().mockResolvedValueOnce(mockResponse),
        });

        await fetchSensorData();

        // Assertions to verify UI updates
        expect(document.getElementById('heartbeat').textContent).toBe('80');
        expect(document.getElementById('oxygen').textContent).toBe('95');
    });

    it('handles critical health parameters with alerts', async () => {
        mockResponse.heartbeat = 50; // Critical value
        fetch.mockResolvedValueOnce({
            json: jest.fn().mockResolvedValueOnce(mockResponse),
        });

        // Simulate the first fetchSensorData call
        await fetchSensorData();

        const alertElement = document.getElementById('alert');

        // Assert that the alert is shown and sound plays
        expect(alertElement).not.toBeUndefined(); // Ensure the element exists
        expect(alertElement.classList.contains('hidden')).toBe(false); // Alert visible
        expect(mockAlertSound.play).toHaveBeenCalled(); // Alert sound played

        // Prepare mock data for the next update
        mockResponse.heartbeat = 80; // Normal value
        fetch.mockResolvedValueOnce({
            json: jest.fn().mockResolvedValueOnce(mockResponse),
        });

        // Simulate the second fetchSensorData call after 5 seconds
        jest.advanceTimersByTime(5000);
        await fetchSensorData();

        // Assert that the alert is hidden and sound stops
        expect(alertElement.classList.contains('hidden')).toBe(true); // Alert hidden
        expect(mockAlertSound.pause).toHaveBeenCalled(); // Alert sound stopped
        expect(mockAlertSound.currentTime).toBe(0); // Reset playback position
    });

    it('handles errors gracefully', async () => {
        fetch.mockRejectedValueOnce(new Error('Network error'));

        console.error = jest.fn(); // Mock console.error

        await fetchSensorData();

        expect(console.error).toHaveBeenCalledWith(
            'Error fetching sensor data:',
            expect.any(Error)
        );
    });
});
