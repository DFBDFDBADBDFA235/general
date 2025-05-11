import pandas as pd

# Carica i dati del book L2 (es. CSV esportato da piattaforma)
# Colonne richieste: timestamp, price, size, side ('bid' o 'ask'), event ('new', 'cancel', 'trade')
df = pd.read_csv("book_data.csv", parse_dates=["timestamp"])

# Parametri personalizzabili
MIN_SIZE = 50  # soglia per considerare un ordine "grande"
PRICE_LEVELS = 3  # profondità massima da considerare vicino al best bid/ask
MAX_LIFETIME_SEC = 2  # tempo massimo in cui l'ordine rimane prima di sparire

# Funzione per identificare eventi sospetti
def detect_layering(df):
    suspects = []

    for i in range(len(df) - 1):
        row = df.iloc[i]
        next_rows = df.iloc[i+1:i+20]  # cerca nelle prossime righe

        if row["event"] == "new" and row["size"] >= MIN_SIZE:
            # cerca se viene cancellato entro poco tempo, senza trade
            cancel_event = next_rows[
                (next_rows["price"] == row["price"]) &
                (next_rows["side"] == row["side"]) &
                (next_rows["event"] == "cancel") &
                ((next_rows["timestamp"] - row["timestamp"]).dt.total_seconds() <= MAX_LIFETIME_SEC)
            ]
            trade_event = next_rows[
                (next_rows["price"] == row["price"]) &
                (next_rows["side"] == row["side"]) &
                (next_rows["event"] == "trade")
            ]

            if not trade_event.empty:
                continue  # l’ordine è stato eseguito → non spoofing/layering

            if not cancel_event.empty:
                suspects.append({
                    "timestamp": row["timestamp"],
                    "price": row["price"],
                    "size": row["size"],
                    "side": row["side"],
                    "cancel_time": cancel_event.iloc[0]["timestamp"]
                })

    return pd.DataFrame(suspects)

# Applica la funzione
suspicious_orders = detect_layering(df)

# Mostra i risultati
print("Possibili casi di layering/spoofing rilevati:")
print(suspicious_orders)
