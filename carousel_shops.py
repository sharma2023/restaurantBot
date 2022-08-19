from linebot.models import FlexSendMessage
import json, requests

def get_shops(hotkey, latitude, longitude, range, order_jun, genre, next):
    hotpepper_url = f"https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key={hotkey}&lat={latitude}&lng={longitude}&range={range}&order={order_jun}&genre={genre}&count=100&format=json"
    hotpepper_res = json.loads(requests.get(hotpepper_url).text)
    dis = ""
    tosend = []
    for i in hotpepper_res["results"]["shop"]:
        dis += i["name"]
        dis += "\n"
        sample = {
            "type": "bubble",
            "size": "kilo",
            "hero": {
                "type": "image",
                "url": i["photo"]["pc"]["m"], 
                "size": "full",
                "aspectMode": "cover",
                "aspectRatio": "320:213"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": i["name"],
                    "weight": "bold",
                    "size": "sm",
                    "wrap": True
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": i["address"],
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "お店を予約",
                        "uri": i["urls"]["pc"]
                    },
                    "style": "primary",
                    "color": "#ff0000",
                }
            ],
            "paddingAll": "10px"
            }
        }
        tosend.append(sample)
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
            "type": "carousel",
            "contents": tosend
        }
    )
    return flex_message