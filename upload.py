import os
import asyncio
from pyrogram import Client

API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")
CHAT_ID = -1003503643297

async def main():
    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print("📥 دەستکرا بە داگرتنی ڤیدیۆکە...")
        os.system(f'wget -q -O "video.mp4" "{VIDEO_URL}"')
        
        # --- بەشی جیاکردنەوەی دەنگ ---
        print("🎵 خەریکی جیاکردنەوەی دەنگم (MP3)...")
        # بەکارهێنانی ffmpeg بۆ دەرهێنانی دەنگ بە کوالێتی بەرز
        os.system('ffmpeg - i video.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3')
        
        # ١. ناردنی ڤیدیۆکە
        print("📤 ناردنی ڤیدیۆ...")
        await app.send_document(chat_id=CHAT_ID, document="video.mp4", caption="🎬 فیلمی تەواو")
        
        # ٢. ناردنی دەنگەکە
        print("📤 ناردنی دەنگی فیلمەکە...")
        await app.send_audio(chat_id=CHAT_ID, audio="audio.mp3", caption="🎵 دەنگی فیلمەکە (بۆ وەرگێڕان یان گوێگرتن)")
        
        print("✨ هەموو کارەکان بە سەرکەوتوویی تەواو بوون!")

if __name__ == "__main__":
    asyncio.run(main())
