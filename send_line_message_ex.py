import os
from linebot.v3.messaging import MessagingApi
from linebot.v3.messaging.models import PushMessageRequest, TextMessage
from linebot.v3.messaging.api_client import ApiClient
from linebot.v3.messaging.configuration import Configuration
# 讀取 LINE Token 並建立 API 實體
line_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
configuration = Configuration()
configuration.access_token = line_token
api_client = ApiClient(configuration=configuration)
line_bot_api = MessagingApi(api_client)

# 設定聊天室 ID（使用者 ID 或群組 ID）
user_ids = [
    "Uef360c65c710f997a64c572b40fd8251",  # 你的 userId
    "Ud0a8ffa8ef11b32b6c3ff24d79cc85af"   # 群組或另一個 userId
]

# Excel 檔案的 GitHub 下載連結
repo_owner = "klamath608"
repo_name = "line_ex"
file_path = "reports/除權息資料排序結果.xlsx"
file_url = f"https://github.com/{repo_owner}/{repo_name}/raw/main/{file_path}"

# 訊息內容
message_text = f"📊 您好~本週除權息預告報表已更新，請點擊下載：\n👉 {file_url}"

# 推送訊息
for uid in user_ids:
    request = PushMessageRequest(
        to=uid,
        messages=[TextMessage(text=message_text)]
    )
    line_bot_api.push_message(request)
