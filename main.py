from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import websockets
import json

# WebSocket listener function to get the latest price
async def get_btc_price():
    uri = "wss://fstream.binance.com/ws/btcusdt@markPrice"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                price = data['p']
                print(f"Received BTC price: {price}")  # Log received price
                return price
    except Exception as e:
        print(f"Error: {e}")  # Log any connection errors
        return "Error: Could not retrieve price."

# Telegram bot function to send the BTC price
async def btc(update: Update, context: CallbackContext) -> None:
    print("Received /btc command")  # Log when the command is received
    price = await get_btc_price()
    await update.message.reply_text(f"Current BTC price: {price} USDT")

def main():
    # Set up the Application and Dispatcher with your token
    application = Application.builder().token("8595969184:AAH59kiHSrg2kGoNuqynp0qrklHAwxlEInY").build()

    # Register the /btc command
    application.add_handler(CommandHandler("btc", btc))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
