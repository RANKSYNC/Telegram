import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import threading

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن ربات
TOKEN = os.environ.get("TOKEN", "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY")

# آدرس ربات
RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL", "ranksync-bot-production-b3b7.up.railway.app")
if RAILWAY_URL.startswith("https://"):
    RAILWAY_URL = RAILWAY_URL.replace("https://", "")
if RAILWAY_URL.startswith("http://"):
    RAILWAY_URL = RAILWAY_URL.replace("http://", "")

# ایجاد Flask app
flask_app = Flask(__name__)
bot_app = None

# گرفتن قیمت از Binance
def get_price(symbol: str):
    try:
        clean_symbol = symbol.upper().strip()
        if not clean_symbol.endswith("USDT"):
            pair = f"{clean_symbol}USDT"
        else:
            pair = clean_symbol
            clean_symbol = clean_symbol.replace("USDT", "")
        
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if "price" in data:
                return data["price"], clean_symbol
    except Exception as e:
        logger.error(f"خطا در دریافت قیمت: {e}")
    return None, None

# فرمت قیمت
def format_price(price_str: str) -> str:
    try:
        price = float(price_str)
        if price < 0.00000001:
            return f"{price:.12f}"
        elif price < 0.0001:
            return f"{price:.8f}"
        elif price < 0.001:
            return f"{price:.6f}"
        elif price < 0.01:
            return f"{price:.4f}"
        elif price < 1:
            return f"{price:.3f}"
        else:
            return f"{price:,.2f}"
    except:
        return price_str

# هندلر start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 به ربات قیمت ارز دیجیتال خوش اومدی!\n\n"
        "فقط کافیه اسم ارز رو با / بنویسی:\n"
        "/btc - بیت‌کوین\n"
        "/eth - اتریوم\n"
        "/ada - کاردانو\n"
        "/sol - سولانا\n"
        "/doge - دوج کوین\n\n"
        "مثال: /btc"
    )

# هندلر اصلی
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    if command == "/start":
        return
    
    symbol = command[1:].strip().upper()
    
    if not symbol:
        await update.message.reply_text("❌ لطفاً اسم ارز رو وارد کن. مثال: /btc")
        return
    
    msg = await update.message.reply_text(f"🔄 در حال دریافت قیمت {symbol}...")
    
    price, clean_symbol = get_price(symbol)
    
    if price:
        formatted = format_price(price)
        await msg.delete()
        await update.message.reply_text(f"💰 {clean_symbol}/USDT: {formatted}$")
    else:
        await msg.delete()
        await update.message.reply_text(f"❌ ارز {symbol} پیدا نشد!")

# مسیر اصلی برای چک کردن
@flask_app.route('/')
def home():
    return "ربات فعال است! 🚀"

# مسیر وب‌هوک
@flask_app.route('/webhook', methods=['POST'])
def webhook():
    if bot_app:
        # پردازش آپدیت
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        bot_app.process_update(update)
    return "OK", 200

@flask_app.route('/webhook', methods=['GET'])
def webhook_get():
    return "وب‌هوک فعال است. از متد POST استفاده کنید."

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def main():
    global bot_app
    logger.info("🚀 راه‌اندازی ربات...")
    
    # ساخت اپلیکیشن تلگرام
    bot_app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.COMMAND, handle_command))
    
    # راه‌اندازی Flask در یک thread جداگانه
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # آدرس وب‌هوک
    webhook_url = f"https://{RAILWAY_URL}/webhook"
    logger.info(f"📍 آدرس وب‌هوک: {webhook_url}")
    
    # ست کردن وب‌هوک
    bot_app.bot.set_webhook(url=webhook_url)
    logger.info("✅ وب‌هوک ست شد")
    
    # نگه داشتن برنامه
    logger.info("✅ ربات آماده است!")
    
    try:
        # اینجا منتظر می‌مونیم
        import time
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        logger.info("خروج از برنامه...")

if __name__ == "__main__":
    main()
