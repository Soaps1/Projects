let points = 0;
let lives = 3;
let currentCountry;

const map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=your.mapbox.access.token', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'mapbox.access.token'
}).addTo(map);

function fetchRandomCountry() {
    fetch('/get_random_country')
        .then(response => response.json())
        .then(country => {
            currentCountry = country;
            document.getElementById('prompt').innerText = `Pin: ${currentCountry.name}`;
        });
}

function updateStatus(message) {
    document.getElementById('status').innerText = message;
}

function updatePoints() {
    document.getElementById('points').innerText = points;
}

function updateLives() {
    document.getElementById('lives').innerText = lives;
}

function resetGame() {
    points = 0;
    lives = 3;
    updatePoints();
    updateLives();
    fetchRandomCountry();
}

map.on('click', function (e) {
    const { lat, lng } = e.latlng;
    const distance = map.distance([lat, lng], [currentCountry.lat, currentCountry.lng]);

    if (distance < 500000) {
        points++;
        updateStatus('Correct!');
    } else {
        lives--;
        updateStatus('Incorrect!');
    }

    updatePoints();
    updateLives();

    if (lives === 0) {
        alert('Game over! Restarting...');
        resetGame();
    } else {
        fetchRandomCountry();
    }
});

fetchRandomCountry();
