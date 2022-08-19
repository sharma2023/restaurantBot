import json
import requests
import pprint

# url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=e84ee8c933bda3ff&lat=34.67&lng=135.52&range=5&order=4&format=json"
url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=35.6859559,139.6947&key=AIzaSyDJk-_Uvj1M9gUb90TeFcGoZxAM9RqVuHc"
res = requests.get(url)
result = json.loads(res.text)

print(result["results"][0]["formatted_address"])

# pprint.pprint(result["results"]["shop"][1]["name"])

# for i in range(len(result["results"]["shop"])):
#     print(result["results"]["shop"][i]["urls"]["pc"])
#     print(result["results"]["shop"][i]["name"])
#     print(result["results"]["shop"][i]["logo_image"])
#     print(result["results"]["shop"][i]["photo"]["pc"]["m"])


# print(len(result["results"]["shop"]))
# with open("sample.json", "w", encoding="utf-8") as outfile:
    # outfile.write(json.dumps(result, indent=4, ensure_ascii=False))