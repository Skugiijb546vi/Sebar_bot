import os
import subprocess
import requests
from pyrogram import Client

# زانیارییەکان
api_id = 22697853
api_hash = "4801319a0aeb52817bc01d3cc60bb245"
bot_token = "8626090651:AAGHXnPCYKcpxYMgZhzWNHFla_3HszBBnGY"

# ویزەرنەیمی چەناڵ
chat_id = "@ajsjajaauai"

video_url = os.environ.get("VIDEO_URL")
audio_url = os.environ.get("AUDIO_URL")
mode = os.environ.get("MODE")

app = Client("sebar_uploader", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# ناسنامەی وێبگەڕ (بۆ ئەوەی سێرڤەرەکە وا بزانێت مرۆڤە و بلۆکی نەکات)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def run():
    with app:
        print(f"📥 دەستکردن بە کار بۆ مۆدی: {mode}")
        
        # ١. مۆدی تەنها ڤیدیۆ (بە بەکارهێنانی سەرچاوەی ماڵپەڕ بۆ شکاندنی بلۆک و ڕاکێشانی بەرزترین کوالێتی)
        if mode == "only_video":
            print("🎥 خەریکی تێپەڕاندنی بلۆکی سێرڤەر و داگرتنی بەرزترین کوالێتیم...")
            subprocess.run([
                "yt-dlp",
                "--user-agent", USER_AGENT,
                "--add-header", "Referer: https://www.hdfilmcehennemi.nl/",
                "--add-header", "Origin: https://www.hdfilmcehennemi.nl",
                "--add-header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "--add-header", "Accept-Language: en-US,en;q=0.5",
                "--hls-prefer-native", 
                "-f", "bestvideo+bestaudio/best",
                "-o", "raw_video.mp4",
                video_url
            ])
            
            if os.path.exists("raw_video.mp4"):
                app.send_video(chat_id=chat_id, video="raw_video.mp4", caption="🎬 ڤیدیۆکە بە بەرزترین کوالێتی داگیرا!")
            else:
                print("❌ سێرڤەرەکە هێشتا ڕێگری دەکات.")
            return

        # --- مۆدەکانی تر ---
        
        # داگرتنی ڤیدیۆکە بە پڕۆگرامی ئاسایی بۆ مۆدەکانی تر
        subprocess.run([
            "yt-dlp", 
            "--user-agent", USER_AGENT,
            "-f", "bestvideo+bestaudio/best", 
            "-o", "video.mp4", 
            video_url
        ])
        
        if not os.path.exists("video.mp4"):
            print("❌ کێشە لە داگرتن هەبوو.")
            return

        # ٢. تێکەڵکردنی دۆبلاژ
        if mode == "merge_dual" and audio_url:
            headers = {'User-Agent': USER_AGENT}
            r = requests.get(audio_url, headers=headers)
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

        # ٣. بچووککردنەوە بۆ 70MB
        elif mode == "small_70":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "33", "-s", "854x480", "small.mp4"])
            if os.path.exists("small.mp4"):
                app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی بچووک (70MB)")

        # ٤. بچووککردنەوە بۆ 150MB
        elif mode == "small_150":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vcodec", "libx264", "-crf", "28", "-s", "1280x720", "small.mp4"])
            if os.path.exists("small.mp4"):
                app.send_video(chat_id=chat_id, video="small.mp4", caption="📦 قەبارەی مامناوەند (150MB)")

        # ٥. تەنها دەنگ
        elif mode == "1":
            subprocess.run(["ffmpeg", "-i", "video.mp4", "-vn", "-acodec", "libmp3lame", "audio.mp3"])
            if os.path.exists("audio.mp3"):
                app.send_audio(chat_id=chat_id, audio="audio.mp3")

        # ٦. ڤیدیۆی ئاسایی
        else:
            app.send_video(chat_id=chat_id, video="video.mp4", caption="🎬 سێبار تیڤی - فەرموو فیلمەکە")

if __name__ == "__main__":
    run()
