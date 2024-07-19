#v0.4 main_update : 人性化更新
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot

bot = telebot.TeleBot("TGAPI")

print("BOT opened")
temp=int(0)
positions=["宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","屏東縣"]
calling=False
location=" "
entergoal=True

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add( InlineKeyboardButton("半天", callback_data="True"),
                InlineKeyboardButton("整天", callback_data="False"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global temp
    global location
    print(f"{temp}{location}")
    bot.send_message(temp, f"{check_now_weather(call.data, location)}")

def check_now_weather(half:bool, pos: str):

    positions=["宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","屏東縣"]
    right_pos=0
    for i in positions:
        if i==pos:
            right_pos=1
            break
    
    if right_pos==0:
        return(f"獲取天氣失敗 : 可能是輸入的地點有誤")  #最後可能要改 可以直接拔

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWA-35C0F6C5-330D-43D7-995D-830446D0EAD5",
        "format": "json",
        "locationName": f"{pos}"  #地點(要以縣市來輸入) 要大寫！
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
                        if half == "True":
                            print("true")   
                            weather = location['weatherElement'][0]['time'][0]['parameter']['parameterName']
                            rain_percent=location['weatherElement'][1]['time'][0]['parameter']['parameterName']
                            MinT=location['weatherElement'][2]['time'][0]['parameter']['parameterName']
                            intro=location['weatherElement'][3]['time'][0]['parameter']['parameterName']
                            MaXT=location['weatherElement'][4]['time'][0]['parameter']['parameterName']
                            return(f"目前{pos}的天氣是{weather}，降雨機率是{rain_percent}，溫度是{MinT}~{MaXT}度，給人的感覺是 {intro}")
                        else:
                            print("false")
                            weather = location['weatherElement'][0]['time'][0]['parameter']['parameterName']
                            rain_percent=location['weatherElement'][1]['time'][0]['parameter']['parameterName']
                            MinT=location['weatherElement'][2]['time'][0]['parameter']['parameterName']
                            intro=location['weatherElement'][3]['time'][0]['parameter']['parameterName']
                            MaXT=location['weatherElement'][4]['time'][0]['parameter']['parameterName']
                            weather2 = location['weatherElement'][0]['time'][1]['parameter']['parameterName']
                            rain_percent2=location['weatherElement'][1]['time'][1]['parameter']['parameterName']
                            MinT2=location['weatherElement'][2]['time'][1]['parameter']['parameterName']
                            intro2=location['weatherElement'][3]['time'][1]['parameter']['parameterName']
                            MaXT2=location['weatherElement'][4]['time'][1]['parameter']['parameterName']
                            return(f"目前{pos}的天氣是{weather}，降雨機率是{rain_percent}，溫度是{MinT}~{MaXT}度, 給人的感覺是 {intro}\n晚一點{pos}的天氣是{weather2}，降雨機率是{rain_percent2}，溫度是{MinT2}~{MaXT2}度，給人的感覺是 {intro2}")
    else:
       return(f"獲取天氣失敗: {response.status_code}, 可能是輸入的地點有誤")

@bot.message_handler(func=lambda message:True) 
def get_pos(message):
    if message.text in positions:
        global entergoal
        global temp 
        global location
        if entergoal:
            temp=message.chat.id
            location=message.text
            i="True"
            entergoal=False
            bot.send_message(message.chat.id, f"{check_now_weather(i, location)}")
            bot.send_message(message.chat.id, "請問您想去哪裡呢")
        else:
            location=message.text
            bot.send_message(message.chat.id, "請問您想去半天還是整天呢",reply_markup=gen_markup())
            bot.send_message(message.chat.id, "若欲放棄出去遊玩請按下--> /home \n若是想換目的地請直接輸出新的目的地")
    if message.text == "/start":
        bot.reply_to(message, "可以在輸入縣市後,再確認是半天或整天給該地點的天氣以及合適的行程以及穿搭 👾🐣 \n目前僅有包含以下縣市 \n宜蘭縣，花蓮縣，臺東縣，澎湖縣，金門縣，連江縣，臺北市，新北市，桃園市，臺中市，臺南市，高雄市，基隆市，新竹縣，新竹市，苗栗縣，彰化縣，南投縣，雲林縣，嘉義縣，嘉義市，屏東縣\n支援的指令有 /start : 使用說明 | /debug : 報錯說明 | /home : 關閉本次規劃")
    if message.text == "/debug":
        bot.reply_to(message, "可能是您的輸入有問題，台跟臺要多加注意喔!🤔") 
    if message.text == "/home":
        entergoal=True
        bot.reply_to(message, "已關閉本次使用，謝謝您的使用") 

    

bot.infinity_polling()