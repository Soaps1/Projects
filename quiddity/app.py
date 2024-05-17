from flask import Flask, render_template, request, redirect, url_for, jsonify
import stripe

app = Flask(__name__)

# Stripe configuration
stripe_keys = {
    'secret_key': 'your-secret-key',
    'publishable_key': 'your-publishable-key'
}
stripe.api_key = stripe_keys['secret_key']

@app.route('/')
def index():
    return render_template('index.html', key=stripe_keys['publishable_key'])

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
    app.run(debug=True)
