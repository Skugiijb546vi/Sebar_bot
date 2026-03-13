import os
import asyncio
from pyrogram import Client

# زانیارییە نوێیەکان
API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")
CHAT_ID = -1003503643297

async def main():
    if not VIDEO_URL:
        print("❌ هیچ لینکێک دابین نەکراوە!")
        return

    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print(f"📥 دەستکرا بە داگرتنی فایل لە: {VIDEO_URL}")
        
        # داگرتنی فایلەکە بە خێرایی سێرڤەری گیتھەب
        os.system(f'wget -q -O "movie_file" "{VIDEO_URL}"')
        
        print("📤 خەریکی بەرزکردنەوەم بۆ ناو چەناڵە تایبەتەکە...")
        
        try:
            # ناردنی وەک دۆکیومێنت (باشترە بۆ ئەوەی هەموو جۆرە قەبارە و فۆرماتێک بنێرێت)
            await app.send_document(
                chat_id=CHAT_ID,
                document="movie_file",
                caption="✅ SEBAR TV - New Content Uploaded",
                progress=lambda current, total: print(f"بۆ پێشەوە: {current * 100 / total:.1f}%")
            )
            print("✨ کارەکە بە سەرکەوتوویی کۆتایی هات!")
        except Exception as e:
            print(f"❌ هەڵە لە کاتی ناردن: {e}")

if __name__ == "__main__":
    asyncio.run(main())
