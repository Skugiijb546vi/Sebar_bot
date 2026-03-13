import os
import subprocess
import requests
from pyrogram import Client

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
        print("📥 داگرتنی ڤیدیۆ...")
        subprocess.run(["yt-dlp", "-o", "video.mp4", video_url])
        
        if mode == "merge_dual" and audio_url:
            print("🎙 داگرتنی دەنگی دۆبلاژ...")
            r = requests.get(audio_url)
            with open("kurdish.mp3", "wb") as f:
                f.write(r.content)
            
            print("🎛 تێکەڵکردنی دەنگەکان...")
            # ئەم فەرمانە ڤیدیۆکە و هەردوو دەنگەکە دەکاتە یەک فایل
            subprocess.run([
                "ffmpeg", "-i", "video.mp4", "-i", "kurdish.mp3",
                "-map", "0:v", "-map", "1:a", "-map", "0:a",
                "-c:v", "copy", "-c:a:0", "aac", "-c:a:1", "copy",
                "-metadata:s:a:0", "title=Kurdish", 
                "-metadata:s:a:1", "title=Original",
                "final.mkv"
            ])
            app.send_document(chat_id, "final.mkv", caption="🎬 فیلمی Dual Audio ئامادەیە")
        
        # مۆدەکانی تر وەک خۆیانن...
        elif mode == "1":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "audio.mp3"])
            app.send_audio(chat_id, "audio.mp3")
        elif mode == "2":
            app.send_video(chat_id, "video.mp4")

run()
