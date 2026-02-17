import json
from urllib.request import urlopen
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن جدید
TOKEN = "8226915169:AAHDOx1s4o2kQOh0u_9cUIz5q-zWrMEkv8Y"

def get_binance_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        response = urlopen(url, timeout=5)
        data = json.loads(response.read())
        return float(data['price'])
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ربات فعال شد!\n\n"
        "دستورات:\n"
        "/btc - بیت‌کوین\n"
        "/eth - اتریوم\n"
        "/doge - دوج کوین"
    )

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = update.message.text[1:].upper()
    
    msg = await update.message.reply_text(f"🔄 دریافت {coin}...")
    
    price = get_binance_price(coin)
    
    if price:
        if price < 1:
            text = f"{price:.4f}"
        else:
            text = f"{price:,.2f}"
        await msg.edit_text(f"💰 {coin}/USDT: {text}$")
    else:
        await msg.edit_text(f"❌ خطا در دریافت {coin}")

def main():
    print("🚀 ربات شروع به کار کرد...")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", price_handler))
    app.add_handler(CommandHandler("eth", price_handler))
    app.add_handler(CommandHandler("doge", price_handler))
    
    app.run_polling()

if __name__ == "__main__":
    main()
