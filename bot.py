from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests
import os
import logging

# Environment tokens
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

logging.basicConfig(level=logging.INFO)

# Detect Dhivehi (Thaana characters)
def is_dhivehi(text: str) -> bool:
    return any("ހ" <= c <= "ް" for c in text)

# Query Google Places API with full free-form text
def search_google_places(query: str):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": GOOGLE_API_KEY,
        "region": "mv",
        "language": "dv" if is_dhivehi(query) else "en"
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    if data.get("status") == "OK":
        for place in data.get("results", []):
            name = place.get("name")
            address = place.get("formatted_address")
            lat = place["geometry"]["location"]["lat"]
            lng = place["geometry"]["location"]["lng"]
            maps_link = f"https://maps.google.com/?q={lat},{lng}"
            results.append((name, address, lat, lng, maps_link))
    return results

# Bot message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    results = search_google_places(query)

    if results:
        for name, address, lat, lng, link in results[:5]:
            await update.message.reply_text(f"📍 *{name}*\n{address}", parse_mode="Markdown")
            await update.message.reply_location(latitude=lat, longitude=lng)
            await update.message.reply_text(f"[🗺️ Open in Google Maps]({link})", parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Couldn't find anything for: *{query}*",
            parse_mode="Markdown"
        )

# Run the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
