import os
import asyncio
import subprocess
from pyrogram import Client

API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")

# لێرەدا یوزەرنەیمی چەناڵەکە بەکاردەهێنین بۆ ئەوەی کێشەی ID نەمێنێت
CHAT_ID = "@ajsjajaauai" 

async def main():
    if not VIDEO_URL:
        print("❌ هیچ لینکێک نییە!")
        return

    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print(f"🔗 هەوڵدان بۆ بەستنەوە بە چەناڵی: {CHAT_ID}")
        
        # ١. داگرتنی ڤیدیۆ
        print("📥 خەریکی داگرتنی ڤیدیۆکەم...")
        subprocess.run(['curl', '-L', '-o', 'video.mp4', VIDEO_URL])
        
        if not os.path.exists("video.mp4") or os.path.getsize("video.mp4") == 0:
            print("❌ داگرتن شکستی هێنا!")
            return

        # ٢. جیاکردنەوەی دەنگ
        print("🎵 خەریکی جیاکردنەوەی دەنگم...")
        subprocess.run(['ffmpeg', '-i', 'video.mp4', '-q:a', '0', '-map', 'a', 'audio.mp3', '-y'])
        
        # ٣. ناردنی ڤیدیۆکە
        print("📤 ناردنی ڤیدیۆ بۆ تێلیگرام...")
        try:
            await app.send_document(
                chat_id=CHAT_ID, 
                document="video.mp4", 
                caption="🎬 SEBAR TV - فیلمی تەواو"
            )
            
            # ٤. ناردنی دەنگەکە
            if os.path.exists("audio.mp3"):
                print("📤 ناردنی دەنگەکە...")
                await app.send_audio(
                    chat_id=CHAT_ID, 
                    audio="audio.mp3", 
                    caption="🎵 دەنگی جیاکراوەی فیلمەکە"
                )
            print("✨ هەموو کارەکان بە سەرکەوتوویی تەواو بوون!")
        except Exception as e:
            print(f"❌ کێشەیەک لە ناردندا هەبوو: {e}")

if __name__ == "__main__":
    asyncio.run(main())
