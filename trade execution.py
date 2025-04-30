def execute_trade(trade_rec_type, trading_ticker):
    global exchange, HOLDING_QUANTITY, INVESTMENT_AMOUNT_PER_TRADE
    order_placed = False
    side_value = 'buy' if trade_rec_type == "BUY" else 'sell'
    
    try:
        # Fetch current ticker price
        ticker_request = exchange.fetch_ticker(trading_ticker)
        if ticker_request is not None:
            current_price = float(ticker_request['last'])  # Utilizza 'last' per il prezzo più recente
            logging.debug(f"Current price for {trading_ticker} is {current_price}")
    
            # Calculate the quantity for the order
            if trade_rec_type == "BUY":
                scrip_quantity = round(INVESTMENT_AMOUNT_PER_TRADE / current_price, 5)
                logging.debug(f"Calculated buy quantity: {scrip_quantity}")
            else:
                # Per gli ordini di vendita, usa la quantità posseduta
                scrip_quantity = HOLDING_QUANTITY
                logging.debug(f"Calculated sell quantity: {scrip_quantity}")
    
            # Ensure not selling more than held
            if trade_rec_type == "SELL":
                if scrip_quantity > HOLDING_QUANTITY:
                    logging.error("Attempting to sell more than held.")
                    return order_placed  # Exit without placing the order
                
                # Check for liquidity
                if not check_liquidity(trading_ticker, scrip_quantity):
                    logging.error("Insufficient funds to complete the sell order.")
                    return order_placed  # Exit without placing the order
    
            # Log the order details before placing it
            order_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            epoch_time = int(time.time() * 1000)
            logging.info(f"PLACING ORDER {order_time}: Ticker: {trading_ticker}, Side: {side_value}, "
                         f"Price: {current_price}, Quantity: {scrip_quantity}, Timestamp: {epoch_time}")
            
            # Place the order on the exchange
 order_response = exchange.create_limit_order(trading_ticker, side_value, scrip_quantity, current_price)
            
            # Log the response
            if order_response:
                order_id = order_response['id']
                logging.info(f'ORDER PLACED SUCCESSFULLY. RESPONSE: {order_response}')

                # Monitor the order status
                order_status = monitor_order(order_id, trading_ticker)

                if order_status == 'closed':
                    logging.info(f"ORDER EXECUTED: {trade_rec_type} {scrip_quantity} at {current_price} for {trading_ticker}")
                    
                    if trade_rec_type == "BUY":
                        HOLDING_QUANTITY += scrip_quantity  # Add the purchased quantity
                        logging.debug(f"HOLDING_QUANTITY updated after BUY: {HOLDING_QUANTITY}")
                    else:
                        HOLDING_QUANTITY -= scrip_quantity  # Subtract the sold quantity
                        logging.debug(f"HOLDING_QUANTITY updated after SELL: {HOLDING_QUANTITY}")

                    # Sincronizza immediatamente il bilancio dopo il trade
                    sync_holdings()

                    order_placed = True
                elif order_status == 'canceled':
                    logging.warning(f"ORDER CANCELED: {trade_rec_type} {scrip_quantity} at {current_price} for {trading_ticker}")
                else:
                    logging.warning(f"ORDER NOT FILLED: {trade_rec_type} {scrip_quantity} at {current_price} for {trading_ticker}")
            else:
                logging.error("Order response was empty or invalid.")
        else:
            logging.error(f"Failed to fetch ticker data for {trading_ticker}.")

    except Exception as e:
        logging.error(f"ALERT!!! UNABLE TO COMPLETE THE ORDER. ERROR: {str(e)}")
    
    return order_placed
