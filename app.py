import braintree
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')

# Replace with your own Braintree sandbox credentials
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id='qjs6htkwpwgn4qp5',
    public_key='d8wz2hzft3wdn9jr',
    private_key='01460cea5636e35e5986662a148137e5'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/client_token')
def client_token():
    token = braintree.ClientToken.generate()
    return jsonify({'clientToken': token})

@app.route('/checkout', methods=['POST'])
def checkout():
    nonce = request.json.get('payment_method_nonce')
    amount = request.json.get('amount', '10.00')

    result = braintree.Transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return jsonify({'success': True, 'transaction_id': result.transaction.id})
    else:
        return jsonify({'success': False, 'message': result.message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
