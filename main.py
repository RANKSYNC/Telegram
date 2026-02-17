import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات جدیدت رو اینجا بذار
TOKEN = "8226915169:AAH6F8009VATxbVNmgAm-78ft4xPCgACjdY"  # توکن جدید از BotFather

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 ربات قیمت بیت‌کوین\n\n"
        "فقط /btc رو بزن"
    )

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # ساده ترین درخواست به بایننس
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url)
        
        # چک کردن وضعیت
        if response.status_code == 200:
            data = response.json()
            price = float(data['price'])
            await update.message.reply_text(f"💰 بیت‌کوین: {price:,.2f}$")
        else:
            await update.message.reply_text(f"❌ خطا: {response.status_code}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")

def main():
    print("🚀 ربات در حال اجرا...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.run_polling()

if __name__ == "__main__":
    main()
