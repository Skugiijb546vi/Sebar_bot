import os
import asyncio
from pyrogram import Client

API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")
CHAT_ID = -1003503643297

async def main():
    if not VIDEO_URL:
        print("❌ هیچ لینکێک نییە!")
        return

    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print("📥 دەستکرا بە داگرتنی ڤیدیۆکە...")
        # داگرتن بەناوی جێگیر
        os.system(f'wget -q -O "video.mp4" "{VIDEO_URL}"')
        
        # --- بەشی جیاکردنەوەی دەنگ (چاککراو) ---
        print("🎵 خەریکی جیاکردنەوەی دەنگم...")
        # بەکارهێنانی فەرمانی سادەتر بۆ ئەوەی تووشی هەڵەی pipe نەبێت
        os.system('ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3 -y')
        
        if os.path.exists("audio.mp3"):
            print("✅ دەنگەکە بە سەرکەوتوویی جیاکرایەوە.")
        else:
            print("❌ کێشەیەک لە جیاکردنەوەی دەنگدا هەبوو.")

        # ١. ناردنی ڤیدیۆکە
        print("📤 ناردنی ڤیدیۆ...")
        await app.send_document(chat_id=CHAT_ID, document="video.mp4", caption="🎬 فیلمی تەواو")
        
        # ٢. ناردنی دەنگەکە ئەگەر دروست بووبوو
        if os.path.exists("audio.mp3"):
            print("📤 ناردنی دەنگی فیلمەکە...")
            await app.send_audio(chat_id=CHAT_ID, audio="audio.mp3", caption="🎵 دەنگی جیاکراوەی فیلمەکە")
        
        print("✨ هەموو کارەکان تەواو بوون!")

if __name__ == "__main__":
    asyncio.run(main())
