import os
import feedparser
import time
from telegram import Bot
from telegram.request import HTTPXRequest

# ✅ بيانات البوت
BOT_TOKEN = "7070457152:AAHkZjquF7p4vtEK31zBkI9c6K58mQXXZZU"
CHANNEL_ID = "@Ricosignal"

# تأكد من أن مجلد data موجود
if not os.path.exists("data"):
    os.makedirs("data")

SEEN_FILE = "data/seen_urls.txt"
bot = Bot(token=BOT_TOKEN, request=HTTPXRequest())

# ✅ مصادر RSS
RSS_FEEDS = [
    "https://arab-btc.net/feed/",
    "https://bitcoinnews.ae/feed/",
    "https://arab.dailyforex.com/feeds/all-articles",
    "https://www.arabictrader.com/ar/technical-analysis/forex/rss",
    "https://www.argaam.com/ar/rss",
    "https://www.aleqt.com/rss"
]

def load_seen_urls():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def save_seen_url(url):
    with open(SEEN_FILE, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def fetch_and_send():
    seen_urls = load_seen_urls()
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            title = entry.title
            link = entry.link

            if link in seen_urls:
                continue

            hashtags = "#أخبار #Crypto #Forex"
            message = f"📰 {title}\n🔗 {link}\n\n{hashtags}"

            try:
                bot.send_message(chat_id=CHANNEL_ID, text=message)
                print(f"✔️ نُشرت: {title}")
                save_seen_url(link)
                time.sleep(2)
            except Exception as e:
                print(f"❌ خطأ أثناء النشر: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_send()
        time.sleep(600)
