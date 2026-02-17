from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import websockets
import json
import os

# WebSocket listener function to get the latest price
async def get_btc_price():
    uri = "wss://fstream.binance.com/ws/btcusdt@markPrice"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                price = data['p']
                print(f"Received BTC price: {price}")
                return price
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Could not retrieve price."

# Telegram bot function to send the BTC price
async def btc(update: Update, context: CallbackContext) -> None:
    print("Received /btc command")
    price = await get_btc_price()
    
    print(f"BTC Price to send: {price}")
    
    if price:
        await update.message.reply_text(f"Current BTC price: {price} USDT")
    else:
        await update.message.reply_text("Sorry, I couldn't fetch the BTC price at the moment.")

def main():
    # Webhook setup (configure properly with your URL)
    application = Application.builder().token("YOUR_BOT_API_KEY").build()

    # Register the /btc command
    application.add_handler(CommandHandler("btc", btc))

    # Setup webhook (replace with your actual domain)
    application.bot.set_webhook(url='https://yourdomain.com/YOUR_BOT_API_KEY')

    # Start the bot using webhook (this will replace polling)
    application.run_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), url_path="YOUR_BOT_API_KEY", webhook_url="https://yourdomain.com/YOUR_BOT_API_KEY")

if __name__ == '__main__':
    asyncio.run(main())
