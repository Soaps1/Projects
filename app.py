from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "capital_guesser"  # for session

COUNTRIES_DATA = {
    'USA': {'capital': 'Washington, D.C.', 'cities': ['New York', 'Los Angeles', 'Chicago']},
    'Canada': {'capital': 'Ottawa', 'cities': ['Toronto', 'Vancouver', 'Montreal']},
    'Germany': {'capital': 'Berlin', 'cities': ['Hamburg', 'Munich', 'Cologne']},
    'France': {'capital': 'Paris', 'cities': ['Marseille', 'Lyon', 'Toulouse']},
    'Japan': {'capital': 'Tokyo', 'cities': ['Osaka', 'Yokohama', 'Nagoya']},
    'United Kingdom': {'capital': 'London', 'cities': ['Birmingham', 'Liverpool', 'Manchester']},
    'Italy': {'capital': 'Rome', 'cities': ['Milan', 'Naples', 'Turin']},
    'Australia': {'capital': 'Canberra', 'cities': ['Sydney', 'Melbourne', 'Brisbane']},
    'Brazil': {'capital': 'Brasília', 'cities': ['São Paulo', 'Rio de Janeiro', 'Salvador']},
    'Russia': {'capital': 'Moscow', 'cities': ['Saint Petersburg', 'Novosibirsk', 'Yekaterinburg']},
    'India': {'capital': 'New Delhi', 'cities': ['Mumbai', 'Bangalore', 'Kolkata']},
    'Argentina': {'capital': 'Buenos Aires', 'cities': ['Córdoba', 'Rosario', 'Mendoza']},
    'China': {'capital': 'Beijing', 'cities': ['Shanghai', 'Hong Kong', 'Guangzhou']},
    'South Africa': {'capital': 'Pretoria', 'cities': ['Johannesburg', 'Cape Town', 'Durban']},
    'Egypt': {'capital': 'Cairo', 'cities': ['Alexandria', 'Giza', 'Shubra El Kheima']},
    'Spain': {'capital': 'Madrid', 'cities': ['Barcelona', 'Valencia', 'Seville']},
    'Mexico': {'capital': 'Mexico City', 'cities': ['Guadalajara', 'Monterrey', 'Tijuana']},
    'Norway': {'capital': 'Oslo', 'cities': ['Bergen', 'Stavanger', 'Trondheim']},
    'Turkey': {'capital': 'Ankara', 'cities': ['Istanbul', 'Izmir', 'Bursa']},
    'Greece': {'capital': 'Athens', 'cities': ['Thessaloniki', 'Patras', 'Heraklion']},
    'Sweden': {'capital': 'Stockholm', 'cities': ['Gothenburg', 'Malmo', 'Uppsala']},
    'Finland': {'capital': 'Helsinki', 'cities': ['Espoo', 'Tampere', 'Vantaa']},
    'Ireland': {'capital': 'Dublin', 'cities': ['Cork', 'Limerick', 'Galway']},
    'New Zealand': {'capital': 'Wellington', 'cities': ['Auckland', 'Christchurch', 'Hamilton']},
    'Nigeria': {'capital': 'Abuja', 'cities': ['Lagos', 'Kano', 'Ibadan']},
    'Switzerland': {'capital': 'Bern', 'cities': ['Zurich', 'Geneva', 'Basel']},
    'Belgium': {'capital': 'Brussels', 'cities': ['Antwerp', 'Ghent', 'Charleroi']},
    'Netherlands': {'capital': 'Amsterdam', 'cities': ['Rotterdam', 'The Hague', 'Utrecht']},
    'Portugal': {'capital': 'Lisbon', 'cities': ['Porto', 'Vila Nova de Gaia', 'Amadora']},
    'Poland': {'capital': 'Warsaw', 'cities': ['Krakow', 'Lodz', 'Wroclaw']},
    'Austria': {'capital': 'Vienna', 'cities': ['Graz', 'Linz', 'Salzburg']},
    'Denmark': {'capital': 'Copenhagen', 'cities': ['Aarhus', 'Odense', 'Aalborg']},
    'Hungary': {'capital': 'Budapest', 'cities': ['Debrecen', 'Szeged', 'Miskolc']},
    'South Korea': {'capital': 'Seoul', 'cities': ['Busan', 'Incheon', 'Daegu']},
    'Chile': {'capital': 'Santiago', 'cities': ['Valparaíso', 'Concepción', 'La Serena']},
    'Peru': {'capital': 'Lima', 'cities': ['Arequipa', 'Trujillo', 'Chiclayo']},
    'Cuba': {'capital': 'Havana', 'cities': ['Santiago de Cuba', 'Camagüey', 'Holguín']},
    'Ukraine': {'capital': 'Kyiv', 'cities': ['Kharkiv', 'Odessa', 'Dnipro']},
    'Thailand': {'capital': 'Bangkok', 'cities': ['Chiang Mai', 'Pattaya', 'Phuket']},
    'Singapore': {'capital': 'Singapore', 'cities': ['Sentosa', 'Jurong East', 'Woodlands']},
    'Malaysia': {'capital': 'Kuala Lumpur', 'cities': ['George Town', 'Ipoh', 'Shah Alam']},
    'Philippines': {'capital': 'Manila', 'cities': ['Quezon City', 'Makati', 'Davao City']},
    'Saudi Arabia': {'capital': 'Riyadh', 'cities': ['Jeddah', 'Mecca', 'Medina']},
    'UAE': {'capital': 'Abu Dhabi', 'cities': ['Dubai', 'Sharjah', 'Ajman']},
    'Venezuela': {'capital': 'Caracas', 'cities': ['Maracaibo', 'Valencia', 'Barquisimeto']},
    'Colombia': {'capital': 'Bogotá', 'cities': ['Medellín', 'Cali', 'Barranquilla']},
    'Israel': {'capital': 'Jerusalem', 'cities': ['Tel Aviv', 'Haifa', 'Rishon LeZion']},
    'Indonesia': {'capital': 'Jakarta', 'cities': ['Surabaya', 'Bandung', 'Medan']},
    'Vietnam': {'capital': 'Hanoi', 'cities': ['Ho Chi Minh City', 'Da Nang', 'Can Tho']},
    'Pakistan': {'capital': 'Islamabad', 'cities': ['Karachi', 'Lahore', 'Faisalabad']},
    'Bangladesh': {'capital': 'Dhaka', 'cities': ['Chittagong', 'Khulna', 'Rajshahi']},
    'Sri Lanka': {'capital': 'Colombo', 'cities': ['Kandy', 'Galle', 'Jaffna']},
    'Nepal': {'capital': 'Kathmandu', 'cities': ['Pokhara', 'Lalitpur', 'Biratnagar']},
    'Kazakhstan': {'capital': 'Nur-Sultan', 'cities': ['Almaty', 'Shymkent', 'Karaganda']},
    'Uzbekistan': {'capital': 'Tashkent', 'cities': ['Samarkand', 'Bukhara', 'Namangan']},
    'Turkmenistan': {'capital': 'Ashgabat', 'cities': ['Turkmenabat', 'Dashoguz', 'Mary']},
    'Kyrgyzstan': {'capital': 'Bishkek', 'cities': ['Osh', 'Jalal-Abad', 'Karakol']},
    'Tajikistan': {'capital': 'Dushanbe', 'cities': ['Khujand', 'Kulob', 'Bokhtar']},
    'Bolivia': {'capital': 'Sucre', 'cities': ['La Paz', 'Santa Cruz', 'Cochabamba']},
    'Ecuador': {'capital': 'Quito', 'cities': ['Guayaquil', 'Cuenca', 'Santo Domingo']},
    'Uruguay': {'capital': 'Montevideo', 'cities': ['Salto', 'Paysandú', 'Las Piedras']},
    'Paraguay': {'capital': 'Asunción', 'cities': ['Ciudad del Este', 'San Lorenzo', 'Encarnación']},
    'Nicaragua': {'capital': 'Managua', 'cities': ['León', 'Granada', 'Estelí']},
    'Honduras': {'capital': 'Tegucigalpa', 'cities': ['San Pedro Sula', 'Choloma', 'La Ceiba']},
    'El Salvador': {'capital': 'San Salvador', 'cities': ['Santa Ana', 'Soyapango', 'San Miguel']},
    'Costa Rica': {'capital': 'San José', 'cities': ['Alajuela', 'Heredia', 'Cartago']},
    'Panama': {'capital': 'Panama City', 'cities': ['San Miguelito', 'Tocumen', 'David']},
    'Guatemala': {'capital': 'Guatemala City', 'cities': ['Mixco', 'Villa Nueva', 'Quetzaltenango']},
    'Jamaica': {'capital': 'Kingston', 'cities': ['Montego Bay', 'Spanish Town', 'Portmore']},
    'Trinidad and Tobago': {'capital': 'Port of Spain', 'cities': ['San Fernando', 'Chaguanas', 'Arima']},
    'Guyana': {'capital': 'Georgetown', 'cities': ['Linden', 'New Amsterdam', 'Bartica']},
    'Suriname': {'capital': 'Paramaribo', 'cities': ['Lelydorp', 'Nieuw Nickerie', 'Moengo']},
    'Barbados': {'capital': 'Bridgetown', 'cities': ['Speightstown', 'Oistins', 'Bathsheba']},
    'Grenada': {'capital': 'St. George’s', 'cities': ['Gouyave', 'Victoria', 'Sauteurs']},
    'St. Vincent and the Grenadines': {'capital': 'Kingstown', 'cities': ['Kingstown Park', 'Layou', 'Barrouallie']},
    'St. Lucia': {'capital': 'Castries', 'cities': ['Gros Islet', 'Vieux Fort', 'Micoud']},
    'Dominica': {'capital': 'Roseau', 'cities': ['Portsmouth', 'Marigot', 'Berekua']},
    'Antigua and Barbuda': {'capital': 'Saint John’s', 'cities': ['All Saints', 'Liberta', 'Potter’s Village']},
    'St. Kitts and Nevis': {'capital': 'Basseterre', 'cities': ['Figtree', 'Dieppe Bay Town', 'Monkey Hill']},
    'Dominican Republic': {'capital': 'Santo Domingo', 'cities': ['Santiago', 'Punta Cana', 'San Pedro de Macorís']},
    'Belize': {'capital': 'Belmopan', 'cities': ['Belize City', 'San Ignacio', 'Orange Walk']},
    'Haiti': {'capital': 'Port-au-Prince', 'cities': ['Cap-Haïtien', 'Delmas', 'Pétion-Ville']},
    'Fiji': {'capital': 'Suva', 'cities': ['Nadi', 'Lautoka', 'Labasa']},
    'Papua New Guinea': {'capital': 'Port Moresby', 'cities': ['Lae', 'Arawa', 'Mount Hagen']},
    'Vanuatu': {'capital': 'Port Vila', 'cities': ['Luganville', 'Norsup', 'Isangel']},
    'Solomon Islands': {'capital': 'Honiara', 'cities': ['Auki', 'Gizo', 'Buala']},
    'Samoa': {'capital': 'Apia', 'cities': ['Asau', 'Mulifanua', 'Faleula']},
    'Tonga': {'capital': 'Nukuʻalofa', 'cities': ['Neiafu', 'Haveluloto', 'Vaini']},
    'Kiribati': {'capital': 'Tarawa', 'cities': ['Betio Village', 'Bikenibeu Village', 'Teaoraereke Village']},
    'Micronesia': {'capital': 'Palikir', 'cities': ['Weno', 'Kitti', 'Kolonia']},
    'Marshall Islands': {'capital': 'Majuro', 'cities': ['Ebeye', 'Jabor', 'Wotje']},
    'Palau': {'capital': 'Ngerulmud', 'cities': ['Koror', 'Meyungs', 'Airai']},
    'Tuvalu': {'capital': 'Funafuti', 'cities': ['Savave Village', 'Tanrake Village', 'Asau']},
    'Nauru': {'capital': 'Yaren', 'cities': ['Meneng', 'Aiwo', 'Ijuw']},
    'Mongolia': {'capital': 'Ulaanbaatar', 'cities': ['Erdenet', 'Darkhan', 'Choibalsan']},
    'Niger': {'capital': 'Niamey', 'cities': ['Zinder', 'Maradi', 'Agadez']},
    'Mali': {'capital': 'Bamako', 'cities': ['Sikasso', 'Mopti', 'Koutiala']},
    'Mauritania': {'capital': 'Nouakchott', 'cities': ['Nouadhibou', 'Néma', 'Kaédi']},
    'Chad': {'capital': 'N’Djamena', 'cities': ['Moundou', 'Sarh', 'Abéché']},
    'Sudan': {'capital': 'Khartoum', 'cities': ['Omdurman', 'Nyala', 'Port Sudan']}
}


