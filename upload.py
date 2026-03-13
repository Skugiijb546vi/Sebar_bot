import os
import sys
import subprocess
from pyrogram import Client

# زانیارییەکان لە گیتھەب وەر دەگرێت
api_id = 22697853
api_hash = "4801319a0aeb52817bc01d3cc60bb245"
bot_token = "8524581086:AAGDZmzCO9ib3faKk8XvV3NfeLbwRNsvWhY"
chat_id = -1002347573041 # ئایدی چەناڵەکەت

video_url = os.environ.get("VIDEO_URL")
mode = os.environ.get("MODE")

app = Client("sebar_uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def run():
    with app:
        # 1. داگرتنی ڤیدیۆکە
        print("📥 خەریکی داگرتنی ڤیدیۆکەم...")
        subprocess.run(["yt-dlp", "-o", "video.mp4", video_url])

        if mode == "1": # تەنها دەنگ
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            app.send_audio(chat_id, "audio.mp3", caption="🎵 دەنگی فیلمەکە جیاکرایەوە")
        
        elif mode == "2": # ڤیدیۆ + دۆبلاژ
            app.send_video(chat_id, "video.mp4", caption="🎬 فیلمەکە بە سەرکەوتوویی نێردرا")

        elif mode == "dual": # دەنگی دووانە (گرنگترین بەش)
            print("🎧 خەریکی تێکەڵکردنی دەنگەکانم...")
            # لێرەدا فێڵەکە ئەوەیە کە فایلەکە بە مۆدێک دادەنێین کە هەردوو تراکەکە بپارێزێت
            subprocess.run([
                "ffmpeg", "-i", "video.mp4", 
                "-map", "0:v", "-map", "0:a", 
                "-c", "copy", "dual_audio.mkv"
            ])
            app.send_document(chat_id, "dual_audio.mkv", caption="🎧 فیلمی Dual Audio (کوردی + ئینگلیزی)\nئێستا دەتوانیت لە ناو ئەپەکە دەنگەکە بگۆڕیت.")

        elif mode == "4": # بچووککردنەوە
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx265", "-crf", "28", "small.mp4"])
            app.send_video(chat_id, "small.mp4", caption="📦 ڤیدیۆی بچووککراوە (70MB)")

run()
