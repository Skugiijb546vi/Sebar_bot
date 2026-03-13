import os
import asyncio
from pyrogram import Client

API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")
# ئایدی چەناڵەکەت وەک خۆی
CHAT_ID = -1003503643297

async def main():
    if not VIDEO_URL:
        print("❌ هیچ لینکێک دابین نەکراوە!")
        return

    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print(f"🔗 بەستنەوە بە چەناڵی: {CHAT_ID}")
        
        try:
            # ئەم بەشە زۆر گرنگە: بۆتەکە ناچار دەکات زانیاری چەناڵەکە وەربگرێت
            chat = await app.get_chat(CHAT_ID)
            print(f"✅ چەناڵەکە دۆزرایەوە: {chat.title}")
            
            print("📥 دەستکرا بە داگرتنی فایل لە سێرڤەری گیتھەب...")
            os.system(f'wget -q -O "movie_file.mp4" "{VIDEO_URL}"')
            
            print("📤 خەریکی ناردنم بۆ ناو چەناڵەکە...")
            await app.send_document(
                chat_id=CHAT_ID,
                document="movie_file.mp4",
                caption="✅ SEBAR TV - New Movie Uploaded",
                progress=lambda current, total: print(f"بۆ پێشەوە: {current * 100 / total:.1f}%")
            )
            print("✨ کارەکە بە سەرکەوتوویی کۆتایی هات!")
            
        except Exception as e:
            print(f"❌ کێشەیەک ڕوویدا: {e}")
            if "Peer id invalid" in str(e):
                print("💡 ئامۆژگاری: یەک نامە لە چەناڵەکەوە فۆروارد بکە بۆ لای بۆتەکە، پاشان ئەمە کار دەکات.")

if __name__ == "__main__":
    asyncio.run(main())
