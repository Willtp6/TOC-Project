import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, push_text_message, push_image_message, push_audio_message

import spotify_api
from user_info_manage import user_is_exists, init_user_info
import json

load_dotenv()

machine = TocMachine(
    states=["user", "state_login", "state_input_account", "state_check_account_info", "state_delete_info", "state_find_artist", "state_find_album", "state_find_track", "state_track_founded", 
            "state_help_in_user", "state_help_in_login", "state_help_in_find_artist", "state_find_in_album", "state_help_in_find_track"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state_login",
            "conditions": "is_going_to_state_login",
        },
        {
            "trigger": "advance",
            "source": "state_login",
            "dest": "state_input_account",
            "conditions": "is_account_message"
        },
        # {
        #     "trigger": "advance",
        #     "source": "state_login",
        #     "dest": "state_showSongList",
        #     "conditions": "is_going_to_state_showSongList"
        # },
        {
            "trigger": "advance",
            "source": "state_login",
            "dest": "state_find_artist",
            "conditions": "is_find_artist",
        },
        {
            "trigger": "advance",
            "source": "state_find_artist",
            "dest": "state_find_album",
            "conditions": "artist_founded",
        },
        {
            "trigger": "advance",
            "source": "state_find_album",
            "dest": "state_find_track",
            "conditions": "album_founded",
        },
        {
            "trigger": "advance",
            "source": "state_login",
            "dest": "state_check_account_info",
            "conditions": "is_check_account_info"
        },
        {
            "trigger": "advance",
            "source": "state_login",
            "dest": "state_delete_info",
            "conditions": "is_delete_user_info"
        },
        {
            "trigger": "advance",
            "source": "state_find_track",
            "dest": "state_track_founded",
            "conditions": "track_exist"
        },
        {
            "trigger": "help",
            "source": "user",
            "dest": "state_help_in_user",
        },
        {
            "trigger": "help",
            "source": "state_login",
            "dest": "state_help_in_login",
        },
        {
            "trigger": "help",
            "source": "state_find_artist",
            "dest": "state_help_in_find_artist",
        },
        {
            "trigger": "help",
            "source": "state_find_album",
            "dest": "state_help_in_find_album",
        },
        {
            "trigger": "help",
            "source": "state_find_track",
            "dest": "state_help_in_find_track",
        },
        {   
            "trigger": "go_back", 
            "source": "state_login", 
            "dest": "user"
        },
        {
            "trigger": "go_back", 
            "source": "state_input_account", 
            "dest": "state_login"
        },
        {
            "trigger": "go_back", 
            "source": "state_check_account_info",
            "dest": "state_login"
        },
        # {   "trigger": "go_back", 
        #     "source": "state_showSongList", 
        #     "dest": "user"
        # },
        {   "trigger": "go_back", 
            "source": "state_find_artist", 
            "dest": "state_login"
        },
        {   "trigger": "go_back", 
            "source": "state_find_album", 
            "dest": "state_find_artist"
        },
        {   "trigger": "go_back", 
            "source": "state_find_track", 
            "dest": "state_find_album"
        },
        {
            "trigger": "go_back", 
            "source": "state_track_founded",
            "dest": "state_find_track"
        },
        {   "trigger": "go_back", 
            "source": "state_help_in_user", 
            "dest": "user"
        },
        {
            "trigger": "go_back", 
            "source": "state_help_in_login", 
            "dest": "state_login"
        },
        {
            "trigger": "go_back", 
            "source": "state_help_in_find_artist", 
            "dest": "state_find_artist"
        },
        {
            "trigger": "go_back", 
            "source": "state_help_in_find_album", 
            "dest": "state_find_album"
        },
        {
            "trigger": "go_back", 
            "source": "state_help_in_find_track", 
            "dest": "state_find_track"
        },
        {
            "trigger": "go_back", 
            "source": "state_delete_info", 
            "dest": "user"
        },
        {
            "trigger": "back_to_menu",
            "source": ["state_login", "state_find_artist", "state_find_album", "state_find_track"],
            "dest": "user",
            "conditions": "is_going_back_to_menu"
        }
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    #get user ID (I do not know why it is user_id not userId)
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        # print(f"REQUEST BODY: \n{body}")
        response = False
        if event.message.text == "help":
            machine.help(event)
            continue
        if event.message.text == "go back" and (machine.state == "state_login" or machine.state == "state_find_artist" or machine.state == "state_find_album" or machine.state == "state_find_track"):
            machine.go_back(event)
            continue
        if event.message.text == "back to menu" and (machine.state == "state_login" or machine.state == "state_find_artist" or machine.state == "state_find_album" or machine.state == "state_find_track"):
            print("Back to Menu")
            response = machine.back_to_menu(event)
            continue
        if machine.state == 'state_find_album' and event.message.text == "show albums":
            push_text_message(event, spotify_api.show_all_album(event.source.user_id))
            continue
        elif machine.state == "state_find_track" and event.message.text == "show tracks":
            push_text_message(event, spotify_api.show_all_track(event.source.user_id))
            continue
        else:
            response = machine.advance(event)
        print(f"\nFSM STATE: {machine.state}")
        if response == False and not (machine.state == "state_find_artist" or machine.state == "state_find_album" or machine.state == "state_find_track"):
            send_text_message(event.reply_token, "please follow the instruction")
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
