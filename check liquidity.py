def check_liquidity(trading_ticker, scrip_quantity):
    """Controlla se ci sono sufficienti fondi per vendere."""
    try:
        # Sincronizza il bilancio prima di controllare la liquidità
        sync_holdings()
        asset = trading_ticker.split('/')[0]  # 'BTC' in questo caso
        available_balance = HOLDING_QUANTITY  # Poiché abbiamo sincronizzato
        return available_balance >= scrip_quantity
    except Exception as e:
        logging.error(f"Error fetching balance for liquidity check: {str(e)}")
        return False

def validate_trade_params(trade_rec_type, scrip_quantity):
    """Controlla se le condizioni per l'operazione sono valide."""
    # Sincronizza il bilancio prima di validare
    sync_holdings()
    if trade_rec_type == "SELL" and scrip_quantity > HOLDING_QUANTITY:
        logging.error("Tentativo di vendere più di quanto si possiede.")
        return False
    return True
