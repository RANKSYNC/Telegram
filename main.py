from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import asyncio
import websockets
import json

# WebSocket listener function to get the latest price for a specific symbol
async def get_price(symbol: str):
    uri = f"wss://stream.binance.com:9443/ws/{symbol.lower()}usdt@ticker"  # Modify to match the format of the symbol

    try:
        async with websockets.connect(uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                price = data['c']
                return price
    except Exception as e:
        print(f"Error: {e}")  # Log any connection errors
        return None

# Telegram bot function to send the specific price based on the command
async def price(update: Update, context: CallbackContext) -> None:
    # Check if the user provided a symbol
    if context.args:
        symbol = context.args[0].upper()  # Convert symbol to uppercase for consistency
        
        # Check for supported symbols and call get_price
        if symbol in ['BTC', 'ADA', 'ETH', 'BNB', 'XRP', 'LTC']:  # Add more symbols as needed
            symbol_name = f"{symbol}USDT"
            price = await get_price(symbol_name)
            
            if price:
                await update.message.reply_text(f"Price for {symbol_name}: {price} USDT")
            else:
                await update.message.reply_text(f"Sorry, I couldn't fetch the price for {symbol_name}.")
        else:
            await update.message.reply_text("Invalid symbol. Please use one of the following: BTC, ADA, ETH, BNB, XRP, LTC.")
    else:
        await update.message.reply_text("Please provide a symbol (e.g., /price btc).")

# Set up the bot with the /price command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Type /price <symbol> to get the price of any coin (e.g., /price btc).")

def main():
    # Set up the Application and Dispatcher with your token
    application = Application.builder().token("8226915169:AAGQeH7cTTBQBmMqFsRWAG7nj7BtQCNa2BQ").build()

    # Register the /price and /start commands
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
