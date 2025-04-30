from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Ricevuto alert:", data)

    # Esempio: estraggo parametri dal messaggio
    symbol = data.get("symbol")
    action = data.get("action")
    lot = data.get("lot")

    # Simula l'azione (qui potresti collegare IB, Binance, ecc.)
    print(f"Eseguo ordine: {action} {lot} {symbol}")

    return jsonify({"status": "ricevuto"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
