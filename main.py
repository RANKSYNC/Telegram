import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات شما
TOKEN = "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY"

# آدرس Webhook که از Railway یا پلتفرم شما به دست می‌آید
WEBHOOK_URL = "https://your-app-name.up.railway.app"  # جایگزین با آدرس واقعی اپ شما

# گرفتن قیمت از Binance REST API
def get_price(symbol: str):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}USDT"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        return data["price"]
    except:
        return None

# وقتی کاربر مثل "/btc" یا "/ada" بنویسه
async def coin_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.replace("/", "").upper()

    price = get_price(command)

    if price:
        await update.message.reply_text(f"{command}/USDT : {price}$")
    else:
        await update.message.reply_text("ارز پیدا نشد ❌")

def main():
    app = Application.builder().token(TOKEN).build()

    # هندل کردن درخواست های مختلف مانند /btc /ada /eth
    app.add_handler(CommandHandler(None, coin_price))

    port = int(os.environ.get("PORT", 8000))

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}",
    )

if __name__ == "__main__":
    main()
