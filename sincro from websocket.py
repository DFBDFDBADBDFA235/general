from binance import BinanceSocketManager
from binance.client import Client

# Inizializza il client di Binance
binance_client = Client(os.environ.get('BINANCE_API_KEY'), os.environ.get('BINANCE_SECRET'))

# Funzione per gestire gli aggiornamenti del bilancio
def handle_balance_update(msg):
    global HOLDING_QUANTITY
    try:
        if msg['e'] == 'outboundAccountPosition':
            asset = TRADING_TICKER_NAME.split('/')[0]  # 'BTC'
            real_holdings = float(msg['B'][0]['a'])  # Estrarre il bilancio dell'asset
            if real_holdings != HOLDING_QUANTITY:
                logging.info(f"WebSocket Sync: HOLDING_QUANTITY updated from {HOLDING_QUANTITY} to {real_holdings}")
                HOLDING_QUANTITY = real_holdings
    except Exception as e:
        logging.error(f"Error handling WebSocket message: {str(e)}")

# Funzione per avviare WebSocket
def start_websocket():
    bsm = BinanceSocketManager(binance_client)
    # Stream per gli aggiornamenti del bilancio
    ws = bsm.user_socket()
    bsm.start_user_socket(callback=handle_balance_update)
    bsm.start()

# Avvia WebSocket in un thread separato
sync_thread = threading.Thread(target=start_websocket, daemon=True)
sync_thread.start()
