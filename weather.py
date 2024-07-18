#v0.2
import requests
import telebot
bot = telebot.TeleBot("7285941230:AAHes-JXLZceO-aKgAf6hpb_c0wJTXYCjdo")

def checkwhether(pos):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWA-35C0F6C5-330D-43D7-995D-830446D0EAD5",
        "format": "json",
        "locationName": "pos"  #地點(要以縣市來輸入) 要大寫！
    }

    headers = {
        "Authorization": "CWA-35C0F6C5-330D-43D7-995D-830446D0EAD5"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # 解析資料，取得溫度資訊
        if data and data['success']:
            records = data['records']
            if records and 'location' in records:
                location_data = records['location']
                if location_data:
                    for location in location_data:
                        # 取得溫度資訊
                        weather = location['weatherElement'][0]['time'][0]['parameter']['parameterName']
                        rain_percent=location['weatherElement'][1]['time'][0]['parameter']['parameterName']
                        MinT=location['weatherElement'][2]['time'][0]['parameter']['parameterName']
                        MaXT=location['weatherElement'][4]['time'][0]['parameter']['parameterName']
                        return(f"目前天氣是{weather}, 降雨機率是{rain_percent}, 溫度是{MinT}~{MaXT}度")
    else:
       return("獲取天氣失敗:", response.status_code)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['chk'])
def send_welcome(message):
    lst="請說你想查溫度的縣市： \n"
    bot.reply_to(message, lst)
    @bot.message_handler(func=lambda m: True)
    def weather_place(message):
	    bot.reply_to(message, checkwhether(message.text))

bot.infinity_polling()