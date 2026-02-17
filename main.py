import os
import requests
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات
TOKEN = "8226915169:AAF4cAmZDUlR-PhDKMvI_MERxjA06W5zH3g"

print(f"پایتون ورژن: {sys.version}")
print("🚀 ربات در حال راه‌اندازی...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 ربات قیمت ارز فعال شد!\n\n"
        "💰 برای دیدن قیمت، اسم ارز رو با / بزن:\n"
        "🔹 /btc - بیت‌کوین\n"
        "🔹 /eth - اتریوم\n"
        "🔹 /ada - کاردانو\n"
        "🔹 /sol - سولانا\n"
        "🔹 /doge - دوج کوین\n\n"
        "✨ مثال: /btc"
    )

async def price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # گرفتن اسم ارز
    coin = update.message.text[1:].upper()
    
    # پیام انتظار
    msg = await update.message.reply_text(f"🔄 در حال دریافت {coin}...")
    
    try:
        # درخواست به بایننس
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            price = float(data['price'])
            
            # فرمت قیمت
            if price < 0.00001:
                text = f"{price:.10f}"
            elif price < 0.0001:
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
            await msg.edit_text(f"❌ ارز {coin} پیدا نشد!")
            
    except requests.exceptions.ConnectionError:
        await msg.edit_text("❌ خطای اتصال به اینترنت")
    except requests.exceptions.Timeout:
        await msg.edit_text("❌ زمان درخواست تمام شد")
    except Exception as e:
        await msg.edit_text(f"❌ خطا: {str(e)}")

def main():
    print("✅ ربات آماده کار است!")
    
    app = Application.builder().token(TOKEN).build()
    
    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    
    # لیست ارزهای پشتیبانی شده
    coins = ["btc", "eth", "ada", "sol", "doge", "xrp", "dot", "link", "matic", "avax", "bnb", "shib", "ltc", "bch", "atom", "uni", "apt", "arb", "op", "inj"]
    
    for coin in coins:
        app.add_handler(CommandHandler(coin, price_handler))
    
    # شروع ربات
    app.run_polling()

if __name__ == "__main__":
    main()
