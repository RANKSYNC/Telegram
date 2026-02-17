import os
import json
import websockets
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")  # توکن رباتت رو اینجا وارد کن

# اینجا همون WebSocket URL برای قیمت بیت کوین هست
WEBSOCKET_URL = "wss://fstream.binance.com/ws/btcusdt@markPrice"

# تابع برای دریافت قیمت از WebSocket
async def get_price():
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            price = data['p']
            return price

# دستور برای ارسال قیمت به گروه
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "بیت کوین" in text:  # اینجا برای "بیت کوین" یا هر ارز دیجیتال دیگه میشه تغییر داد
        price = await get_price()
        await update.message.reply_text(f"قیمت بیت کوین: {price} USDT")

# ساخت اپلیکیشن و متصل کردن آن به تلگرام
application = ApplicationBuilder().token(TOKEN).build()

# اضافه کردن هَندلر برای پیام‌های گروه
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

# شروع ربات
application.run_polling()
