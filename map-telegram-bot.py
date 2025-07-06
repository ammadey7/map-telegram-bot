from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import logging

# Replace with your keys
TELEGRAM_BOT_TOKEN = "8055294857:AAGMhN3QROQU7twiIPzK7_JQj_ELj6rdY2I"
GOOGLE_API_KEY = "AIzaSyApOEHWldb4HPzRon_xQf1UYz7QrwQqQe4"

# Logging
logging.basicConfig(level=logging.INFO)

async def get_location_details(query: str):
    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": GOOGLE_API_KEY,
        "language": "en"  # Change to "dv" for Dhivehi if supported
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] == "OK":
        result = data["results"][0]
        address = result["formatted_address"]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        return address, lat, lng
    return None, None, None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    address, lat, lng = await get_location_details(query)
    
    if address:
        await update.message.reply_text(f"📍 Location: {address}")
        await update.message.reply_location(latitude=lat, longitude=lng)
        maps_link = f"https://maps.google.com/?q={lat},{lng}"
        await update.message.reply_text(f"🗺️ View on map: {maps_link}")
    else:
        await update.message.reply_text("❌ Couldn't find this location. Please try a nearby landmark or correct spelling.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
