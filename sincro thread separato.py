import threading

# Funzione per eseguire la sincronizzazione in un thread separato
def periodic_sync():
    while not shutdown_requested:
        sync_holdings()
        time.sleep(BALANCE_SYNC_INTERVAL)

# All'interno della funzione run_bot_for_ticker, avviare il thread di sincronizzazione
def run_bot_for_ticker(ccxt_ticker, trading_ticker, shutdown_file_path='shutdown.txt'):
    global shutdown_requested, last_candle_time
    currently_holding = False

    # Register the signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Avvia il thread di sincronizzazione
    sync_thread = threading.Thread(target=periodic_sync, daemon=True)
    sync_thread.start()

    while not shutdown_requested:
        try:
            # [Resto del codice del ciclo principale]
            # ...

            # Check for shutdown file
            if check_shutdown_file(shutdown_file_path):
                logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Shutdown file detected. Initiating shutdown...')
                shutdown_requested = True

        except Exception as e:
            logging.error(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Error in bot execution: {str(e)}")
            time.sleep(10)  # Wait before retrying to avoid hammering the API

    # Cleanup and exit
    logging.info(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - Bot has shut down safely.')

# Avvio del bot
try:
    run_bot_for_ticker(CCXT_TICKER_NAME, TRADING_TICKER_NAME)
except KeyboardInterrupt:
    logging.info("Bot stopped manually.")
