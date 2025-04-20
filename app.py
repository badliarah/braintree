import braintree
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Replace these with your Braintree sandbox credentials
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id='qjs6htkwpwgn4qp5',
    public_key='d8wz2hzft3wdn9jr',
    private_key='01460cea5636e35e5986662a148137e5'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/client_token', methods=['GET'])
def client_token():
    token = braintree.ClientToken.generate()
    return jsonify({'clientToken': token})

@app.route('/checkout', methods=['POST'])
def create_transaction():
    nonce = request.json.get("payment_method_nonce")
    amount = request.json.get("amount")

    result = braintree.Transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return jsonify({"success": True, "transaction_id": result.transaction.id})
    else:
        return jsonify({"success": False, "message": str(result.message)}), 400

if __name__ == '__main__':
    app.run(debug=True)