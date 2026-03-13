import os
import asyncio
from pyrogram import Client

# وەرگرتنی زانیارییەکان لە گیتھەبەوە
API_ID = 22697853
API_HASH = "4801319a0aeb52817bc01d3cc60bb245"
BOT_TOKEN = "8524581086:AAGDZmzCO9ib3faKk8XvV3NfeLbwRNsvWhY"
VIDEO_URL = os.environ.get("VIDEO_URL")
# ئایدی گروپەکە لێرە جێگیر کراوە
CHAT_ID = -1003503643297

async def main():
    async with Client("sebar_worker", API_ID, API_HASH, bot_token=BOT_TOKEN) as app:
        print("📥 دەستکرا بە داگرتنی فیلمەکە لە سێرڤەری گیتھەب...")
        
        # داگرتنی ڤیدیۆکە بە خێراییەکی زۆر
        os.system(f'wget -q -O video.mp4 "{VIDEO_URL}"')
        
        print("📤 خەریکی ناردنم بۆ ناو گروپە تایبەتەکە...")
        
        # ناردنی ڤیدیۆکە بۆ گروپەکە
        await app.send_video(
            chat_id=CHAT_ID,
            video="video.mp4",
            caption="🎬 فیلمی نوێ بارکرا بۆ ناو داتابەیس\n\n✅ SEBAR TV Project",
            progress=lambda current, total: print(f"بۆ پێشەوە: {current * 100 / total:.1f}%")
        )
        print("✨ پیرۆزە! فیلمەکە بە سەرکەوتوویی گەیشتە ناو گروپەکە.")

if __name__ == "__main__":
    asyncio.run(main())