def get_easy_options(country):
    data = COUNTRIES_DATA[country]
    correct_capital = data['capital']
    wrong_cities = random.sample(data['cities'], 2)
    options = wrong_cities + [correct_capital]
    random.shuffle(options)
    return options

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/select_mode', methods=['POST'])
def select_mode():
    session['mode'] = request.form['mode']
    session['lives'] = 3
    session['score'] = 0
    session['unanswered_countries'] = list(COUNTRIES_DATA.keys())  # initialize the list with all countries
    return redirect(url_for('game'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'answer' in request.form:
        country = session['current_country']  # Get the current country from session
        correct_answer = COUNTRIES_DATA[country]['capital']
        
        if session['mode'] == 'hard':
            is_correct = request.form['answer'].strip().lower() == correct_answer.lower()
        else:
            is_correct = request.form['answer'] == correct_answer
        
        if is_correct:
            session['score'] += 1
            session['unanswered_countries'].remove(country)  # remove the country from the list if answered correctly
        else:
            session['lives'] -= 1

        if session['lives'] <= 0:
            return redirect(url_for('result'))
            
    if not session['unanswered_countries']:  # If the list is empty, reset it to contain all countries
        session['unanswered_countries'] = list(COUNTRIES_DATA.keys())

    country = random.choice(session['unanswered_countries'])  # pick a country from the unanswered list
    session['current_country'] = country

    if session['mode'] == 'hard':
        return render_template('game.html', country=country)
    else:
        options = get_easy_options(country)
        return render_template('game_easy.html', country=country, options=options)

@app.route('/result')
def result():
    score = session.get('score', 0)
    session.clear()
    return render_template('result.html', score=score)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

