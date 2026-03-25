import hashlib
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup

URL = "https://www.uniroma1.it/it/node/40540"
HASH_FILE = "last_hash.txt"

EMAIL_MITTENTE = os.environ["EMAIL_MITTENTE"]
EMAIL_DESTINATARIO = os.environ["EMAIL_DESTINATARIO"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
FORCE_EMAIL = os.environ.get("FORCE_EMAIL", "false").lower() == "true"

def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=30)
    content = response.text # Per sicurezza prendiamo tutto il testo
    current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    
    last_hash = None
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            last_hash = f.read().strip()

    if FORCE_EMAIL:
        print("FORZATURA: Invio email di test...")
        send_email(URL)

    if last_hash is None or current_hash != last_hash:
        if last_hash is not None and not FORCE_EMAIL:
            send_email(URL)
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
        print("Stato aggiornato.")
    else:
        print("Nessun cambiamento.")

def send_email(url):
    msg = MIMEMultipart()
    msg["From"], msg["To"], msg["Subject"] = EMAIL_MITTENTE, EMAIL_DESTINATARIO, "Monitor Sapienza"
    msg.attach(MIMEText(f"Novità qui: {url}", "plain"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(EMAIL_MITTENTE, GMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_MITTENTE, EMAIL_DESTINATARIO, msg.as_string())
    print("✅ Email inviata!")

if __name__ == "__main__":
    main()
