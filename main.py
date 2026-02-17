import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات
TOKEN = "8226915169:AAF4cAmZDUlR-PhDKMvI_MERxjA06W5zH3g"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 ربات قیمت ارز فعال شد!\n\n"
        "💰 **روش استفاده:**\n"
        "فقط اسم ارز رو با / بزن:\n\n"
        "🔹 /btc - بیت‌کوین\n"
        "🔹 /eth - اتریوم\n"
        "🔹 /ada - کاردانو\n"
        "🔹 /sol - سولانا\n"
        "🔹 /doge - دوج کوین\n\n"
        "✨ هر ارز دیگه‌ای هم می‌تونی امتحان کنی!"
    )

async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # گرفتن اسم ارز از دستور (بدون /)
    coin = update.message.text[1:].upper()
    
    if not coin:
        await update.message.reply_text("❌ لطفاً اسم ارز رو وارد کن")
        return
    
    # پیام انتظار
    msg = await update.message.reply_text(f"🔄 در حال دریافت {coin}...")
    
    try:
        # درخواست به بایننس
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
        r = requests.get(url, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            price = float(data['price'])
            
            # فرمت قیمت
            if price < 0.0001:
                text = f"{price:.8f}"
            elif price < 0.001:
                text = f"{price:.6f}"
            elif price < 0.01:
                text = f"{price:.5f}"
            elif price < 0.1:
                text = f"{price:.4f}"
            elif price < 1:
                text = f"{price:.3f}"
            else:
                text = f"{price:,.2f}"
            
            await msg.edit_text(f"💰 {coin}/USDT: {text}$")
        else:
            await msg.edit_text(f"❌ ارز {coin} پیدا نشد!\nمثال: /btc, /eth, /ada")
            
    except requests.exceptions.ConnectionError:
        await msg.edit_text("❌ خطای اتصال به اینترنت")
    except requests.exceptions.Timeout:
        await msg.edit_text("❌ زمان درخواست تمام شد")
    except Exception as e:
        await msg.edit_text(f"❌ خطا: {str(e)}")

def main():
    print("🚀 ربات شروع به کار کرد...")
    
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    
    # اضافه کردن هندلر برای همه دستورات
    app.add_handler(CommandHandler("btc", handle_price))
    app.add_handler(CommandHandler("eth", handle_price))
    app.add_handler(CommandHandler("ada", handle_price))
    app.add_handler(CommandHandler("sol", handle_price))
    app.add_handler(CommandHandler("doge", handle_price))
    app.add_handler(CommandHandler("xrp", handle_price))
    app.add_handler(CommandHandler("dot", handle_price))
    app.add_handler(CommandHandler("link", handle_price))
    app.add_handler(CommandHandler("matic", handle_price))
    app.add_handler(CommandHandler("avax", handle_price))
    app.add_handler(CommandHandler("bnb", handle_price))
    
    # شروع ربات
    app.run_polling()

if __name__ == "__main__":
    main()
