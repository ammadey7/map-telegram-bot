import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from urllib.parse import quote_plus

# ✅ Load tokens from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)

# ✅ Detect if Dhivehi (Thaana script) is used
def is_dhivehi(text: str) -> bool:
    return any("ހ" <= c <= "ް" for c in text)

# ✅ Search location details using Google Places API
async def search_places(query: str, is_dv: bool = False):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query + " in Maldives",
        "key": GOOGLE_API_KEY,
        "language": "dv" if is_dv else "en"
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

# ✅ Handle incoming Telegram messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    is_dv = is_dhivehi(query)

    # 🔍 Fetch locations from Google Places
    results = await search_places(query, is_dv)

    if results:
        pins = []
        for result in results[:5]:  # Limit to 5 results
            name = result.get("name", "Unknown")
            address = result.get("formatted_address", "No address available")
            pins.append(f"📍 *{name}*\n{address}")

        # 📍 Prepare map search URL
        encoded_query = quote_plus(query + " in Maldives")
        maps_link = f"https://www.google.com/maps/search/{encoded_query}"

        # 📦 Send summary + map
        reply_text = "\n\n".join(pins) + f"\n\n[🗺️ View All on Map]({maps_link})"
        await update.message.reply_text(reply_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            f"❌ Couldn't find anything for: *{query}*\nTry asking:\n- Where is Majeedhee Magu?\n- Flower shops near me",
            parse_mode="Markdown"
        )

# ✅ Main bot launcher
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
