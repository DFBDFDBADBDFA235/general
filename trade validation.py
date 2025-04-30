def validate_trade_params(trade_rec_type, scrip_quantity):
    """Controlla se le condizioni per l'operazione sono valide."""
    # Sincronizza il bilancio prima di validare
    sync_holdings()
    logging.debug(f"Validating trade parameters: Type={trade_rec_type}, Quantity={scrip_quantity}, HOLDING_QUANTITY={HOLDING_QUANTITY}")
    if trade_rec_type == "SELL" and scrip_quantity > HOLDING_QUANTITY:
        logging.error("Tentativo di vendere più di quanto si possiede.")
        return False
    return True
