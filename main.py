import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات شما
TOKEN = "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY"

# آدرس Webhook که از Railway به دست می‌آید
RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL", "https://your-app-name.up.railway.app")
WEBHOOK_URL = f"https://{RAILWAY_URL}" if RAILWAY_URL else "https://your-app-name.up.railway.app"

# لیست همه ارزهای معروف (می‌تونید بیشتر هم کنید)
CRYPTO_SYMBOLS = ["BTC", "ETH", "ADA", "BNB", "SOL", "XRP", "DOGE", "DOT", "LINK", "MATIC", "SHIB", "TRX", "AVAX", "UNI", "ATOM"]

# گرفتن قیمت از Binance REST API
def get_price(symbol: str):
    # حذف / از ابتدا و تبدیل به حروف بزرگ
    clean_symbol = symbol.replace("/", "").upper()
    
    # اگه با USDT تموم نشده بود، اضافه کن
    if not clean_symbol.endswith("USDT"):
        pair = f"{clean_symbol}USDT"
    else:
        pair = clean_symbol
    
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
        if "price" in data:
            return data["price"], clean_symbol
        return None, None
    except:
        return None, None

# وقتی کاربر /start بزنه
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به ربات قیمت ارز دیجیتال خوش اومدی 🚀\n\n"
        "برای دیدن قیمت هر ارز می‌تونی از دستورات زیر استفاده کنی:\n"
        "/btc - قیمت بیت‌کوین\n"
        "/eth - قیمت اتریوم\n"
        "/ada - قیمت کاردانو\n"
        "/help - راهنما\n\n"
        "یا هر ارز دیگه‌ای که می‌خوای با /[نماد ارز] امتحان کن"
    )

# راهنما
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbols_text = "\n".join([f"/{symbol.lower()} - {symbol}" for symbol in CRYPTO_SYMBOLS])
    await update.message.reply_text(
        f"ارزهای پشتیبانی شده:\n{symbols_text}\n\n"
        "یا می‌تونید هر ارز دیگه‌ای که توی بایننس هست رو با /[نماد ارز] امتحان کنید"
    )

# هندلر عمومی برای همه دستورات
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    # اگه فقط "/" بود یا دستور start/help بود، نادیده بگیر
    if command in ["/", "/start", "/help"]:
        return
    
    # استخراج اسم ارز از دستور (حذف /)
    symbol = command[1:].upper()
    
    price, clean_symbol = get_price(symbol)
    
    if price:
        # فرمت کردن عدد قیمت
        try:
            price_float = float(price)
            if price_float < 0.01:
                formatted_price = f"{price_float:.8f}"
            elif price_float < 1:
                formatted_price = f"{price_float:.4f}"
            else:
                formatted_price = f"{price_float:,.2f}"
        except:
            formatted_price = price
        
        await update.message.reply_text(f"💰 {clean_symbol}/USDT : {formatted_price}$")
    else:
        await update.message.reply_text(f"❌ ارز {symbol} پیدا نشد یا خطا در دریافت قیمت")

def main():
    app = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # این هندلر همه دستورات رو می‌گیره (هر چی که با / شروع بشه)
    app.add_handler(MessageHandler(filters.COMMAND, handle_command))

    port = int(os.environ.get("PORT", 8000))
    
    # برای Railway
    railway_url = os.environ.get("RAILWAY_URL", "")
    if railway_url:
        webhook_url = f"https://{railway_url}/{TOKEN}"
    else:
        webhook_url = f"{WEBHOOK_URL}/{TOKEN}"

    print(f"Starting webhook on port {port}")
    print(f"Webhook URL: {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    main()
