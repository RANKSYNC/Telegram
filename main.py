import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات
TOKEN = "8226915169:AAF4cAmZDUlR-PhDKMvI_MERxjA06W5zH3g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **ربات قیمت ارز**\n\n"
        "دستورات:\n"
        "/btc - قیمت بیت‌کوین\n"
        "/eth - قیمت اتریوم\n"
        "/ada - قیمت کاردانو"
    )

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin = update.message.text[1:].upper()
    
    # پیام انتظار
    msg = await update.message.reply_text(f"🔄 دریافت {coin}...")
    
    try:
        # درخواست به بایننس
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
        r = requests.get(url, timeout=5)
        
        if r.status_code == 200:
            price = float(r.json()['price'])
            
            # فرمت قیمت
            if price < 0.01:
                text = f"{price:.8f}"
            elif price < 1:
                text = f"{price:.4f}"
            else:
                text = f"{price:,.2f}"
            
            await msg.edit_text(f"💰 {coin}/USDT: {text}$")
        else:
            await msg.edit_text(f"❌ {coin} پیدا نشد!")
    except:
        await msg.edit_text("❌ خطا در دریافت قیمت")

def main():
    print("🚀 ربات شروع به کار کرد...")
    
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", price_handler))
    app.add_handler(CommandHandler("eth", price_handler))
    app.add_handler(CommandHandler("ada", price_handler))
    
    # شروع ربات
    app.run_polling()

if __name__ == "__main__":
    main()
