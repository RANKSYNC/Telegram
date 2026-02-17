import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن جدیدت رو اینجا بذار
TOKEN = "توکن جدیدت رو اینجا بذار"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات فعال است!\n\nدستورات:\n/btc - قیمت بیت‌کوین")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        price = float(r.json()['price'])
        await update.message.reply_text(f"💰 BTC/USDT: {price:,.2f}$")
    except:
        await update.message.reply_text("❌ خطا!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.run_polling()

if __name__ == "__main__":
    main()
