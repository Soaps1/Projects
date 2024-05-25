from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

countries = [
    {"name": "South Africa", "lat": -30.5595, "lng": 22.9375},
    {"name": "United States", "lat": 37.0902, "lng": -95.7129},
    {"name": "Brazil", "lat": -14.2350, "lng": -51.9253},
    {"name": "Australia", "lat": -25.2744, "lng": 133.7751},
    {"name": "India", "lat": 20.5937, "lng": 78.9629},
    {"name": "Canada", "lat": 56.1304, "lng": -106.3468},
    {"name": "China", "lat": 35.8617, "lng": 104.1954},
    {"name": "Russia", "lat": 61.5240, "lng": 105.3188},
    {"name": "France", "lat": 46.6034, "lng": 1.8883},
    {"name": "Germany", "lat": 51.1657, "lng": 10.4515},
    {"name": "Argentina", "lat": -38.4161, "lng": -63.6167},
    {"name": "Mexico", "lat": 23.6345, "lng": -102.5528},
    {"name": "United Kingdom", "lat": 55.3781, "lng": -3.4360},
    {"name": "Italy", "lat": 41.8719, "lng": 12.5674},
    {"name": "Spain", "lat": 40.4637, "lng": -3.7492},
    {"name": "Japan", "lat": 36.2048, "lng": 138.2529},
    {"name": "South Korea", "lat": 35.9078, "lng": 127.7669},
    {"name": "Saudi Arabia", "lat": 23.8859, "lng": 45.0792},
    {"name": "Indonesia", "lat": -0.7893, "lng": 113.9213},
    {"name": "Turkey", "lat": 38.9637, "lng": 35.2433},
    {"name": "Netherlands", "lat": 52.1326, "lng": 5.2913},
    {"name": "Belgium", "lat": 50.8503, "lng": 4.3517},
    {"name": "Sweden", "lat": 60.1282, "lng": 18.6435},
    {"name": "Norway", "lat": 60.4720, "lng": 8.4689},
    {"name": "Finland", "lat": 61.9241, "lng": 25.7482},
    {"name": "Denmark", "lat": 56.2639, "lng": 9.5018},
    {"name": "Ireland", "lat": 53.4129, "lng": -8.2439},
    {"name": "Portugal", "lat": 39.3999, "lng": -8.2245},
    {"name": "Greece", "lat": 39.0742, "lng": 21.8243},
    {"name": "Poland", "lat": 51.9194, "lng": 19.1451},
    {"name": "Czech Republic", "lat": 49.8175, "lng": 15.4730},
    {"name": "Austria", "lat": 47.5162, "lng": 14.5501},
    {"name": "Switzerland", "lat": 46.8182, "lng": 8.2275},
    {"name": "Hungary", "lat": 47.1625, "lng": 19.5033},
    {"name": "Romania", "lat": 45.9432, "lng": 24.9668},
    {"name": "Bulgaria", "lat": 42.7339, "lng": 25.4858},
    {"name": "Serbia", "lat": 44.0165, "lng": 21.0059},
    {"name": "Croatia", "lat": 45.1, "lng": 15.2},
    {"name": "Slovenia", "lat": 46.1512, "lng": 14.9955},
    {"name": "Slovakia", "lat": 48.6690, "lng": 19.6990},
    {"name": "Ukraine", "lat": 48.3794, "lng": 31.1656},
    {"name": "Belarus", "lat": 53.7098, "lng": 27.9534},
    {"name": "Lithuania", "lat": 55.1694, "lng": 23.8813},
    {"name": "Latvia", "lat": 56.8796, "lng": 24.6032},
    {"name": "Estonia", "lat": 58.5953, "lng": 25.0136},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_random_country')
def get_random_country():
    country = random.choice(countries)
    return jsonify(country)

if __name__ == '__main__':
    app.run(debug=True)
