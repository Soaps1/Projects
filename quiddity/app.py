import stripe
from flask import Flask, request, render_template

app = Flask(__name__)

# Set your secret keys here
stripe.api_key = 'your-secret-key'  # Replace 'your-secret-key' with your Stripe secret key

# Define a simple function to determine recommendations based on age
def recommend_tasks(user_age):
    if user_age < 18:
        return ["Join a sports team", "Learn to play a musical instrument"]
    elif 18 <= user_age < 25:
        return ["Internship opportunities", "Start a small business"]
    elif 25 <= user_age < 30:
        return ["Investment basics", "Buying your first home"]
    else:
        return ["Career advancement courses", "Planning for retirement"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-charge', methods=['POST'])
def create_charge():
    # Token is created using Stripe Checkout or Elements!
    token = request.form['stripeToken']
    age = int(request.form.get('age', 0))

    # Attempt to charge the customer's card
    try:
        charge = stripe.Charge.create(
            amount=200,  # $2, charged in cents
            currency='usd',
            description='Example charge',
            source=token,
        )
        tasks = recommend_tasks(age)
        return render_template('results.html', age=age, tasks=tasks)
    except stripe.error.StripeError as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True)
