import os
import asyncio
from pyrogram import Client

# زانیارییەکان
API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8436877565:AAEG6We8wKSh1RXG85uI_VA5w-6Sswu7YLo"
VIDEO_URL = os.environ.get("VIDEO_URL")

# بەکارهێنانی یوزەرنەیم بۆ شکاندنی بەربەستی Peer ID
CHAT_ID = "@ajsjajaauai" 

async def main():
    if not VIDEO_URL:
        print("❌ هیچ لینکێک نییە بۆ داگرتن!")
        return

    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print(f"🔗 هەوڵدان بۆ ناسینەوەی چەناڵی: {CHAT_ID}")
        
        try:
            # دۆزینەوەی چەناڵەکە
            chat = await app.get_chat(CHAT_ID)
            print(f"✅ چەناڵەکە دۆزرایەوە: {chat.title}")
            
            print("📥 دەستکرا بە داگرتنی فایل لە سێرڤەری گیتھەب...")
            # داگرتنی فایلەکە (ناوی دەنێین movie.mp4)
            os.system(f'wget -q -O "movie.mp4" "{VIDEO_URL}"')
            
            print("📤 خەریکی ناردنی فیلمەکە بۆ ناو چەناڵەکە...")
            # ناردنی فیلمەکە
            await app.send_document(
                chat_id=CHAT_ID,
                document="movie.mp4",
                caption="✅ فیلمەکە بە سەرکەوتوویی لە ڕێگەی گیتھەبەوە بارکرا\n\n🎬 SEBAR TV",
                progress=lambda current, total: print(f"بۆ پێشەوە: {current * 100 / total:.1f}%")
            )
            print("✨ پیرۆزە! کارەکە بە سەرکەوتوویی کۆتایی هات.")
            
        except Exception as e:
            print(f"❌ هەڵەیەک ڕوویدا: {e}")

if __name__ == "__main__":
    asyncio.run(main())
