# 📍 Greater Male Bot — Telegram Location Finder Bot

**Greater Male Bot** is a Telegram bot that helps users find the **exact location** of any place in **Malé, Maldives** (or anywhere globally), using **Google Maps**.

It supports **English and Dhivehi** inputs and returns:
- 🏠 Formatted Address  
- 📌 Location Pin  
- 🔗 Google Maps Link  
- 📍 Nearby Landmark (if matched)

---

## 🚀 How It Works

1. User sends a message like:

tsunami monument
މާފަންނު ދަނޑު
STO Home improvements


2. The bot replies with:
- 📍 Formatted location name  
- 🗺️ Google Maps location pin  
- 🔗 Link to open in Google Maps

---

## 🔧 Setup Instructions (For Developers)

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/greater-male-bot.git
cd greater-male-bot


2. Install Python Requirements
pip install -r requirements.txt

3. Create a .env or Add Tokens to the Script
TELEGRAM_BOT_TOKEN=your_telegram_token_here
GOOGLE_API_KEY=your_google_api_key_here

4.Run the Bot
python bot.py

