import telebot
import requests
import os
from flask import Flask
from threading import Thread

# --- زانیارییەکانت ---
BOT_TOKEN = "8626090651:AAFQAfMXvzMfWRfQ3qp2pw7Lix6EHusjJ8g"
GITHUB_TOKEN = "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"
REPO = "Skugiijb546vi/Sebar_bot"
# ناوی فایلەکە کە لە وۆرکفلۆوەکەدا داوات کردووە (بە شێوەی دیفۆڵت)
DEFAULT_FILE_NAME = "sebar_video_v1.safetensors"

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# --- سێرڤەری ساختە بۆ ئەوەی بۆتەکە نەکوژێتەوە ---
app = Flask(__name__)
@app.route('/')
def home():
    return "سێبار بۆت بە سەرکەوتوویی کار دەکات!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- نامەکان ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 سڵاو لە سێبار تیڤی!\n🔗 لینکی فیلم یان M3U8 بنێرە بۆ دەستپێکردن.")

@bot.message_handler(func=lambda m: True, content_types=['text', 'audio', 'voice', 'document'])
def handle(message):
    chat_id = message.chat.id
    if chat_id not in user_data: 
        user_data[chat_id] = {"link": None, "audio": None, "file_name": DEFAULT_FILE_NAME}

    if message.content_type == 'text':
        # پشکنین ئەگەر بەکارهێنەر لینک بنێرێت
        if message.text.startswith("http"):
            user_data[chat_id]["link"] = message.text
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)

            btn_only_video = telebot.types.InlineKeyboardButton("🎥 تەنها ڤیدیۆ (Ninja Mode)", callback_data="only_video")
            btn_normal = telebot.types.InlineKeyboardButton("🎬 ڤیدیۆ + دەنگ", callback_data="normal")
            btn_audio = telebot.types.InlineKeyboardButton("🎵 تەنها دەنگ (MP3)", callback_data="audio_only")

            markup.add(btn_only_video) 
            markup.add(btn_normal, btn_audio)

            bot.reply_to(message, "🎬 جۆری داگرتن هەڵبژێرە بۆ ئەم لینکە:", reply_markup=markup)
        else:
            # ئەگەر تێکست بوو بەڵام لینک نەبوو، وەک ناوی فایل دایبنێ
            user_data[chat_id]["file_name"] = message.text.replace(" ", "_") + ".safetensors"
            bot.reply_to(message, f"✅ ناوی فایل گۆڕدرا بۆ: {user_data[chat_id]['file_name']}")

    elif message.content_type in ['audio', 'voice', 'document']:
        file_id = message.audio.file_id if message.audio else (message.document.file_id if message.document else None)
        if file_id:
            file_info = bot.get_file(file_id)
            user_data[chat_id]["audio"] = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
            bot.reply_to(message, "✅ فایلی دەنگ وەرگیرا!")

@bot.callback_query_handler(func=lambda call: True)
def action(call):
    chat_id = call.message.chat.id
    data = user_data.get(chat_id)
    
    if not data or not data.get("link"):
        bot.answer_callback_query(call.id, "❌ تکایە سەرەتا لینکەکە بنێرە!")
        return

    # ئاگادارکردنەوەی بەکارهێنەر
    bot.edit_message_text("⏳ خەریکی ناردنی فەرمانم بۆ گیتھەب...", chat_id, call.message.message_id)

    # ناردنی داواکاری بۆ GitHub Actions
    # تێبینی: لێرەدا inputs دەبێت ڕێک بێت لەگەڵ ئەو ناوانەی لە وۆرکفلۆوەکە داتناوە
    payload = {
        "ref": "main",
        "inputs": {
            "video_url": data["link"],
            "file_name": data.get("file_name", DEFAULT_FILE_NAME)
        }
    }

    response = requests.post(
        f"https://api.github.com/repos/{REPO}/actions/workflows/main.yml/dispatches",
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        },
        json=payload
    )

    if response.status_code == 204:
        bot.edit_message_text(f"🚀 فەرمانی دابەزاندن بە سەرکەوتوویی نێردرا!\n📦 ناو: {data['file_name']}", chat_id, call.message.message_id)
    else:
        bot.edit_message_text(f"❌ هەڵەیەک ڕوویدا لە پەیوەندی بە گیتھەب:\n{response.status_code}", chat_id, call.message.message_id)

if __name__ == "__main__":
    try:
        bot.remove_webhook()
    except:
        pass

    t = Thread(target=run_web)
    t.daemon = True
    t.start()
    
    print("🚀 Sebar Bot is Running...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
