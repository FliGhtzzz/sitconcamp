#v1.0 TG X AI = 天氣 + 行程
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import google.generativeai as genai


def call_ai():
    global schedule
    with open("縣市/"+location + ".txt", 'r') as file:
        schedule = file.readlines()
    genai.configure(api_key="AI-TOKEN")
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 5000,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction=f"你完全不會markdown語法而且你是一位出門小精靈,負責幫我規劃我的行程和穿搭,會依照{schedule}幫我安排行程"
    )

    chat_session = model.start_chat(
    history=[
    ]
    )
    if half:
        response = chat_session.send_message(f"依照{schedule}幫我規畫一個從{start}到{end}的行程,天氣是{sky},時間是半天")
    else:
        response = chat_session.send_message(f"依照{schedule}幫我規畫一個從{start}到{end}的行程,天氣是{sky},時間是一整天")
    return response.text
print("AI opennnned")
bot = telebot.TeleBot("TGTOKEN")
print("BOT opened")

schedule=" "
temp=int(0)
calling=False
location=" "
entergoal=True
start=" "
end=" "
positions=["宜蘭縣","花蓮縣","臺東縣","澎湖縣","金門縣","連江縣","臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹縣","新竹市","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","嘉義市","屏東縣"]
sky=""
half=bool(0)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add( InlineKeyboardButton("半天", callback_data="True"),
                InlineKeyboardButton("整天", callback_data="False"))
    return markup

def end_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add( InlineKeyboardButton("確定行程", callback_data="sure"),
                InlineKeyboardButton("放棄行程", callback_data="giveup"))
    return markup

def contry_markup():
    global positions
    markup=InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(len(positions)//3):
        i*=3
        markup.add(InlineKeyboardButton(positions[i], callback_data=positions[i]),
                   InlineKeyboardButton(positions[i+1], callback_data=positions[i+1]),
                   InlineKeyboardButton(positions[i+2], callback_data=positions[i+2]))
    markup.add(InlineKeyboardButton(positions[21], callback_data=positions[21]))
    return markup
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global entergoal
    global start 
    global end
    global temp
    global half
    global location
    print(f"{temp}{location}")
    if call.data=="True" or call.data=="False":
        if call.data=="True":
            half=1
        else:
            half=0
        bot.send_message(temp, f"{check_weather(call.data, location)}",reply_markup=end_markup())
        bot.send_message(temp, f"重選目的地可以直接按按鈕(可重複使用)")
    elif call.data=="sure":
        entergoal=True
        bot.send_message(temp, f"本次行程是由{start}出發到{end},即將為您規劃行程")
        bot.send_message(temp, f"{call_ai()}")

    elif call.data=="giveup":
        entergoal=True
        bot.send_message(temp, f"已關閉本次使用，謝謝您的使用")
    else:
        if entergoal:
            start=call.data
            entergoal=False
            bot.send_message(temp, f"{check_weather('True', start)}")
            bot.send_message(temp, "請問您的目的地為何呢",reply_markup=contry_markup())
            bot.send_message(temp, f"若要選目的地可以直接按按鈕(可重複使用)")
        else:
            location=call.data
            end=location
            bot.send_message(temp, f"請問您{location}想去半天還是整天呢",reply_markup=gen_markup())
        
def check_weather(half:bool, pos: str):

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
        global sky
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
                            sky=f"目前{pos}的天氣是{weather}，降雨機率是{rain_percent}，溫度是{MinT}~{MaXT}度，給人的感覺是 {intro}"
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
                            sky=f"目前{pos}的天氣是{weather}，降雨機率是{rain_percent}，溫度是{MinT}~{MaXT}度, 給人的感覺是 {intro}\n晚一點{pos}的天氣是{weather2}，降雨機率是{rain_percent2}，溫度是{MinT2}~{MaXT2}度，給人的感覺是 {intro2}"
                            return(f"目前{pos}的天氣是{weather}，降雨機率是{rain_percent}，溫度是{MinT}~{MaXT}度, 給人的感覺是 {intro}\n晚一點{pos}的天氣是{weather2}，降雨機率是{rain_percent2}，溫度是{MinT2}~{MaXT2}度，給人的感覺是 {intro2}")
    else:
       return(f"獲取天氣失敗: {response.status_code}, 可能是輸入的地點有誤")

@bot.message_handler(func=lambda message:True) 
def get_pos(message):
    if message.text == "/schedule":
        global entergoal
        global temp 
        global location
        global start 
        global end
        if entergoal:
            temp=message.chat.id
            location=message.text
            start=location
            bot.send_message(message.chat.id, "請問您的出發地在哪呢",reply_markup=contry_markup())
    if message.text == "/start":
        bot.reply_to(message, "可以在輸入 /schedule 後，輸入出發地及目的地，告訴您該行程的天氣以及幫您排合適的行程以及穿搭 👾🐣 \n目前僅有包含以下縣市 \n宜蘭縣，花蓮縣，臺東縣，澎湖縣，金門縣，連江縣，臺北市，新北市，桃園市，臺中市，臺南市，高雄市，基隆市，新竹縣，新竹市，苗栗縣，彰化縣，南投縣，雲林縣，嘉義縣，嘉義市，屏東縣\n")
    

    

bot.infinity_polling()