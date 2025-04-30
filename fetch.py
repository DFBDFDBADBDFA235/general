def fetch_data(ticker):
    global exchange
    ticker_df = None
    try:
        logging.debug(f"Attempting to fetch OHLCV data for {ticker}")
        # Fetch OHLCV data
        bars = exchange.fetch_ohlcv(ticker, timeframe=f'{CANDLE_DURATION_IN_MIN}m', limit=100)
        logging.debug(f"Fetched {len(bars)} bars for {ticker}")

        # Verifica se nessun dato è stato ricevuto
        if not bars:
            raise ValueError(f"No data fetched for ticker {ticker}")

        # Crea DataFrame dai dati
        ticker_df = pd.DataFrame(bars[:-1], columns=['at', 'open', 'high', 'low', 'close', 'vol'])
        ticker_df['Date'] = pd.to_datetime(ticker_df['at'], unit='ms')
        ticker_df['symbol'] = ticker

        logging.debug(f"Created DataFrame with {len(ticker_df)} rows for {ticker}")

        # Controllo se il DataFrame è vuoto
        if ticker_df.empty:
            raise ValueError(f"Received empty DataFrame for ticker {ticker}")

        # Controllo valori NaN nel DataFrame
        if ticker_df.isna().any().any():  # Se esistono NaN in qualsiasi colonna
            logging.warning(f"Missing data detected in DataFrame for {ticker}")

            # Opzioni di gestione dei dati mancanti
            ticker_df = ticker_df.dropna()  # Rimuove le righe con NaN
            logging.debug(f"Dropped rows with NaN. DataFrame now has {len(ticker_df)} rows.")

    except ccxt.NetworkError as ce:
        logging.error(f"Connection error while fetching data for {ticker}: {str(ce)}")
    except ccxt.ExchangeError as ee:
        logging.error(f"Exchange error while fetching data for {ticker}: {str(ee)}")
    except TimeoutError as te:
        logging.error(f"Timeout error while fetching data for {ticker}: {str(te)}")
    except ValueError as ve:
        logging.error(f"Value error while processing data for {ticker}: {str(ve)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching data for {ticker}: {str(e)}")

    return ticker_df
