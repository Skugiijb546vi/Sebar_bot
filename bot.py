import telebot
import requests
import os
from flask import Flask
from threading import Thread
from telebot import apihelper

# زانیارییەکانت
BOT_TOKEN = "8626090651:AAGHXnPCYKcpxYMgZhzWNHFla_3HszBBnGY"
GITHUB_TOKEN = "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"
REPO = "Skugiijb546vi/Sebar_bot"

# سڕینەوەی پرۆکسی (لە ڕێندەر پێویستت پێی نییە و کێشەت بۆ دروست دەکات)
# apihelper.proxy = {'https': 'http://proxy.server:3128'}

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

# --- سێرڤەری ساختە بۆ ئەوەی ڕێندەر بۆتەکە نەکوژێتەوە ---
app = Flask(__name__)
@app.route('/')
def home():
    return "سێبار بۆت بە سەرکەوتوویی کار دەکات!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
# ----------------------------------------------------

@bot.message_handler(func=lambda m: True, content_types=['text', 'audio', 'voice', 'document'])
def handle(message):
    chat_id = message.chat.id
    if chat_id not in user_data: user_data[chat_id] = {"link": None, "audio": None}

    if message.content_type == 'text':
        user_data[chat_id]["link"] = message.text
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)

        btn_only_video = telebot.types.InlineKeyboardButton("🎥 تەنها ڤیدیۆ (M3U8)", callback_data="only_video")
        btn_normal = telebot.types.InlineKeyboardButton("🎬 ڤیدیۆ + دەنگ (Normal)", callback_data="2")
        btn_70mb = telebot.types.InlineKeyboardButton("📦 قەبارە 70MB", callback_data="small_70")
        btn_150mb = telebot.types.InlineKeyboardButton("📦 قەبارە 150MB", callback_data="small_150")
        btn_dual = telebot.types.InlineKeyboardButton("🎧 تێکەڵکردن (Dual Audio)", callback_data="merge_dual")
        btn_audio = telebot.types.InlineKeyboardButton("🎵 تەنها دەنگ (MP3)", callback_data="1")

        markup.add(btn_only_video) 
        markup.add(btn_normal)
        markup.add(btn_70mb, btn_150mb)
        markup.add(btn_dual)
        markup.add(btn_audio)

        bot.reply_to(message, "🎬 سێبار تیڤی ئامادەیە، بژاردەیەک هەڵبژێرە:", reply_markup=markup)

    elif message.content_type in ['audio', 'voice', 'document']:
        file_id = message.audio.file_id if message.audio else message.document.file_id
        file_info = bot.get_file(file_id)
        user_data[chat_id]["audio"] = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        bot.reply_to(message, "✅ دەنگی دۆبلاژ وەرگیرا!")

@bot.callback_query_handler(func=lambda call: True)
def action(call):
    data = user_data.get(call.message.chat.id)
    if not data or not data.get("link"):
        bot.answer_callback_query(call.id, "❌ کێشەیەک هەیە، لینکەکە نەدۆزرایەوە!")
        return

    requests.post(
        f"https://api.github.com/repos/{REPO}/actions/workflows/main.yml/dispatches",
        headers={"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"},
        json={"ref": "main", "inputs": {"video_url": data["link"], "mode": call.data, "audio_url": data.get("audio", "")}}
    )
    bot.edit_message_text(f"🚀 فەرمانی ({call.data}) نێردرا بۆ گیتھەب!", call.message.chat.id, call.message.message_id)

if __name__ == "__main__":
    # کارپێکردنی سێرڤەرەکە بۆ ڕێندەر
    t = Thread(target=run_web)
    t.start()
    # کارپێکردنی بۆتەکە خۆی
    bot.infinity_polling()
