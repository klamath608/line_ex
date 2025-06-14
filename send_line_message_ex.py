import os
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.messaging.models import PushMessageRequest, TextMessage

# 讀取 LINE Token 並建立 API 實體
line_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
configuration = Configuration(access_token=line_token)
line_bot_api = MessagingApi(configuration)

# 設定聊天室 ID（使用者 ID 或群組 ID）
user_ids = [
    "Cbfedfeb371931301daa1e9d15c3c68f3",  # 你的 userId
    "Ud0a8ffa8ef11b32b6c3ff24d79cc85af"   # 群組或另一個 userId
]

# Excel 檔案的 GitHub 下載連結
repo_owner = "你的 GitHub 使用者名稱"
repo_name = "你的 Repo 名稱"
file_path = "reports/報表.xlsx"
file_url = f"https://github.com/{repo_owner}/{repo_name}/raw/main/{file_path}"

# 訊息內容
message_text = f"📊 本週報表已更新，請點擊下載：\n👉 {file_url}"

# 推送訊息
for uid in user_ids:
    request = PushMessageRequest(
        to=uid,
        messages=[TextMessage(text=message_text)]
    )
    line_bot_api.push_message(request)
