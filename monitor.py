import requests
import hashlib
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

if not os.path.exists("hashes"):
    os.mkdir("hashes")

with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    try:
        response = requests.get(url, timeout=15)
        current_hash = get_hash(response.text)

        filename = "hashes/" + get_hash(url) + ".txt"

        if os.path.exists(filename):
            with open(filename, "r") as f:
                old_hash = f.read()

            if old_hash != current_hash:
                send_telegram(f"🔔 La pagina è cambiata:\n{url}")
        else:
            send_telegram(f"✅ Monitoraggio attivato:\n{url}")

        with open(filename, "w") as f:
            f.write(current_hash)

    except Exception:
        send_telegram(f"⚠️ Errore nel controllo:\n{url}")
