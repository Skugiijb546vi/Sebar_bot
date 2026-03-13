import os, asyncio, subprocess
from pyrogram import Client

API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")
MODE = os.environ.get("MODE")
CHAT_ID = "@ajsjajaauai"

async def main():
    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print(f"📥 دەستکرا بە داگرتن... مۆد: {MODE}")
        # داگرتنی فایلی سەرەکی
        subprocess.run(['curl', '-L', '-o', 'input_file', VIDEO_URL])
        
        # ١. تەنها دەنگ
        if MODE == "1":
            subprocess.run(['ffmpeg', '-i', 'input_file', '-q:a', '0', '-map', 'a', 'audio.mp3', '-y'])
            await app.send_audio(CHAT_ID, audio="audio.mp3", caption="🎵 تەنها دەنگی فیلمەکە")

        # ٢. دەنگ و ڕەنگ (ڤیدیۆکە و دەنگەکە پێکەوە وەک دوو فایلی جیاواز)
        elif MODE == "2":
            subprocess.run(['ffmpeg', '-i', 'input_file', '-q:a', '0', '-map', 'a', 'audio.mp3', '-y'])
            await app.send_document(CHAT_ID, document="input_file", caption="🎬 فیلمی تەواو")
            await app.send_audio(CHAT_ID, audio="audio.mp3", caption="🎵 دەنگی فیلمەکە")

        # ٣. تەنها ڤیدیۆ
        elif MODE == "3":
            await app.send_document(CHAT_ID, document="input_file", caption="🎬 تەنها ڤیدیۆی فیلمەکە")

        # ٤. بچووککردنەوەی فیلمەکە بۆ 70MB
        elif MODE == "4":
            print("📉 خەریکی بچووککردنەوەم...")
            # لێرەدا بیتڕەیتەکە ڕێکدەخەین بۆ ئەوەی قەبارەکە نزیک بێتەوە لە ٧٠ مێگابایت
            subprocess.run(['ffmpeg', '-i', 'input_file', '-vcodec', 'libx264', '-crf', '30', '-preset', 'ultrafast', '-vf', 'scale=-2:480', 'compressed.mp4', '-y'])
            await app.send_video(CHAT_ID, video="compressed.mp4", caption="📉 فیلمی بچووککراوە (70MB)")

asyncio.run(main())
