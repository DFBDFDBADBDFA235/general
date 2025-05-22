#google cloud non costa se lancio questo script che funziona ma vediDeprecationWarning Apre un Google Sheet, Crea un nuovo foglio, Scrive qualche riga così genera meno richieste API totali quindi puoi farlo 5000 volte al giorno senza pagare nulla.
#DeprecationWarning: The order of arguments in worksheet.update() has changed. Please pass values first and range_name secondor used named arguments (range_name=, values=)
Credential path: C:\repos\general\hip-watch-460612-c4-e0dd0a659b54.json
Dati scritti nel foglio 'Metalli interessanti' del Google Sheet con ID 1SpBWUH5bbF4WGbx2WV_ChrXr7ls3RQZnOoToJy-GWag.

import gspread
import os
from google.oauth2.service_account import Credentials

# === CONFIGURA QUI ===
SHEET_ID = "1SpBWUH5bbF4WGbx2WV_ChrXr7ls3RQZnOoToJy-GWag"  # L'ID è nella URL tra /d/ e /edit
NEW_SHEET_NAME = "Metalli interessanti"
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "hip-watch-460612-c4-e0dd0a659b54.json")

print("Credential path:", CREDENTIALS_PATH)


# === AUTENTICAZIONE ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
client = gspread.authorize(credentials)

# === APRE LA CARTELLA DI LAVORO ===
spreadsheet = client.open_by_key(SHEET_ID)

# === CREA UN NUOVO FOGLIO ===
try:
    worksheet = spreadsheet.add_worksheet(title=NEW_SHEET_NAME, rows="100", cols="10")
except gspread.exceptions.APIError:
    worksheet = spreadsheet.worksheet(NEW_SHEET_NAME)

# === TABELLA DA INSERIRE ===
data = [
    ["nome", "gruppo", "unità di misura", "note", "TBD", "TBO"],
    ["Litio", "Batterie", "tonnellate metriche", "Catodi/anodi batterie Li-ion; alta domanda, volatilità nei prezzi", "", ""],
    ["Cobalto", "Batterie", "tonnellate metriche", "Stabilizza il catodo; critico per l’approvvigionamento etico (RDC)", "", ""],
    ["Nickel", "Batterie", "tonnellate metriche", "Aumenta densità energetica; richiesto nelle batterie NMC, NCA", "", ""],
    ["Manganese", "Batterie", "tonnellate metriche", "Stabilità chimica; meno critico del cobalto", "", ""],
    ["Rame", "Batterie / Robotica / Microelettronica", "tonnellate metriche", "Conduttore chiave; uso trasversale; domanda crescente", "", ""],
    ["Alluminio", "Batterie / Robotica", "tonnellate metriche", "Leggero, resistente; collettori e strutture", "", ""],
    ["Grafite", "Batterie", "tonnellate metriche", "Anodo più comune; alternativa al silicio", "", ""],
    ["Silicio", "Batterie / Microelettronica", "tonnellate metriche", "Anodi ad alte prestazioni; semiconduttori; cruciale", "", ""],
    ["Fosforo", "Batterie", "tonnellate metriche", "Componente nelle batterie LFP; stabile ed economico", "", ""],
    ["Titanio", "Robotica", "tonnellate metriche", "Resistente, leggero; usato in telai e giunti", "", ""],
    ["Terre rare (Nd, Pr, Dy)", "Robotica / Elettronica", "kg", "Magneti permanenti; critici; concentrazione in Cina", "", ""],
    ["Oro", "Microelettronica", "kg", "Connessioni nei chip; costoso ma insostituibile", "", ""],
    ["Gallio", "Microelettronica", "kg", "Chip GaN e GaAs; strategico per telecomunicazioni", "", ""],
    ["Germanio", "Microelettronica", "kg", "Semiconduttori avanzati; alta mobilità elettronica", "", ""],
    ["Indio", "Microelettronica", "kg", "Display, LED, chip InP; raro", "", ""],
    ["Stagno", "Microelettronica", "tonnellate metriche", "Saldature senza piombo; uso in crescita", "", ""],
    ["Tantalio", "Microelettronica", "kg", "Condensatori ad alta capacità; essenziale per miniaturizzazione", "", ""],
]

# === SCRIVE LA TABELLA ===
worksheet.clear()
worksheet.update("A1", data)#correggere secondo #DeprecationWarning: The order of arguments in worksheet.update() has changed. Please pass values first and range_name secondor used named arguments (range_name=, values=)

print(f"Dati scritti nel foglio '{NEW_SHEET_NAME}' del Google Sheet con ID {SHEET_ID}.")
