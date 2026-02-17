from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import websockets
import json

# WebSocket listener function to get the latest prices for all pairs
async def get_all_prices(update: Update, context: CallbackContext) -> None:
    uri = "wss://stream.binance.com:9443/stream?streams=!ticker@arr"

    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            
            # Preparing message to send to the Telegram group
            price_message = ""
            for symbol in data['data']:
                symbol_name = symbol['s']
                price = symbol['c']
                price_message += f"Price for {symbol_name}: {price} USDT\n"

            # Send the price information to Telegram
            await update.message.reply_text(price_message)
            await asyncio.sleep(1)  # sleep for a moment before checking for new data

# Set up the bot with the /prices command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Type /prices to get real-time prices for all pairs on Binance.")

def main():
    # Set up the Application and Dispatcher with your token
    application = Application.builder().token("8226915169:AAGQeH7cTTBQBmMqFsRWAG7nj7BtQCNa2BQ").build()

    # Register the /prices command
    application.add_handler(CommandHandler("prices", get_all_prices))
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
