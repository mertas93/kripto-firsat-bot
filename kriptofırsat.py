import requests
import time
from telegram import Bot
import random

# Telegram botu ayarla
bot_token = "8036527191:AAEGeUZHDb4AMLICFGmGl6OdrN4hrSaUpoQ"
chat_id = "1119272011"
bot = Bot(token=bot_token)

def rsi_dummy(price_list):
    return random.randint(20, 80)  # rastgele RSI

def macd_dummy():
    return random.choice(["yukarı", "aşağı", "belirsiz"])  # dummy MACD

print("İlk 250 coin taranıyor…")
total_count = 0
fırsat_count = 0
page = 1
max_pages = 1  # yalnızca ilk 250 coin
fırsatlar = []

while True:
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=volume_desc&per_page=250&page={page}&price_change_percentage=1h"
    response = requests.get(url)
    try:
        data = response.json()
    except ValueError:
        print("JSON parse hatası, boş veri veya yanlış format.")
        break

    if not isinstance(data, list):
        print(f"Beklenmeyen yanıt: {data}")
        break

    if not data:
        break

    for coin in data:
        total_count += 1
        symbol = coin.get('symbol', '').upper()
        price = float(coin.get('current_price', 0))
        change_1h = coin.get('price_change_percentage_1h_in_currency') or 0
        volume = coin.get('total_volume', 0)

        rsi = rsi_dummy([])
        macd = macd_dummy()

        print(f"{symbol} — RSI: {rsi}, 1h: {change_1h}%, MACD: {macd}, Hacim: {volume}")

        if (rsi < 25 or change_1h > 2 or change_1h < -3) and macd == "yukarı" and volume > 1_000_000:
            fırsat_count += 1
            fırsatlar.append(
                f"🎯 {symbol}\nFiyat: {price}$\n1h Değişim: {change_1h}%\nHacim: {volume}\nRSI: {rsi}\nMACD: {macd}"
            )

    page += 1
    time.sleep(1)

    if page > max_pages:
        break

if fırsatlar:
    print(f"Bildirim gönderiliyor. {len(fırsatlar)} fırsat bulundu.")
    mesaj = "📈 Ciddi Fırsat Coinler (MACD yukarı, hacim güçlü):\n\n"
    mesaj += "\n\n".join(fırsatlar[:10])  # en fazla 10 tane gönder
    try:
        bot.send_message(chat_id=chat_id, text=mesaj)
        print("Bildirim gönderildi.")
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")

print(f"İlk 250 coin tarandı. Toplam: {total_count} coin. Fırsat: {fırsat_count} coin.")
