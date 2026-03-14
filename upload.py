import os
import subprocess
import requests
from pyrogram import Client

# زانیارییەکان
api_id = 22697853
api_hash = "4801319a0aeb52817bc01d3cc60bb245"
bot_token = "8626090651:AAGHXnPCYKcpxYMgZhzWNHFla_3HszBBnGY"

# بەکارهێنانی ویزەرنەیم بەبێ گۆڕینی بۆ ژمارە
chat_id = "@ajsjajaauai"

video_url = os.environ.get("VIDEO_URL")
audio_url = os.environ.get("AUDIO_URL")
mode = os.environ.get("MODE")

app = Client("sebar_uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def run():
    with app:
        print(f"📥 دەستکردن بە کار بۆ مۆدی: {mode}")
        
        # داگرتنی ڤیدیۆکە - بەکارهێنانی کوالێتی گونجاو
        subprocess.run(["yt-dlp", "-f", "bestvideo+bestaudio/best", "-o", "video.mp4", video_url])
        
        # پشکنین: ئایا ڤیدیۆکە بە سەرکەوتوویی دانەگیراوە؟
        if not os.path.exists("video.mp4"):
            print("❌ کێشە لە داگرتنی ڤیدیۆکە هەیە، سێرڤەری سەرچاوە وەڵام ناداتەوە.")
            return

        # ١. تێکەڵکردنی دۆبلاژ (Dual Audio)
        if mode == "merge_dual" and audio_url:
            r = requests.get(audio_url)
            with open("kurdish.mp3", "wb") as f: f.write(r.content)
            subprocess.run([
                "ffmpeg", "-i", "video.mp4", "-i", "kurdish.mp3",
                "-map", "0:v", "-map", "1:a", "-map", "0:a",
                "-c:v", "copy", "-c:a", "aac", 
                "-metadata:s:a:0", "title=Kurdish", "-metadata:s:a:1", "title=Original",
                "output.mkv"
            ])
            if os.path.exists("output.mkv"):
                app.send_document(chat_id=chat_id, document="output.mkv", caption="🎬 فیلمی دۆبلاژ و ئۆرجیناڵ ئامادەیە")

        # ٢. بچووککردنەوە بۆ 70MB
        elif mode == "small_70":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "33", "-s", "854x480", "small.mp4"])
            if os.path.exists("small.mp4"):
                app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی بچووک (70MB)")

        # ٣. بچووککردنەوە بۆ 150MB
        elif mode == "small_150":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "28", "-s", "1280x720", "small.mp4"])
            if os.path.exists("small.mp4"):
                app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی مامناوەند (150MB)")

        # ٤. تەنها دەنگ
        elif mode == "1":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            if os.path.exists("audio.mp3"):
                app.send_audio(chat_id=chat_id, audio="audio.mp3")

        # ٥. ڤیدیۆی ئاسایی (دەنگ و ڕەنگ)
        else:
            app.send_video(chat_id=chat_id, video="video.mp4", caption="🎬 سێبار تیڤی - فەرموو فیلمەکە")

if __name__ == "__main__":
    run()
