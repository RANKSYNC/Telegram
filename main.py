from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# توکن ربات خود را وارد کنید
TOKEN = "YOUR_BOT_TOKEN"  # توکن ربات خود را اینجا وارد کنید

# تابع /start
async def start(update: Update, context: CallbackContext) -> None:
    # وقتی کاربر دستور /start را وارد کند، پیام خوشامدگویی ارسال می‌شود
    await update.message.reply_text('سلام! من ربات هستم.')

# ساختن نمونه‌ای از اپلیکیشن
application = Application.builder().token(TOKEN).build()

# افزودن CommandHandler برای دستور /start
application.add_handler(CommandHandler("start", start))

# شروع اجرای polling
application.run_polling()
