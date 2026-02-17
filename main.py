import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن ربات
TOKEN = os.environ.get("TOKEN", "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY")

# گرفتن قیمت از Binance
def get_price(symbol: str):
    try:
        clean_symbol = symbol.upper().strip()
        pair = f"{clean_symbol}USDT"
        
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if "price" in data:
                return data["price"], clean_symbol
    except Exception as e:
        logger.error(f"خطا: {e}")
    return None, None

# فرمت قیمت
def format_price(price_str: str) -> str:
    try:
        price = float(price_str)
        if price < 0.0001:
            return f"{price:.8f}"
        elif price < 0.01:
            return f"{price:.6f}"
        elif price < 1:
            return f"{price:.4f}"
        else:
            # جدا کردن هزارگان
            return f"{price:,.2f}"
    except:
        return price_str

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **ربات قیمت ارز دیجیتال**\n\n"
        "برای دیدن قیمت، از دستور زیر استفاده کن:\n"
        "`/[اسم ارز]`\n\n"
        "**مثال:**\n"
        "`/btc` - قیمت بیت‌کوین\n"
        "`/eth` - قیمت اتریوم\n"
        "`/ada` - قیمت کاردانو\n"
        "`/sol` - قیمت سولانا\n"
        "`/doge` - قیمت دوج کوین",
        parse_mode='Markdown'
    )

# هندلر اصلی دستورات
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text
    
    # اگه start بود، نادیده بگیر
    if command == "/start":
        return
    
    # استخراج اسم ارز
    symbol = command[1:].strip().upper()
    
    if not symbol:
        await update.message.reply_text("❌ لطفاً اسم ارز رو وارد کن. مثال: /btc")
        return
    
    # پیام انتظار
    wait_message = await update.message.reply_text(f"🔄 در حال دریافت قیمت {symbol}...")
    
    # دریافت قیمت
    price, clean_symbol = get_price(symbol)
    
    if price:
        formatted_price = format_price(price)
        await wait_message.delete()
        await update.message.reply_text(
            f"💰 **{clean_symbol}/USDT**\n"
            f"قیمت: `{formatted_price}$`",
            parse_mode='Markdown'
        )
        logger.info(f"قیمت {clean_symbol}: {formatted_price}$")
    else:
        await wait_message.delete()
        await update.message.reply_text(
            f"❌ ارز `{symbol}` پیدا نشد!\n"
            "از درستی اسم ارز مطمئن شو.",
            parse_mode='Markdown'
        )

def main():
    logger.info("🚀 راه‌اندازی ربات...")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.COMMAND, handle_command))
    
    # راه‌اندازی با Polling (ساده‌ترین روش)
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"📡 پورت: {port}")
    logger.info("✅ ربات آماده است!")
    
    # شروع ربات با polling
    app.run_polling()

if __name__ == "__main__":
    main()
