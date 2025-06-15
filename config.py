YAHOO_FINANCE_BASE_URL = "https://finance.yahoo.com/quote/"

# Lista ATUALIZADA dos 30 tickers do Dow Jones Industrial Average
DOW_JONES_TICKERS = [
    "MMM",  # 3M
    "AXP",  # American Express
    "AAPL", # Apple
    "AMGN", # Amgen
    "BA",   # Boeing
    "CAT",  # Caterpillar
    "CVX",  # Chevron
    "CSCO", # Cisco
    "KO",   # Coca-Cola
    "DOW",  # Dow Inc.
    "DIS",  # Disney
    "GS",   # Goldman Sachs
    "HD",   # Home Depot
    "HON",  # Honeywell
    "IBM",  # IBM
    "INTC", # Intel
    "JNJ",  # Johnson & Johnson
    "JPM",  # JPMorgan Chase
    "MCD",  # McDonald's
    "MRK",  # Merck
    "MSFT", # Microsoft
    "NKE",  # Nike
    "PG",   # Procter & Gamble
    "CRM",  # Salesforce
    "SHW",  # Sherwin-Williams
    "TRV",  # Travelers
    "UNH",  # UnitedHealth Group
    "VZ",   # Verizon
    "V",    # Visa
    "WMT",  # Walmart
    "AMZN", # Amazon
    "NVDA"  # Nvidia
]


SELECTOR_OPEN_PRICE = 'fin-streamer[data-field="regularMarketOpen"]'
SELECTOR_VOLUME = 'fin-streamer[data-field="regularMarketVolume"]'
SELECTOR_PREVIOUS_CLOSE = 'fin-streamer[data-field="regularMarketPreviousClose"]'



# --- Configurações de E-mail ---
SENDER_EMAIL = "lucas.netgoncalves1810@gmail.com"  # <<< Substitua pelo seu email remetente 
SENDER_PASSWORD = "oszm yfxo ebjr tdbf" # <<< MUITO CUIDADO AQUI! Use uma senha de APP.
RECIPIENT_EMAIL = "lucasprog1810@gmail.com" # <<< Substitua pelo email para onde o relatório será enviado
EMAIL_SUBJECT = "Relatório Diário de Cotações - Dow Jones" # Assunto do e-mail
ALERT_EMAIL_SUBJECT = "ALERTA: Falha na Coleta de Dados Dow Jones"

# Configurações para Gmail:
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587 # Porta para TLS/STARTTLS

