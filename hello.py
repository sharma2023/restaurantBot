from flask import Flask, redirect, request, abort
# Webhookイベントを受け取るHandler
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
# 様々なメッセージオブジェクト
from linebot.models import (
    MessageEvent, TextMessage, LocationMessage, TextSendMessage, QuickReplyButton, QuickReply,  MessageAction, ImageMessage, LocationAction, TemplateSendMessage, CarouselTemplate, CarouselColumn, PostbackAction, CarouselTemplate, URIAction
)

# HTTP通信と解析を行うライブラリ
from bs4 import BeautifulSoup
import requests
import json
import time

app = Flask(__name__)
port = "5000"
line_bot_api = LineBotApi("UrGPE+tEAYzYC2HxOmYpVragfJdVgqObcGQEnRp4fXxJjN/q4NcxYvc78GmtOcHIwEucjROYJ4X4/wUioy7PItOHuMCDwE0YbYJUtRNeRTDTSmR62K+9UzfMjVmc9v/ah6n6OYn4cz4mlq1ttAHXhQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("8710ea53808686bc2143e5718364153a")
# places_api_key = "AIzaSyDJk-_Uvj1M9gUb90TeFcGoZxAM9RqVuHc"
# places_api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/"
# google_map_url = "https://www.google.com/maps/search/?api=1"


def hotpepper():
    url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=e84ee8c933bda3ff&lat=34.67&lng=135.52&range=5&order=4"
    res = requests.get(url)
    

def make_carousel(thumbnail_image_url,shop_name,like,map_url,user_ratings_total):
    column = CarouselColumn(
            thumbnail_image_url=thumbnail_image_url,
            title=shop_name,
            text=f"いいね👍 :{like}\n評価数 :{user_ratings_total}",
            actions=[URIAction(label='mapで表示',uri=map_url)]
            )
    return column


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def reply_message(event):
    global sessions, selectable_food
    if not event.source.user_id in sessions.keys():
        sessions[event.source.user_id] = {"flag":False,"food":None,"place":None}
  
@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    latitude = event.message.latitude
    longitude = event.message.longitude
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"{latitude},{longitude}")
    )

if __name__ == "__main__":
    app.run(port=port, debug=True)