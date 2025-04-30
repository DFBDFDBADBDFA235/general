def monitor_order(order_id, trading_ticker):
    """
    Monitora lo stato dell'ordine fino a quando non viene eseguito, annullato o scade il timeout.
    Restituisce lo stato finale dell'ordine: 'closed', 'canceled', 'open', o 'expired'.
    """
    global exchange
    start_time = time.time()
    logging.debug(f"Started monitoring order {order_id} for {trading_ticker}")
    while True:
        try:
            order = exchange.fetch_order(order_id, TRADING_TICKER_NAME)
            status = order['status']
            logging.debug(f"Monitoring order {order_id}: Current status: {status}")

            if status == 'closed':
                logging.debug(f"Order {order_id} has been closed.")
                return 'closed'
            elif status == 'canceled':
                logging.debug(f"Order {order_id} has been canceled.")
                return 'canceled'
            elif status in ['open', 'partial']:
                if time.time() - start_time > ORDER_TIMEOUT:
                    logging.warning(f"ORDER TIMEOUT: {order_id} for {trading_ticker} has not been filled within {ORDER_TIMEOUT} seconds.")
                    # Annulla l'ordine se non è stato eseguito entro il timeout
                    try:
                        exchange.cancel_order(order_id, TRADING_TICKER_NAME)
                        logging.info(f"ORDER CANCELED DUE TO TIMEOUT: {order_id} for {trading_ticker}")
                        return 'canceled'
                    except Exception as e:
                        logging.error(f"Error canceling order {order_id}: {str(e)}")
                        return 'expired'
                logging.debug(f"Order {order_id} still {status}. Retrying in {ORDER_CHECK_INTERVAL} seconds...")
                time.sleep(ORDER_CHECK_INTERVAL)
            else:
                logging.warning(f"Unknown status for order {order_id}: {status}")
                return status  # Restituisce lo stato se non è né 'open' né 'partial'
        except ccxt.NetworkError as ce:
            logging.error(f"Network error while monitoring order {order_id}: {str(ce)}")
        except ccxt.ExchangeError as ee:
            logging.error(f"Exchange error while monitoring order {order_id}: {str(ee)}")
        except Exception as e:
            logging.error(f"Unexpected error while monitoring order {order_id}: {str(e)}")
        
        # Attendi prima di ritentare
        time.sleep(ORDER_CHECK_INTERVAL)