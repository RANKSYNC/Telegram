import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن جدید
TOKEN = "8226915169:AAHDOx1s4o2kQOh0u_9cUIz5q-zWrMEkv8Y"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 ربات فعال شد!\n\n"
        "💰 دستورات:\n"
        "/btc - قیمت بیت‌کوین\n"
        "/eth - قیمت اتریوم\n"
        "/ada - قیمت کاردانو"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        price = float(r.json()['price'])
        await update.message.reply_text(f"💰 BTC/USDT: {price:,.2f}$")
    except:
        await update.message.reply_text("❌ خطا")

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
        price = float(r.json()['price'])
        await update.message.reply_text(f"💰 ETH/USDT: {price:,.2f}$")
    except:
        await update.message.reply_text("❌ خطا")

async def ada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ADAUSDT")
        price = float(r.json()['price'])
        await update.message.reply_text(f"💰 ADA/USDT: {price:,.2f}$")
    except:
        await update.message.reply_text("❌ خطا")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("eth", eth))
    app.add_handler(CommandHandler("ada", ada))
    
    print("🚀 ربات در حال اجرا...")
    app.run_polling()

if __name__ == "__main__":
    main()
