def sync_holdings():
    global HOLDING_QUANTITY
    try:
        logging.debug("Starting synchronization of HOLDING_QUANTITY with actual balance.")
        balance = exchange.fetch_balance()
        asset = TRADING_TICKER_NAME.split('/')[0]  # 'BTC' in questo caso
        real_holdings = balance['total'].get(asset, 0)
        logging.debug(f"Real holdings fetched: {real_holdings}")
        if real_holdings != HOLDING_QUANTITY:
            logging.info(f"Sincronizzazione HOLDING_QUANTITY: {HOLDING_QUANTITY} -> {real_holdings}")
            HOLDING_QUANTITY = real_holdings
            logging.debug(f"HOLDING_QUANTITY updated to: {HOLDING_QUANTITY}")
        else:
            logging.debug("HOLDING_QUANTITY is already synchronized.")
    except Exception as e:
        logging.error(f"Error during holdings synchronization: {str(e)}")
