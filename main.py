import os
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیم لاگ برای پیدا کردن خطاها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن ربات - از متغیر محیطی می‌گیره
TOKEN = os.environ.get("TOKEN", "8226915169:AAGmGCTWVbRHcseOXawfTp7AfSgluaHSqYY")

# آدرس ربات در Railway
RAILWAY_URL = os.environ.get("RAILWAY_STATIC_URL", "ranksync-bot-production-b3b7.up.railway.app")
if RAILWAY_URL.startswith("https://"):
    RAILWAY_URL = RAILWAY_URL.replace("https://", "")
if RAILWAY_URL.startswith("http://"):
    RAILWAY_URL = RAILWAY_URL.replace("http://", "")

WEBHOOK_URL = f"https://{RAILWAY_URL}/webhook"

# گرفتن قیمت از Binance
def get_price(symbol: str):
    """دریافت قیمت از Binance"""
    # پاکسازی نماد
    clean_symbol = symbol.upper().strip()
    
    # اگه با USDT تموم نشده، اضافه کن
    if not clean_symbol.endswith("USDT"):
        pair = f"{clean_symbol}USDT"
    else:
        pair = clean_symbol
        clean_symbol = clean_symbol.replace("USDT", "")
    
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={pair}"
    
    try:
        logger.info(f"دریافت قیمت برای {pair}...")
        r = requests.get(url, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            if "price" in data:
                return data["price"], clean_symbol
            else:
                logger.error(f"پاسخ بدون قیمت: {data}")
                return None, None
        else:
            logger.error(f"خطا در دریافت: {r.status_code}")
            return None, None
            
    except requests.exceptions.Timeout:
        logger.error("Timeout در دریافت اطلاعات")
        return None, None
    except requests.exceptions.ConnectionError:
        logger.error("مشکل اتصال به Binance")
        return None, None
    except Exception as e:
        logger.error(f"خطای غیرمنتظره: {str(e)}")
        return None, None

# فرمت کردن قیمت
def format_price(price_str: str) -> str:
    """فرمت کردن قیمت برای نمایش بهتر"""
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
            # جدا کردن هزارگان
            return f"{price:,.2f}"
    except:
        return price_str

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیام خوش‌آمدگویی"""
    user = update.effective_user
    welcome_message = (
        f"🚀 سلام {user.first_name}!\n\n"
        "به ربات قیمت ارز دیجیتال خوش اومدی!\n\n"
        "💰 **چطور کار می‌کنه؟**\n"
        "فقط کافیه اسم ارز رو با / بنویسی:\n\n"
        "🔹 `/btc` - قیمت بیت‌کوین\n"
        "🔹 `/eth` - قیمت اتریوم\n"
        "🔹 `/ada` - قیمت کاردانو\n"
        "🔹 `/sol` - قیمت سولانا\n"
        "🔹 `/doge` - قیمت دوج کوین\n"
        "🔹 `/xrp` - قیمت ریپل\n\n"
        "✨ هر ارز دیگه‌ای که توی Binance هست رو هم می‌تونی امتحان کنی!\n\n"
        "📊 قیمت‌ها به صورت لحظه‌ای از Binance دریافت میشن."
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

# هندلر اصلی برای همه دستورات
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش دستورات ارز"""
    command = update.message.text
    
    # اگه فقط / بود یا start بود، نادیده بگیر
    if command in ["/", "/start"]:
        return
    
    # استخراج اسم ارز
    symbol = command[1:].strip().upper()
    
    if not symbol:
        await update.message.reply_text("❌ لطفاً اسم ارز رو وارد کن. مثال: /btc")
        return
    
    # پیام انتظار
    wait_message = await update.message.reply_text(f"🔄 در حال دریافت قیمت {symbol}...")
    
    try:
        # دریافت قیمت
        price, clean_symbol = get_price(symbol)
        
        if price:
            formatted_price = format_price(price)
            
            # حذف پیام انتظار
            await wait_message.delete()
            
            # ارسال قیمت
            result_message = (
                f"💰 **{clean_symbol}/USDT**\n\n"
                f"قیمت: `{formatted_price}$`\n"
                f"📊 منبع: Binance\n"
                f"⏱ {update.message.date.strftime('%H:%M:%S')}"
            )
            await update.message.reply_text(result_message, parse_mode='Markdown')
            
            # لاگ برای دیباگ
            logger.info(f"قیمت {clean_symbol}: {formatted_price}$")
            
        else:
            # حذف پیام انتظار
            await wait_message.delete()
            
            # ارسال پیام خطا
            error_message = (
                f"❌ **خطا در دریافت قیمت**\n\n"
                f"ارز `{symbol}` پیدا نشد!\n\n"
                f"📝 نکات:\n"
                f"• از درستی اسم ارز مطمئن شو\n"
                f"• مثال: /btc, /eth, /ada\n"
                f"• بعضی ارزها ممکنه توی Binance نباشن"
            )
            await update.message.reply_text(error_message, parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"خطا در پردازش دستور {command}: {str(e)}")
        await wait_message.delete()
        await update.message.reply_text("❌ خطایی رخ داد. لطفاً دوباره تلاش کن.")

# دستور help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنما"""
    help_text = (
        "📚 **راهنمای استفاده**\n\n"
        "برای دیدن قیمت هر ارز، از دستور زیر استفاده کن:\n"
        "`/[اسم ارز]`\n\n"
        "**مثال‌ها:**\n"
        "🔸 `/btc` - بیت‌کوین\n"
        "🔸 `/eth` - اتریوم\n"
        "🔸 `/ada` - کاردانو\n"
        "🔸 `/sol` - سولانا\n"
        "🔸 `/doge` - دوج کوین\n"
        "🔸 `/xrp` - ریپل\n"
        "🔸 `/dot` - پولکادات\n"
        "🔸 `/link` - چین لینک\n"
        "🔸 `/matic` - پالیگان\n\n"
        "✨ **نکته:** هر ارز دیگه‌ای که توی Binance باشه رو هم می‌تونی امتحان کنی!\n\n"
        "💡 اگه ارزی پیدا نشد، با املای دیگه امتحان کن."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# دستور برای تست اتصال
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تست اتصال ربات"""
    await update.message.reply_text("🏓 پونگ! ربات فعال است.")

def main():
    """تابع اصلی"""
    logger.info("🚀 راه‌اندازی ربات...")
    logger.info(f"📍 آدرس وب‌هوک: {WEBHOOK_URL}")
    
    try:
        # ساخت اپلیکیشن
        app = Application.builder().token(TOKEN).build()
        
        # اضافه کردن هندلرها
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("ping", ping_command))
        
        # این هندلر همه دستورات رو می‌گیره (باید آخر از همه باشه)
        app.add_handler(MessageHandler(filters.COMMAND, handle_command))
        
        # دریافت پورت از محیط
        port = int(os.environ.get("PORT", 8080))
        
        logger.info(f"📡 پورت: {port}")
        logger.info("✅ ربات آماده است!")
        
        # راه‌اندازی وب‌هوک
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path="webhook",
            webhook_url=WEBHOOK_URL,
        )
        
    except Exception as e:
        logger.error(f"❌ خطا در راه‌اندازی ربات: {str(e)}")
        raise e

if __name__ == "__main__":
    main()
