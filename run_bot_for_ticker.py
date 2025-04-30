def run_bot_for_ticker(ccxt_ticker, trading_ticker, shutdown_file_path='shutdown.txt'):
    global shutdown_requested, last_candle_time
    currently_holding = False

    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not shutdown_requested:
        try:
            # STEP 1: FETCH THE DATA
            ticker_data = fetch_data(ccxt_ticker)
            if ticker_data is not None:
                # Extract the timestamp of the latest candle (this is the 'at' column in ticker_df)
                latest_candle_time = ticker_data.iloc[-1]['at']  # Last row in the DataFrame
                logging.debug(f"Latest candle time: {latest_candle_time}")

                # Check if a new candle has been generated
                if last_candle_time is None or latest_candle_time > last_candle_time:
                    # Log that a new candle is available
                    logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - New candle detected.')

                    # Update the last candle time
                    last_candle_time = latest_candle_time
                    logging.debug(f"Updated last_candle_time to: {last_candle_time}")

                    # Log the current price fetched from the ticker
                    current_price = ticker_data.iloc[-1]['close']  # Get the closing price of the latest candle
                    logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Ticker: {ccxt_ticker}, Current Price: {current_price}')
                    logging.debug(f"Current price for {ccxt_ticker}: {current_price}")

                    # STEP 2: COMPUTE TECHNICAL INDICATORS & APPLY THE TRADING STRATEGY
                    trade_rec_type = get_trade_recommendation(ticker_data)
                    logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - TRADING RECOMMENDATION: {trade_rec_type}')
                    logging.debug(f"Trade recommendation for {ccxt_ticker}: {trade_rec_type}")

                    # STEP 3: EXECUTE THE TRADE
                    if (trade_rec_type == 'BUY' and not currently_holding) or \
                       (trade_rec_type == 'SELL' and currently_holding):

                        logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Placing {trade_rec_type} order for {trading_ticker}')
                        logging.debug(f"Preparing to place {trade_rec_type} order for {trading_ticker}")

                        # Execute the trade
                        trade_successful = execute_trade(trade_rec_type, trading_ticker)

                        if trade_successful:
                            logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Trade {trade_rec_type} for {trading_ticker} successful.')
                            logging.debug(f"Trade successful. Currently holding: {currently_holding}")
                            currently_holding = not currently_holding
                        else:
                            logging.error(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Failed to execute {trade_rec_type} order for {trading_ticker}')
                            logging.debug(f"Trade failed for {trade_rec_type} order on {trading_ticker}")
                
                # No new candle, sleep for a shorter duration
                else:
                    logging.debug("No new candle detected. Sleeping for 10 seconds.")
                    time.sleep(10)  # Sleep for 10 seconds before checking again

            else:
                logging.warning(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Unable to fetch ticker data for {ccxt_ticker}. Retrying in 5 seconds.')
                logging.debug(f"Ticker data for {ccxt_ticker} is None. Sleeping for 5 seconds.")
                time.sleep(5)

            # Check for shutdown file
            if check_shutdown_file(shutdown_file_path):
                logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Shutdown file detected. Initiating shutdown...')
                logging.debug(f"Shutdown file {shutdown_file_path} detected.")
                shutdown_requested = True

        except Exception as e:
            logging.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Error in bot execution: {str(e)}")
            logging.debug("Exception details:", exc_info=True)
            time.sleep(10)  # Wait before retrying to avoid hammering the API

    # Avvio del bot
    if __name__ == "__main__":
        try:
            run_bot_for_ticker(CCXT_TICKER_NAME, TRADING_TICKER_NAME)
        except KeyboardInterrupt:
            logging.info("Bot stopped manually.")
            logging.debug("KeyboardInterrupt received. Exiting bot.")
