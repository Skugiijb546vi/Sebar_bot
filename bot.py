@bot.callback_query_handler(func=lambda call: True)
def action(call):
    chat_id = call.message.chat.id
    data = user_data.get(chat_id)
    if not data or not data.get("link"):
        bot.answer_callback_query(call.id, "❌ لینکەکە نەدۆزرایەوە!")
        return

    # ناردنی داتا بۆ گیتھەب
    # دڵنیابە کە ناوی فایلەکە لە گیتھەب main.yml بێت
    response = requests.post(
        f"https://api.github.com/repos/{REPO}/actions/workflows/main.yml/dispatches",
        headers={"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"},
        json={
            "ref": "main", 
            "inputs": {
                "video_url": data["link"], 
                "mode": str(call.data), 
                "audio_url": data.get("audio", "")
            }
        }
    )
    
    if response.status_code == 204:
        bot.edit_message_text(f"🚀 فەرمانی ({call.data}) نێردرا! چاودێری چەناڵەکە بکە.", chat_id, call.message.message_id)
    else:
        bot.edit_message_text(f"❌ هەڵە لە گیتھەب: {response.status_code}", chat_id, call.message.message_id)
