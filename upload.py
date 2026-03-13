import os
import subprocess
import requests
from pyrogram import Client

# زانیارییەکان
api_id = 22697853
api_hash = "4801319a0aeb52817bc01d3cc60bb245"
bot_token = "8626090651:AAGHXnPCYKcpxYMgZhzWNHFla_3HszBBnGY"
chat_id = -1002347573041

video_url = os.environ.get("VIDEO_URL")
audio_url = os.environ.get("AUDIO_URL")
mode = os.environ.get("MODE")

app = Client("sebar_uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def run():
    with app:
        print("📥 خەریکی داگرتنی ڤیدیۆکەم...")
        subprocess.run(["yt-dlp", "-o", "video.mp4", video_url])
        
        # ئەگەر مۆدەکە تێکەڵکردن بوو و دەنگی ناردبوو
        if mode == "merge_dual" and audio_url:
            print("🎙 داگرتنی دەنگی دۆبلاژ...")
            r = requests.get(audio_url)
            with open("kurdish.mp3", "wb") as f:
                f.write(r.content)
            
            print("🎛 تێکەڵکردنی دەنگەکان (Dual Audio)...")
            subprocess.run([
                "ffmpeg", "-i", "video.mp4", "-i", "kurdish.mp3",
                "-map", "0:v", "-map", "1:a", "-map", "0:a",
                "-c:v", "copy", "-c:a", "aac", 
                "-metadata:s:a:0", "title=Kurdish", "-metadata:s:a:1", "title=Original",
                "final_movie.mkv"
            ])
            app.send_document(chat_id, "final_movie.mkv", caption="🎬 فیلمی Dual Audio ئامادەیە")

        elif mode == "1": # تەنها دەنگ
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            app.send_audio(chat_id, "audio.mp3", caption="🎵 دەنگی فیلمەکە")

        elif mode == "2": # دەنگ و ڕەنگ
            app.send_video(chat_id, "video.mp4", caption="🎬 فیلمەکە نێردرا")

        elif mode == "4": # بچووککردنەوە
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx265", "-crf", "28", "small.mp4"])
            app.send_video(chat_id, "small.mp4", caption="📦 ڤیدیۆی بچووککراوە")

run()
