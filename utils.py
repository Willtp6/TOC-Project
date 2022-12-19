import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, AudioSendMessage, ImageSendMessage

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

import json

def send_text_message(reply_token, text):

    line_bot_api = LineBotApi(channel_access_token)
    if isinstance(text, str):
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text)])
        return "OK"
    msg_num = len(text)
    if msg_num == 1:
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text[0])])
    elif msg_num == 2:
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text[0]), TextSendMessage(text=text[1])])
    elif msg_num == 3:
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text[0]), TextSendMessage(text=text[1]), TextSendMessage(text=text[2])])
    elif msg_num == 4:
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text[0]), TextSendMessage(text=text[1]), TextSendMessage(text=text[2]), TextSendMessage(text=text[3])])
    else:
        line_bot_api.reply_message(reply_token, [TextSendMessage(text=text[0]), TextSendMessage(text=text[1]), TextSendMessage(text=text[2]), TextSendMessage(text=text[3]), TextSendMessage(text=text[4])])

    return "OK"

def push_text_message(event, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(event.source.user_id, TextSendMessage(text=text))

def push_image_message(event, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    image_message = ImageSendMessage(original_content_url=img_url, preview_image_url=img_url)
    line_bot_api.push_message(event.source.user_id, image_message)

def push_audio_message(event, audio_url):
    line_bot_api = LineBotApi(channel_access_token)
    audio_message = AudioSendMessage(original_content_url=audio_url, duration=30000)
    line_bot_api.push_message(event.source.user_id, audio_message)

def send_audio_message(event):
    print("audio")
    line_bot_api = LineBotApi(channel_access_token)
    audio_message = AudioSendMessage(original_content_url="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", duration=30000)
    line_bot_api.reply_message(event.reply_token, audio_message)