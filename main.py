import asyncio
import websockets
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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
def btc(update: Update, context: CallbackContext) -> None:
    # Get BTC price from WebSocket
    price = asyncio.run(get_btc_price())
    update.message.reply_text(f"Current BTC price: {price} USDT")

def main():
    # Set up the Updater and Dispatcher
    updater = Updater("YOUR_BOT_API_KEY", use_context=True)
    dispatcher = updater.dispatcher
    
    # Register the /btc command
    dispatcher.add_handler(CommandHandler("btc", btc))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
