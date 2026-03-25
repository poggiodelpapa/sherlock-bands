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

# Nome carino da mostrare come mittente
SENDER_NAME = "Monitor Sapienza"   # ← puoi cambiarlo come vuoi (es. "Avvisi Sapienza", "Bot Graduatorie", ecc.)

def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    # Estraiamo solo il contenuto principale
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("div", class_="node__content")
    content_to_hash = str(main_content) if main_content else response.text

    current_hash = hashlib.sha256(content_to_hash.encode("utf-8")).hexdigest()
    
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
        print("✅ Hash aggiornato.")
    else:
        print("Nessun cambiamento rilevato.")

def send_email(url):
    msg = MIMEMultipart()
    # Qui impostiamo il nome carino
    msg["From"] = f"{SENDER_NAME} <{EMAIL_MITTENTE}>"
    msg["To"] = EMAIL_DESTINATARIO
    msg["Subject"] = "🔔 Monitor Sapienza - Novità rilevata!"
    
    body = f"È cambiato il contenuto della pagina:\n\n{url}\n\nControlla subito!"
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(EMAIL_MITTENTE, GMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_MITTENTE, EMAIL_DESTINATARIO, msg.as_string())
    
    print("✅ Email inviata!")

if __name__ == "__main__":
    main()
