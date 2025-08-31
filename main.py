# main.py
from fastapi import FastAPI, Request
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent
from linebot.v3.messaging import ReplyMessageRequest, TextMessage
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io
import os

# ----------------------------
# Google Drive Config
# ----------------------------
SERVICE_ACCOUNT_FILE = "/secrets/service-account.json"
SCOPES = ['https://www.googleapis.com/auth/drive']
FILE_ID = os.environ.get("GOOGLE_DRIVE_FILE_ID")  # Google Drive file ID

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=creds)


def set_flag(value: str):
    """Update the Google Drive flag file."""
    content = f"enabled={value}".encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype="text/plain")
    drive_service.files().update(fileId=FILE_ID, media_body=media).execute()

# ----------------------------
# LINE Bot Config
# ----------------------------
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

if CHANNEL_ACCESS_TOKEN is None:
    raise ValueError("CHANNEL_ACCESS_TOKEN environment variable not set.")
if CHANNEL_SECRET is None:
    raise ValueError("CHANNEL_SECRET environment variable not set.")

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
line_bot_api = MessagingApi(ApiClient(configuration))
handler = WebhookHandler(CHANNEL_SECRET)

app = FastAPI()

# ----------------------------
# LINE Webhook Endpoint
# ----------------------------
@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")
    signature = request.headers.get("X-Line-Signature", "")
    handler.handle(body_str, signature)
    return "OK"

# ----------------------------
# Message Event Handling
# ----------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.lower()
    if text == "on":
        set_flag("true")
        reply = "CronJob is ON"
    elif text == "off":
        set_flag("false")
        reply = "CronJob is OFF"
    else:
        reply = "Available commands: on / off"
    line_bot_api.reply_message(
        reply_message_request=ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=reply)
            ]
        )
    )
