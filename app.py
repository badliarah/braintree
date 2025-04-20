from flask import Flask, render_template, request, jsonify
import braintree

app = Flask(__name__, template_folder="templates")

# Braintree Sandbox Configuration (replace with your own)
braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    merchant_id='qjs6htkwpwgn4qp5',
    public_key='d8wz2hzft3wdn9jr',
    private_key='01460cea5636e35e5986662a148137e5'
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/raw-check', methods=['POST'])
def raw_check():
    data = request.json
    number = data.get("number")
    month = data.get("exp_month")
    year = data.get("exp_year")
    cvv = data.get("cvv")
    amount = data.get("amount", "10.00")

    # Create payment method (via fake customer)
    result = braintree.PaymentMethod.create({
        "customer_id": "test_user_1",
        "payment_method_nonce": "fake-valid-nonce",  # we use a placeholder
        "credit_card": {
            "number": number,
            "expiration_month": month,
            "expiration_year": year,
            "cvv": cvv
        }
    })

    if result.is_success:
        token = result.payment_method.token

        txn = braintree.Transaction.sale({
            "amount": amount,
            "payment_method_token": token,
            "options": {"submit_for_settlement": True}
        })

        if txn.is_success:
            return jsonify({'success': True, 'transaction_id': txn.transaction.id})
        else:
            return jsonify({'success': False, 'message': txn.message})
    else:
        return jsonify({'success': False, 'message': result.message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
