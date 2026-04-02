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

def get_size_mb(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0

def check_and_compress(file_path):
    size = get_size_mb(file_path)
    if size > 1990:
        print(f"⚠️ فایلەکە گەورەیە ({size:.2f} MB)، خەریکی بچووککردنەوەم بۆ ژێر ٢ گێگا...")
        compressed_file = "final_fixed.mp4"
        subprocess.run(["ffmpeg", "-i", file_path, "-vcodec", "libx264", "-crf", "28", "-preset", "faster", "-acodec", "copy", compressed_file])
        return compressed_file
    return file_path

def run():
    with app:
        print(f"📥 دەستکردن بە کار بۆ مۆدی: {mode}")
        
        # فەرمانی پارێزراو بۆ بڕینی بەربەستی سێرڤەر (بەهۆی curl_cffi کار دەکات)
        download_cmd = [
            "yt-dlp",
            "--impersonate", "chrome",
            "--referer", "https://kurdsubtitle.net/",
            "--add-header", "Origin:https://kurdsubtitle.net",
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "-f", "b", 
            "-o", "video.mp4",
            video_url
        ]
        
        print("🚀 خەریکی داگرتنی ڤیدیۆکەم بە مۆدی پارێزراو (Chrome Stealth)...")
        subprocess.run(download_cmd)
        
        if not os.path.exists("video.mp4"):
            print("❌ شکستی هێنا! دڵنیابە curl_cffi دامەزراوە و لینکەکە نوێیە.")
            return

        # جێبەجێکردنی مۆدەکان (بەپێی ئەو دوگمەیەی لە بۆتەکەدا گیراوە)
        if mode == "merge_dual" and audio_url:
            print("🎧 خەریکی تێکەڵکردنی دەنگی دۆبلاژم...")
            r = requests.get(audio_url)
            with open("kurdish.mp3", "wb") as f: f.write(r.content)
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-i", "kurdish.mp3", "-map", "0:v", "-map", "1:a", "-map", "0:a", "-c:v", "copy", "-c:a", "aac", "output.mkv"])
            target = check_and_compress("output.mkv")
            app.send_document(chat_id=chat_id, document=target, caption="🎬 فیلمی دۆبلاژ (تێکەڵکراو) ئامادەیە")

        elif mode == "small_70":
            print("📦 خەریکی بچووککردنەوەم بۆ 70MB...")
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "35", "-s", "854x480", "small.mp4"])
            app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی 70MB")

        elif mode == "small_150":
            print("📦 خەریکی بچووککردنەوەم بۆ 150MB...")
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "30", "-s", "1280x720", "small.mp4"])
            app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی 150MB")

        elif mode == "1":
            print("🎵 خەریکی دەرهێنانی دەنگم...")
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            app.send_audio(chat_id=chat_id, audio="audio.mp3", caption="🎵 تەنها دەنگی فیلمەکە")

        else:
            print("🎬 خەریکی ناردنی ڤیدیۆی ئاساییم...")
            target = check_and_compress("video.mp4")
            app.send_video(chat_id=chat_id, video=target, caption="🎬 سێبار تیڤی - فەرموو ڤیدیۆکە")

if __name__ == "__main__":
    run()
