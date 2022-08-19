from re import template
from flask import Flask, request, abort
from distance import buttons_template_message
from carousel_t import carousel_template_message
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
import requests, json, os
from orderjun import order_template_message

load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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


hot = os.getenv("HOTPEPPER_API")
latitude, longitude = 0.0, 0.0
range = 0
order_jun = 0
genre = ""
place_name = ""

@handler.add(MessageEvent)
def handle_message(event):
    try:
        global latitude, longitude, place_name
        latitude = event.message.latitude
        longitude = event.message.longitude
        locres = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=35.6859559,139.6947&key=AIzaSyDJk-_Uvj1M9gUb90TeFcGoZxAM9RqVuHc&language=ja")
        # print(json.)
        locresult = json.loads(locres.text)
        locresponse = locresult["results"][0]["formatted_address"]
        place_name = locresponse
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"位置を設定しました。\n{locresponse}\n\n続きまして、他の設定を行ってください\n使えるコマンド: \n@loc - 位置を設定\n@kyori - 範囲を設定\n@jun - 表示の順を設定\n@genre - ジャンルを設定\n@place - 設定の場所を表示\n@setting - 設定を表示\n\n@show - 店を表示")
        )
    except:
        text=event.message.text
        ptext=text.strip(" ")
        global range
        global genre
        global order_jun
        if ptext.startswith("はじめる"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='''使えるコマンド：\n@loc - 位置を設定\n@kyori - 範囲を設定\n@jun - 表示の順を設定\n@genre - ジャンルを設定\n@place - 設定の場所を表示\n@setting - 設定を表示\n\n@show - 店を表示''')
            )
        
        if ptext.startswith("@loc"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"位置情報を送信してください")
            )
        elif ptext.startswith("@kyori"):
            line_bot_api.reply_message(
                event.reply_token,
                buttons_template_message
            )
        elif ptext.startswith("@jun"):
            line_bot_api.reply_message(
                event.reply_token,
                order_template_message
            )
        elif ptext.startswith("@genre"):
            line_bot_api.reply_message(
                event.reply_token,
                carousel_template_message
            )
        elif ptext.startswith("3キロ以内"): range = 5
        elif ptext.startswith("2キロ以内"): range = 4
        elif ptext.startswith("1キロ以内"): range = 3
        elif ptext.startswith("500メートル以内"): range = 2
        elif ptext.startswith("店名かな順"): order_jun = 1
        elif ptext.startswith("ジャンルコード順"): order_jun = 2
        elif ptext.startswith("小エリアコード順"): order_jun = 3
        elif ptext.startswith("おススメ順"): order_jun = 4
        elif ptext.startswith("ラーメン"): genre = "G013"
        elif ptext.startswith("居酒屋"): genre = "G001"
        elif ptext.startswith("中華"): genre = "G007"
        elif ptext.startswith("和食"): genre = "G004"
        elif ptext.startswith("韓国料理"): genre = "G017"
        elif ptext.startswith("イタリアン・フレンチ"): genre = "G006"
        elif ptext.startswith("カフェ・スイーツ"): genre = "G014"
        elif ptext.startswith("お好み焼き・もんじゃ"): genre = "G016"
        elif ptext.startswith("バー・カクテル"): genre = "G012"
        elif ptext.startswith("洋食"): genre = "G005"
        elif ptext.startswith("@setting"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"おすすめのTOP10店。\nの設定の場所は\n{place_name}\nです。変えたい場合は、@locを使ってください")
            )
        elif latitude != 0.0 and range != 0 and order_jun != 0 and genre != "":
            hotpepper_url = f"https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={hot}&lat={latitude}&lng={longitude}&range={range}&order={order_jun}&genre={genre}&format=json"
            hotpepper_res = json.loads(requests.get(hotpepper_url).text)
            dis = ""
            for i in hotpepper_res["results"]["shop"]:
                dis += i["name"]
                dis += "\n"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=dis)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="その用語わかりません\nもしくは設定が終わっていません。")
            )
        # if latitude!=0.0 and ptext.startswith("@show"):
        #     hotpepper_url = f"https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={hot}&lat={latitude}&lng={longitude}&range={range}&order=4&format=json"
        #     hotpepper_res = json.loads(requests.get(hotpepper_url).text)
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=hotpepper_res["results"]["shop"][0]["name"])
        #     )
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text=hotpepper_res["results"]["shop"][1]["name"])
        #     )
        
        # print(range)

# line_bot_api.reply_message(
#                 event.reply_token,
#                 carousel_template_message
#             )


# commands
# @loc - asks for location
# @kyori - asks for kyori
# @

if __name__ == "__main__":
    app.run()