from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import logging
from fuzzywuzzy import process

import os

# ✅ Load your token from environment variables for safety
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)

# ✅ Known locations (you can expand this)
KNOWN_LOCATIONS = {
    "tsunami monument": "Tsunami Monument",
    "majeedhee magu": "Majeedhee Magu",
    "sto aifaanu": "STO Aifaanu",
    "male city council": "Malé City Council",
    "henveiru dhandu": "Henveiru Dhandu",
    "villa college": "Villa College",
    "hulhumale central park": "Hulhumale Central Park",
    "villingili ferry terminal": "Villingili Ferry Terminal",
    "fhiyavalhu mosque": "Fiyavalhu Mosque",
}

# ✅ Fuzzy match using fuzzywuzzy
def fuzzy_match(query: str) -> str:
    best_match, score = process.extractOne(query.lower(), KNOWN_LOCATIONS.keys())
    return KNOWN_LOCATIONS[best_match] if score > 70 else query

# ✅ Detect if Thaana (Dhivehi) characters are present
def is_dhivehi(text: str) -> bool:
    return any("ހ" <= c <= "ް" for c in text)

# ✅ Get location from Google Geocoding API
async def get_location_details(query: str, is_dv: bool = False):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": GOOGLE_API_KEY,
        "language": "dv" if is_dv else "en"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") == "OK" and data["results"]:
        result = data["results"][0]
        address = result["formatted_address"]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]
        return address, lat, lng
    return None, None, None

# ✅ Main handler for user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    # Detect language
    is_dv = is_dhivehi(query)

    # Apply fuzzy matching if it's not Dhivehi
    if not is_dv:
        query = fuzzy_match(query)

    # Search location
    address, lat, lng = await get_location_details(query, is_dv)

    if address:
        await update.message.reply_text(f"📍 Location: {address}")
        await update.message.reply_location(latitude=lat, longitude=lng)
        maps_link = f"https://maps.google.com/?q={lat},{lng}"
        await update.message.reply_text(f"🗺️ [Open in Google Maps]({maps_link})", parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Couldn't find: *{query}*\n\nTry a known place like:\n"
            "- Tsunami Monument\n"
            "- Majeedhee Magu\n"
            "- Hulhumale Central Park\n"
            "- Villingili Ferry Terminal",
            parse_mode="Markdown"
        )

# ✅ Start the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
