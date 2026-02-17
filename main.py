import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن جدید
TOKEN = "8226915169:AAF4cAmZDUlR-PhDKMvI_MERxjA06W5zH3g"

# دریافت قیمت از بایننس
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return float(data['price'])
    except:
        return None
    return None

# فرمت قیمت
def format_price(price):
    if price < 0.00001:
        return f"{price:.10f}"
    elif price < 0.0001:
        return f"{price:.8f}"
    elif price < 0.001:
        return f"{price:.6f}"
    elif price < 0.01:
        return f"{price:.5f}"
    elif price < 0.1:
        return f"{price:.4f}"
    elif price < 1:
        return f"{price:.3f}"
    else:
        return f"{price:,.2f}"

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **ربات قیمت ارز دیجیتال**\n\n"
        "💰 **ارزهای قابل پشتیبانی:**\n"
        "بیت‌کوین `/btc`\n"
        "اتریوم `/eth`\n"
        "کاردانو `/ada`\n"
        "سولانا `/sol`\n"
        "دوج کوین `/doge`\n"
        "ریپل `/xrp`\n"
        "پولکادات `/dot`\n"
        "و هر ارز دیگه‌ای که توی Binance باشه!\n\n"
        "✨ **مثال:** `/btc`",
        parse_mode='Markdown'
    )

# هندلر قیمت
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # گرفتن اسم ارز
    coin = update.message.text[1:].upper()
    
    # پیام انتظار
    msg = await update.message.reply_text(f"🔄 در حال دریافت {coin}...")
    
    # گرفتن قیمت
    price = get_price(coin)
    
    if price:
        formatted = format_price(price)
        await msg.edit_text(f"💰 **{coin}/USDT**: `{formatted}$`", parse_mode='Markdown')
        logger.info(f"{coin}: {formatted}$")
    else:
        await msg.edit_text(f"❌ ارز `{coin}` پیدا نشد!\nاز `/start` برای دیدن لیست ارزها استفاده کن.", parse_mode='Markdown')

def main():
    logger.info("🚀 راه‌اندازی ربات با توکن جدید...")
    
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.COMMAND, price_command))
    
    logger.info("✅ ربات آماده است!")
    
    # شروع ربات
    app.run_polling()

if __name__ == "__main__":
    main()
