import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json

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

WEBHOOK_URL = f"https://{RAILWAY_URL}/webhook"

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
        elif price < 10:
            return f"{price:.2f}"
        else:
            return f"{price:,.2f}"
    except:
        return price_str

# هندلر start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 به ربات قیمت ارز دیجیتال خوش اومدی!\n\n"
        "برای دیدن قیمت، اسم ارز رو با / بزن:\n"
        "/btc - بیت‌کوین\n"
        "/eth - اتریوم\n"
        "/ada - کاردانو\n"
        "/sol - سولانا\n"
        "/doge - دوج کوین"
    )

# هندلر help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 راهنما:\n"
        "از دستور /[اسم ارز] استفاده کن\n"
        "مثال: /btc, /eth, /ada"
    )

# هندلر ping
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 پونگ!")

# هندلر اصلی دستورات
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    if command in ["/", "/start", "/help", "/ping"]:
        return
    
    symbol = command[1:].strip().upper()
    
    if not symbol:
        await update.message.reply_text("❌ اسم ارز رو وارد کن")
        return
    
    msg = await update.message.reply_text(f"🔄 در حال دریافت {symbol}...")
    
    price, clean_symbol = get_price(symbol)
    
    if price:
        formatted = format_price(price)
        await msg.delete()
        await update.message.reply_text(f"💰 {clean_symbol}/USDT: {formatted}$")
    else:
        await msg.delete()
        await update.message.reply_text(f"❌ ارز {symbol} پیدا نشد!")

# سرور ساده برای Railway
class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot is running! Use POST for webhook.")
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        # اینجا می‌تونی درخواست‌های وب‌هوک رو پردازش کنی
        self.wfile.write(b"OK")
    
    def log_message(self, format, *args):
        return

def run_http_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    logger.info(f"HTTP Server running on port {port}")
    server.serve_forever()

def main():
    logger.info("🚀 راه‌اندازی ربات...")
    logger.info(f"📍 آدرس وب‌هوک: {WEBHOOK_URL}")
    
    # راه‌اندازی HTTP server در یک thread جداگانه
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # راه‌اندازی ربات تلگرام
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(MessageHandler(filters.COMMAND, handle_command))
    
    port = int(os.environ.get("PORT", 8080))
    
    logger.info("✅ ربات آماده است!")
    
    # ست کردن وب‌هوک
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="webhook",
        webhook_url=WEBHOOK_URL,
        secret_token=None,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
