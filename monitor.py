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
# Questa riga legge il comando dal file YAML
FORCE_EMAIL = os.environ.get("FORCE_EMAIL", "false").lower() == "true"

def get_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find("main") or soup.find("article") or soup.find("body")
    return main.get_text(separator="\n", strip=True) if main else response.text

def send_email(url, test=False):
    subject = "🧪 TEST: Email Forzata" if test else "⚠️ Sapienza: Cambiamento Rilevato"
    msg = MIMEMultipart()
    msg["From"], msg["To"], msg["Subject"] = EMAIL_MITTENTE, EMAIL_DESTINATARIO, subject
    msg.attach(MIMEText(f"Link: {url}", "plain"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_MITTENTE, GMAIL_APP_PASSWORD)
        server.sendmail(EMAIL_MITTENTE, EMAIL_DESTINATARIO, msg.as_string())
    print("✅ Email inviata!")

def main():
    content = get_page_content(URL)
    current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    last_hash = open(HASH_FILE, "r").read().strip() if os.path.exists(HASH_FILE) else None

    # Se FORCE_EMAIL è true, invia l'email subito
    if FORCE_EMAIL:
        print("FORZATURA: Invio email di test...")
        send_email(URL, test=True)

    if last_hash is None or current_hash != last_hash:
        if last_hash is not None and not FORCE_EMAIL:
            send_email(URL)
        with open(HASH_FILE, "w") as f:
            f.write(current_hash)
        print("Hash aggiornato.")
    else:
        print("Nessun cambiamento.")

if __name__ == "__main__":
    main()
