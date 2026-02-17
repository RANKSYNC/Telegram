import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات - از محیط بگیر
TOKEN = os.environ.get("TOKEN", "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY")

# گرفتن قیمت از Binance
def get_price(symbol: str):
    pair = f"{symbol.upper()}USDT"
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if "price" in data:
            return data["price"]
    except:
        return None
    return None

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 به ربات قیمت ارز دیجیتال خوش اومدی!\n\n"
        "فقط کافیه اسم ارز رو با / بنویسی:\n"
        "/btc\n/eth\n/ada\n/sol\n/doge\nو ..."
    )

# هندلر همه دستورات
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    # اگه start بود، نادیده بگیر
    if command == "/start":
        return
    
    # استخراج اسم ارز
    symbol = command[1:].upper()
    
    # پیام در حال دریافت
    msg = await update.message.reply_text("🔄 لطفاً صبر کنید...")
    
    # گرفتن قیمت
    price = get_price(symbol)
    
    if price:
        # فرمت قیمت
        try:
            p = float(price)
            if p < 0.0001:
                formatted = f"{p:.8f}"
            elif p < 0.01:
                formatted = f"{p:.6f}"
            elif p < 1:
                formatted = f"{p:.4f}"
            else:
                formatted = f"{p:,.2f}"
        except:
            formatted = price
        
        await msg.edit_text(f"💰 {symbol}/USDT: {formatted}$")
    else:
        await msg.edit_text(f"❌ ارز {symbol} یافت نشد!")

def main():
    print("Starting bot...")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.COMMAND, handle_command))
    
    # راه‌اندازی بر اساس محیط
    port = int(os.environ.get("PORT", 8080))
    railway_url = os.environ.get("RAILWAY_STATIC_URL", "")
    
    if railway_url:
        # حالت وب‌هوک برای Railway
        webhook_url = f"https://{railway_url}/{TOKEN}"
        print(f"Webhook URL: {webhook_url}")
        print(f"Port: {port}")
        
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=webhook_url,
        )
    else:
        # حالت poll برای تست محلی
        print("Running in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
