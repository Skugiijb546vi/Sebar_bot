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

# فەرمانی دۆزینەوەی Referer بەپێی لینکەکە
def get_headers(url):
    headers = ["--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"]
    if "kurdsubtitle" in url or "greenstream" in url:
        headers.extend(["--add-header", "Referer:https://kurdsubtitle.net/"])
    elif "hdfilmcehennemi" in url:
        headers.extend(["--add-header", "Referer:https://www.hdfilmcehennemi.nl/"])
    return headers

def get_size_mb(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0

def check_and_compress(file_path):
    size = get_size_mb(file_path)
    if size > 1990:
        print(f"⚠️ فایلەکە گەورەیە ({size:.2f} MB)، خەریکی بچووککردنەوەم...")
        compressed_file = "final_fixed.mp4"
        subprocess.run(["ffmpeg", "-i", file_path, "-vcodec", "libx264", "-crf", "28", "-preset", "faster", "-acodec", "copy", compressed_file])
        return compressed_file
    return file_path

def run():
    with app:
        print(f"📥 دەستکردن بە کار بۆ مۆدی: {mode}")
        headers = get_headers(video_url)
        
        # ١. داگرتنی ڤیدیۆ بە هەموو مەرجەکانەوە
        download_cmd = ["yt-dlp"] + headers + ["-f", "bestvideo+bestaudio/best", "-o", "video.mp4", video_url]
        subprocess.run(download_cmd)
        
        if not os.path.exists("video.mp4"):
            print("❌ فیلمەکە دانەبەزی! ئەگەری زۆرە لینکەکە Expire بووبێت.")
            return

        # ٢. جێبەجێکردنی مۆدە جیاوازەکان
        if mode == "merge_dual" and audio_url:
            r = requests.get(audio_url)
            with open("kurdish.mp3", "wb") as f: f.write(r.content)
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-i", "kurdish.mp3", "-map", "0:v", "-map", "1:a", "-map", "0:a", "-c:v", "copy", "-c:a", "aac", "output.mkv"])
            target = check_and_compress("output.mkv")
            app.send_document(chat_id=chat_id, document=target, caption="🎬 فیلمی دۆبلاژ ئامادەیە")

        elif mode == "small_70":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "35", "-s", "854x480", "small.mp4"])
            app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 70MB Optimized")

        elif mode == "small_150":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "30", "-s", "1280x720", "small.mp4"])
            app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 150MB Optimized")

        elif mode == "1": # تەنها دەنگ
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            app.send_audio(chat_id=chat_id, audio="audio.mp3", caption="🎵 تەنها دەنگی فیلمەکە")

        else: # بۆ مۆدی Normal (2) یان only_video
            target = check_and_compress("video.mp4")
            app.send_video(chat_id=chat_id, video=target, caption="🎬 سێبار تیڤی - فەرموو فیلمەکە")

if __name__ == "__main__":
    run()
