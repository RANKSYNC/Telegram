from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import websockets
import json

# WebSocket listener function to get the latest price
async def get_btc_price():
    uri = "wss://fstream.binance.com/ws/btcusdt@markPrice"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            price = data['p']
            return price

# Telegram bot function to send the BTC price
async def btc(update: Update, context: CallbackContext) -> None:
    # Get BTC price from WebSocket
    price = await get_btc_price()
    await update.message.reply_text(f"Current BTC price: {price} USDT")

def main():
    # Set up the Application and Dispatcher (new method)
    application = Application.builder().token("YOUR_BOT_API_KEY").build()

    # Register the /btc command
    application.add_handler(CommandHandler("btc", btc))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
