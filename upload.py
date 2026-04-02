import os
import subprocess
import requests
from pyrogram import Client

# زانیارییەکان
api_id = 22697853
api_hash = "4801319a0aeb52817bc01d3cc60bb245"
bot_token = "8626090651:AAFQAfMXvzMfWRfQ3qp2pw7Lix6EHusjJ8g"
chat_id = "@ajsjajaauai"

video_url = os.environ.get("VIDEO_URL")
audio_url = os.environ.get("AUDIO_URL")
mode = os.environ.get("MODE")

app = Client("sebar_uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def run():
    with app:
        print(f"📥 دەستکردن بە کار بۆ مۆدی: {mode}")
        
        # لێرەدا فەرمانەکەمان تۆکمەتر کردووە
        download_cmd = [
            "yt-dlp",
            "--impersonate", "chrome",  # ئێستا بەهۆی curl_cffi کار دەکات
            "--referer", "https://kurdsubtitle.net/",
            "--add-header", "Origin:https://kurdsubtitle.net",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            # گۆڕینی -f best بۆ -f b بۆ نەمانی ئیرۆر و کوالێتی باش
            "-f", "b", 
            "-o", "video.mp4",
            video_url
        ]
        
        print("🚀 خەریکی داگرتنی ڤیدیۆکەم بە مۆدی پارێزراو (Chrome Stealth)...")
        result = subprocess.run(download_cmd)
        
        if not os.path.exists("video.mp4"):
            print("❌ شکستی هێنا! دڵنیابە curl_cffi دامەزراوە و لینکەکە نوێیە.")
            return

        # پڕۆسەی ناردن بۆ تێلێگرام (وەک کۆدەکەی پێشوو)
        if mode == "1":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            app.send_audio(chat_id=chat_id, audio="audio.mp3")
        else:
            # پشکنینی قەبارە و ناردنی ڤیدیۆ
            file_size = os.path.getsize("video.mp4") / (1024 * 1024)
            if file_size > 1990:
                 subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "28", "final.mp4"])
                 app.send_video(chat_id=chat_id, video="final.mp4", caption="🎬 سێبار تیڤی - ڤیدیۆی چڕکراوە")
            else:
                 app.send_video(chat_id=chat_id, video="video.mp4", caption="🎬 سێبار تیڤی - فەرموو")

if __name__ == "__main__":
    run()
