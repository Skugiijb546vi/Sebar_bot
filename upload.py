import os
import asyncio
import subprocess
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
        print("📥 خەریکی داگرتنی ڤیدیۆکەم...")
        
        # بەکارهێنانی curl لەبری wget چونکە لە گیتھەب جێگیرترە
        download = subprocess.run(['curl', '-L', '-o', 'video.mp4', VIDEO_URL])
        
        if download.returncode != 0 or not os.path.exists("video.mp4") or os.path.getsize("video.mp4") == 0:
            print("❌ داگرتنی ڤیدیۆکە سەرکەوتوو نەبوو یان فایلەکە بەتاڵە!")
            return

        # --- جیاکردنەوەی دەنگ ---
        print("🎵 خەریکی جیاکردنەوەی دەنگم...")
        # فەرمانی FFmpeg بە شێوەی لیست بۆ ئەوەی هیچ کێشەی نێوان (Space) دروست نەبێت
        subprocess.run(['ffmpeg', '-i', 'video.mp4', '-q:a', '0', '-map', 'a', 'audio.mp3', '-y'])
        
        # ناردنی ڤیدیۆ
        print("📤 ناردنی ڤیدیۆ...")
        await app.send_document(
            chat_id=CHAT_ID, 
            document="video.mp4", 
            caption="🎬 فیلمی تەواو (SEBAR TV)"
        )
        
        # ناردنی دەنگ ئەگەر دروست ببوو و بەتاڵ نەبوو
        if os.path.exists("audio.mp3") and os.path.getsize("audio.mp3") > 0:
            print("📤 ناردنی دەنگەکە...")
            await app.send_audio(
                chat_id=CHAT_ID, 
                audio="audio.mp3", 
                caption="🎵 دەنگی جیاکراوەی فیلمەکە"
            )
        
        print("✨ هەموو کارەکان بە سەرکەوتوویی تەواو بوون!")

if __name__ == "__main__":
    asyncio.run(main())
