def validate_trade_params(trade_type, scrip_quantity, symbol, price_estimate):
    sync_holdings()
    sync_cash_balance()

    if trade_type not in {"BUY", "SELL"}:
        logging.error(f"Tipo di trade non valido: {trade_type}")
        return False

    if scrip_quantity <= 0 or not isinstance(scrip_quantity, int):
        logging.error(f"Quantità non valida: {scrip_quantity}")
        return False

    if not is_market_open():
        logging.warning("Mercato chiuso.")
        return False

    if trade_type == "BUY":
        estimated_cost = scrip_quantity * price_estimate * 1.01  # 1% margine per slippage/commissioni
        if estimated_cost > CASH_BALANCE:
            logging.error(f"Fondi insufficienti. Necessari: {estimated_cost}, Disponibili: {CASH_BALANCE}")
            return False

    elif trade_type == "SELL":
        holding_qty = get_holding_quantity(symbol)
        if scrip_quantity > holding_qty:
            logging.error("Tentativo di vendere più di quanto si possiede.")
            return False

    if is_duplicate_order(symbol, trade_type, scrip_quantity):
        logging.warning("Trade duplicato rilevato.")
        return False

    logging.info("Parametri di trade validati con successo.")
    return True
