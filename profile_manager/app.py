from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import stripe

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Stripe configuration
stripe_keys = {
    'secret_key': 'your-secret-key',
    'publishable_key': 'your-publishable-key'
}
stripe.api_key = stripe_keys['secret_key']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        username = session['username']
        return render_template('profile.html', username=username)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/young-teen')
def young_teen():
    return render_template('young_teen.html')

@app.route('/young-professional')
def young_professional():
    return render_template('young_professional.html')

@app.route('/create-charge', methods=['POST'])
def create_charge():
    try:
        amount = 200  # amount in cents
        customer = stripe.Customer.create(
            email=request.form['stripeEmail'],
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Personalized Recommendations'
        )
        return render_template('results.html', amount=amount)
    except stripe.error.StripeError as e:
        return str(e), 403

@app.route('/charge')
def charge():
    return render_template('charge.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
