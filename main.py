#v0.3 main_update: 可以在客戶輸入錯誤地點時報錯
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import telebot
import google.generativeai as genai
import random
import threading


TELEBOT_KEY = " "
CWA_KEY = " "

advise=bool(False)
where=" "
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
user_data = {}  # 用於儲存使用者的年齡和選擇
category_stages = ["上衣類", "外套", "下裝類", "套裝、正式服裝", "配飾"]
category_options = {
    "上衣類": [
        ("T恤", "T恤"),
        ("長袖", "長袖"),
        ("長袖襯衫", "長袖襯衫"),
        ("短袖襯衫", "短袖襯衫"),
        ("無袖背心", "無袖背心"),
        ("毛衣", "毛衣"),
        ("帽T", "帽T"),
        ("運動T恤", "運動T恤")
    ],
    "外套": [
        ("風衣", "風衣"),
        ("皮外套", "皮外套"),
        ("西裝外套", "西裝外套"),
        ("牛仔外套", "牛仔外套"),
        ("薄外套(防曬外套)", "薄外套"),
        ("刷毛外套", "刷毛外套"),
        ("運動外套", "運動外套"),
        ("針織外套", "針織外套")
    ],
    "下裝類": [
        ("牛仔褲", "牛仔褲"),
        ("直筒褲", "直筒褲"),
        ("喇叭褲", "喇叭褲"),
        ("工裝褲", "工裝褲"),
        ("西裝褲", "西裝褲"),
        ("短褲", "短褲"),
        ("短裙", "短裙"),
        ("長裙", "長裙"),
        ("背帶褲", "背帶褲"),
        ("運動短褲", "運動短褲"),
        ("運動長褲", "運動長褲")
    ],
    "套裝、正式服裝": [
        ("套裝", "套裝"),
        ("睡衣套裝", "睡衣套裝"),
        ("禮服", "禮服"),
        ("洋裝", "洋裝"),
        ("連身裙", "連身裙"),
        ("西裝", "西裝")
    ],
    "配飾": [
        ("棒球帽", "棒球帽"),
        ("漁夫帽", "漁夫帽"),
        ("草帽", "草帽"),
        ("太陽眼鏡", "太陽眼鏡"),
        ("毛帽", "毛帽"),
        ("貝雷帽", "貝雷帽"),
        ("圍巾", "圍巾"),
        ("手套", "手套")
    ]
}  

def call_ai(user_id):
    global user_data, schedule, where
    response2 = " "
    user_choices = user_data.get(user_id, {}).get('choices', {})
    
    with open("縣市/"+location + ".txt", 'r') as file:
        print(file)
        schedule = file.readlines()
    genai.configure(api_key="")
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
    system_instruction=f"`no-markdown`\n你是一位出門小精靈，負責幫我規劃我的行程，會依照{schedule}幫我安排行程"
    )

    model2 = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=f"`no-markdown`\n你是一位出門小精靈，負責幫我規劃我的穿搭，會幫我安排穿搭"
    )

    chat_session = model.start_chat(
    history=[]
    )
    chat_session2 = model.start_chat(
    history=[]
    )
    if advise:
        print(user_id)
        print(type(user_id))
        print(f"依照{user_data}幫我想一個穿搭+")
        if half:
            response = chat_session.send_message(f"依照{schedule}幫我規畫一個半天從{start}到{end}的行程，天氣是{sky}")
            response2 = chat_session2.send_message(f"依照{user_data[user_id]['choices']}幫{user_data[user_id]['age']}歲的人想一個要去{where}的穿搭")


            print(f"依照{schedule}幫我規畫一個從{start}到{end}的行程，天氣是{sky}，時間是半天")
            print(f"依照{user_data[user_id]['choices']}幫我想一個穿搭,要去{where}")
        else:
            response = chat_session.send_message(f"依照{schedule}幫我規畫一個整天從{start}到{end}的行程，天氣是{sky}")
            response2 = chat_session2.send_message(f"依照{user_data[user_id]['choices']}幫{user_data[user_id]['age']}歲的人想一個要去{where}的穿搭")
        return response.text + "\n\n" + response2.text
    else:
        if half:
            response = chat_session.send_message(f"依照{schedule}幫我規畫一個從{start}到{end}的行程，天氣是{sky}，時間是半天")
        else:
            response = chat_session.send_message(f"依照{schedule}幫我規畫一個從{start}到{end}的行程，天氣是{sky}，時間是一整天")
        return response.text

print("AI opennnned")
bot = telebot.TeleBot(f"{TELEBOT_KEY}")
print("BOT opened")


import threading
# 設定要編輯的訊息 ID
messages_to_edit = {}
color_box = "🔴🟠🟡🟢🔵🟣⚪️🟤🤡"
# 處理 /start 指令
@bot.message_handler(commands=['pickcolor'])
def send_welcome(message):
    bot.send_message(message.chat.id, "今日幸運色是什麼⬇")
    sent_msg = bot.send_message(message.chat.id, color_box)
    messages_to_edit[sent_msg.message_id] = sent_msg.chat.id
    
    # 啟動一個新線程來編輯訊息
    threading.Thread(target=edit_message_periodically, args=(sent_msg.chat.id, sent_msg.message_id)).start()


def edit_message_periodically(chat_id, message_id):
    #while message_id in messages_to_edit:
    global color_box
    for i in range(len(color_box)):
        color_box = color_box[1:] + color_box[:1]
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= color_box)
    color = color_box[random.randint(0, len(color_box) - 1)]
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text= color)


@bot.message_handler(commands=['GIF'])
def send_welcome(message):
    bot.send_message(message.chat.id, "GIF⬇")
    gifbox = [
        "https://media.giphy.com/media/HoizjFXoOQuNkfLH00/giphy.gif",
        "https://media.giphy.com/media/l0HlBO7eyXzSZkJri/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlK4Bl9Nr6q1rXG/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/xT1XGzUOKH8u2ZlZ7m/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26uTt2z7t3n2iEryU/giphy.gif",
        "https://media.giphy.com/media/3oEjHCWdU7F4A4xGSY/giphy.gif",
        "https://media.giphy.com/media/l0Ex5goMmnC6zJkW0/giphy.gif",
        "https://media.giphy.com/media/l0MYLSECuZsJjcs4g/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/l0MYLRCD7b6DbSyzq/giphy.gif",
        "https://media.giphy.com/media/l0HlIAGu2L9SRHcgI/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/l0HlQhQyl2Wd3a5qw/giphy.gif",
        "https://media.giphy.com/media/3o6Zt0skJ0hTGq0gR2/giphy.gif",
        "https://media.giphy.com/media/l0HlVCPVmm8yVIXcI/giphy.gif",
        "https://media.giphy.com/media/l0HlQ8eK2K7JQSJMQ/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/l0MYLRCD7b6DbSyzq/giphy.gif",
        "https://media.giphy.com/media/3o6Zt0skJ0hTGq0gR2/giphy.gif",
        "https://media.giphy.com/media/l0HlIAGu2L9SRHcgI/giphy.gif",
        "https://media.giphy.com/media/l0HlQ8eK2K7JQSJMQ/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/l0MYLRCD7b6DbSyzq/giphy.gif",
        "https://media.giphy.com/media/l0HlQhQyl2Wd3a5qw/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/26uTt2z7t3n2iEryU/giphy.gif",
        "https://media.giphy.com/media/l0HlQhQyl2Wd3a5qw/giphy.gif",
        "https://media.giphy.com/media/3oEjHCWdU7F4A4xGSY/giphy.gif",
        "https://media.giphy.com/media/l0Ex5goMmnC6zJkW0/giphy.gif",
        "https://media.giphy.com/media/3oEjHCWdU7F4A4xGSY/giphy.gif",
        "https://media.giphy.com/media/l0MYLSECuZsJjcs4g/giphy.gif",
        "https://media.giphy.com/media/l0HlIAGu2L9SRHcgI/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "https://media.giphy.com/media/l0HlPaZkLIzGfc1MQ/giphy.gif",
        "https://media.giphy.com/media/3o7aCSs7XBOEMqU3d6/giphy.gif",
        "https://media.giphy.com/media/26BRuo6sLetdllPAQ/giphy.gif",
        "https://media.giphy.com/media/3o7bu3XilJ5BOiSGic/giphy.gif",
        "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
        "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif",
        "https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif",
        "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"
    ]
    gif_url = random.choice(gifbox)
    bot.send_animation(message.chat.id, gif_url)

# TODO
# 需要 merge
def cloth_markup(user_id, category):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    choices = user_data[user_id].get('choices', {}).get(category, set())
    
    options = category_options[category]
    
    for text, data in options:
        if data in choices:
            text = f"✅ {text}"
        markup.add(InlineKeyboardButton(text, callback_data=f"{category}:{data}"))
    
    markup.add(InlineKeyboardButton(" > 完成 <", callback_data=f"{category}:done"))
    return markup


def gen_initial_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("要", callback_data="cb_yes"),
                InlineKeyboardButton("不要", callback_data="cb_no"))
    return markup

def gen_occasion_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("正式", callback_data="cb_正式"),
                InlineKeyboardButton("遊玩/聚會", callback_data="cb_遊玩/聚會"),
                InlineKeyboardButton("採購/領包裹", callback_data="cb_採購/領包裹"),
                InlineKeyboardButton("運動", callback_data="cb_運動"),
                InlineKeyboardButton("上課", callback_data="cb_上課"),
                InlineKeyboardButton("上班", callback_data="cb_上班"))
    return markup

def get_outfit(occasion, weather):
    parts = weather.split('，')
    temp_range = parts[2].split('是')[1].replace('度', '')
    min_temp, max_temp = map(int, temp_range.split('~'))
    
    wardrobe = {
        '上衣': {
            '熱': ['T恤', '短袖襯衫', '無袖背心', '運動T恤'],
            '冷': ['長袖', '長袖襯衫', '毛衣', '帽T', ]
        },
        '下裝': {
            '熱': ['牛仔褲', '直筒褲', '喇叭褲', '工裝褲', '短褲', '短裙', '背帶褲', '運動長褲', '運動短褲'],
            '冷': ['牛仔褲', '直筒褲', '喇叭褲', '工裝褲', '長裙', '運動長褲']
        },
        '套裝': {
            '熱': ['睡衣套裝','連身裙','家居服','禮服','洋裝'],
            '冷': ['睡衣套裝','連身裙','家居服','禮服','洋裝']
        },
        '鞋類': {
            '熱': ['運動鞋', '皮鞋', '涼鞋','高跟鞋','拖鞋'],
            '冷': ['運動鞋', '靴子','皮鞋', '涼鞋','拖鞋','高跟鞋']
        },
        '配飾': {
            '熱': ['棒球帽','漁夫帽','草帽','太陽眼鏡'],
            '冷': ['毛帽', '貝雷帽','棒球帽','漁夫帽','草帽','圍巾','手套']
        }
    }
    
    occasion_filter = {
        '正式': {
            '上衣': ['長袖襯衫', '短袖襯衫'],
            '下裝': ['西裝褲'],
            '套裝': ['禮服', '洋裝'],
            '鞋類': ['皮鞋', '高跟鞋'],
            '配飾': ['']
        },
        '遊玩/聚會': {
            '上衣': ['T恤', '短袖襯衫', '無袖背心', '帽T', '薄外套'],
            '下裝': ['牛仔褲', '直筒褲', '喇叭褲', '工裝褲', '休閒褲', '短褲', '裙短', '背帶褲'],
            '套裝': ['連身裙'],
            '鞋類': ['運動鞋', '涼鞋'],
            '配飾': ['帽子','太陽眼鏡','毛帽','貝雷帽','棒球帽','漁夫帽','草帽','圍巾','手套']
        },
        '採購/領包裹': {
            '上衣': ['T恤', '運動T恤', '帽T', '薄外套','毛衣'],
            '下裝': ['牛仔褲', '直筒褲', '喇叭褲', '工裝褲', '休閒褲', '短褲', '運動短褲','運動長褲'],
            '套裝': ['家居服','睡衣套裝'],
            '鞋類': ['運動鞋', '涼鞋', '拖鞋'],
            '配飾': ['帽子','棒球帽','漁夫帽','草帽','手套','圍巾']
        },
        '運動': {
            '上衣': ['運動T恤', '帽T'],
            '下裝': ['運動短褲', '運動長褲'],
            '套裝': [''],
            '鞋類': ['運動鞋'],
            '配飾': ['帽子','太陽眼鏡']
        },
        '上課': {
            '上衣': ['T恤', '薄外套'],
            '下裝': ['牛仔褲', '直筒褲', '短褲', '長裙','背帶褲','工裝褲','喇叭褲'],
            '套裝': ['連身裙'],
            '鞋類': ['運動鞋', '涼鞋','靴子'],
            '配飾': ['帽子','圍巾']
        },
        '上班': {
            '上衣': ['長袖襯衫', '短袖襯衫'],
            '下裝': ['牛仔褲', '直筒褲'],
            '套裝': [],
            '鞋類': ['皮鞋'],
            '配飾': []
        }
    }

    temperature_type = '熱' if max_temp > 27 else '冷'

    available_clothes = {
        '上衣': [item for item in wardrobe['上衣'][temperature_type] if item in occasion_filter[occasion]['上衣']],
        '下裝': [item for item in wardrobe['下裝'][temperature_type] if item in occasion_filter[occasion]['下裝']],
        '套裝': [item for item in wardrobe['套裝'][temperature_type] if item in occasion_filter[occasion]['套裝']],
        '鞋類': [item for item in wardrobe['鞋類'][temperature_type] if item in occasion_filter[occasion]['鞋類']],
        '配飾': [item for item in wardrobe['配飾'][temperature_type] if item in occasion_filter[occasion]['配飾']]
    }

    outfit = []
    if available_clothes['上衣'] and available_clothes['下裝']:
        outfit.append(random.choice(available_clothes['上衣']))
        outfit.append(random.choice(available_clothes['下裝']))
    elif available_clothes['套裝']:
        outfit.append(random.choice(available_clothes['套裝']))

    outfit.append(random.choice(available_clothes['鞋類']))
    if available_clothes['配飾']:
        outfit.append(random.choice(available_clothes['配飾']))

    return ' + '.join(outfit)

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
    global advise
    
    user_id = call.from_user.id

    if call.data=="True" or call.data=="False":
        if call.data=="True":
            half=1
        else:
            half=0
        bot.send_message(temp, f"{check_weather(call.data, location)}", reply_markup=end_markup())
    elif call.data=="sure":
        entergoal=True
        bot.send_message(temp, "是否需要推薦穿搭?", reply_markup=gen_initial_markup())
    elif call.data=="giveup":
        entergoal=True
        bot.send_message(temp, f"已關閉本次使用，謝謝您的使用💗🤖")
    elif call.data == "cb_yes":
        #bot.answer_callback_query(call.id, "請問今天要去場合是哪裡呢?", show_alert=True)
        bot.send_message(call.message.chat.id, "請選擇今天要去的場合:", reply_markup=gen_occasion_markup())
    elif call.data == "cb_no":
        bot.send_message(temp, f"本次行程是由{start}出發到{end},即將為您規劃行程💗🤖☆*: .｡. o(≧▽≦)o .｡.:*☆")
        bot.send_message(temp, f"{call_ai(user_id)}", parse_mode="Markdown")
    elif call.data.startswith("cb_"):
        advise=True
        where = call.data[3:]
        bot.send_message(temp, f"本次行程是由{start}出發到{end},即將為您規劃行程💗🤖☆*: .｡. o(≧▽≦)o .｡.:*☆")
        bot.send_message(temp, f"{call_ai(user_id)}", parse_mode="Markdown")
        #bot.answer_callback_query(call.id, f"您選擇的場合是: {occasion}", show_alert=True)
    elif call.data in positions:
        if entergoal:
            start=call.data
            entergoal=False
            bot.send_message(temp, f"{check_weather('True', start)}")
            bot.send_message(temp, "請問您的目的地為何呢👾",reply_markup=contry_markup())
            bot.send_message(temp, f"若要選目的地可以直接按按鈕(可重複使用)🔁")
        else:
            location=call.data
            end=location
            bot.send_message(temp, f"請問您{location}想去半天還是整天呢🤔🔎",reply_markup=gen_markup())
    category, data = call.data.split(":")
    if data == "done":
        current_stage_index = category_stages.index(category)
        if current_stage_index == len(category_stages) - 1:
            choices = {stage: list(user_data[user_id]['choices'][stage]) for stage in category_stages}
            
            # 創建格式化的選擇文字
            formatted_choices = "你的衣櫃有\n"
            for stage, items in choices.items():
                if items:  # 只有當該類別有選擇時才添加
                    formatted_choices += f"{stage}：{' / '.join(items)}\n"
                else:
                    formatted_choices += f"{stage}：無\n"
            bot.edit_message_text(formatted_choices, call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, "註冊完成 !\n我們會根據你衣櫃中的衣服幫尼進行最適合今天的穿搭，也會推薦行程及告訴你當天的天氣呦 (*´∀`)/\n使用 /schedule 來規劃行程")
            # user_data.pop(user_id, None) <-- 幹
        else:
            next_stage = category_stages[current_stage_index + 1]
            bot.edit_message_text(f"你的衣櫃有哪些{next_stage}（可多選）呢~：", call.message.chat.id, call.message.message_id, reply_markup=cloth_markup(user_id, next_stage))
    
   
    else:
        if category not in user_data[user_id]['choices']:
            user_data[user_id]['choices'][category] = set()
        if data in user_data[user_id]['choices'][category]:
            user_data[user_id]['choices'][category].remove(data)
        else:
            user_data[user_id]['choices'][category].add(data)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=cloth_markup(user_id, category))
        bot.answer_callback_query(call.id)
        
def check_weather(half:bool, pos: str):

    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": f"{CWA_KEY}",
        "format": "json",
        "locationName": f"{pos}"  #地點(要以縣市來輸入) 要大寫！
    }

    headers = {
        "Authorization": f"{CWA_KEY}"
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
    user_id = message.from_user.id
    global entergoal
    global temp 
    global location
    global start 
    global end
    global user_data
    if message.text == "/schedule":
        if entergoal:
            temp=message.chat.id
            location=message.text
            start=location
            bot.send_message(message.chat.id, "請問您的出發地在哪呢🤔🔎",reply_markup=contry_markup())
    elif message.text == "/start":
        user_data[user_id] = {
            'age': None,
            'choices': {category: set() for category in category_stages}
        }
        bot.send_message(message.chat.id, "哈囉我是出門小精靈(・ε・)\n請問你的年齡是?")

    elif user_id in user_data and user_data[user_id]['age'] is None:
        try:
            age = int(message.text)
            if 1 <= age <= 110:
                user_data[user_id]['age'] = age
                bot.send_message(message.chat.id, "這裡是性別多元友善衣櫃~(*´∀`)~♥")
                bot.send_message(message.chat.id, f"你的衣櫃有哪些{category_stages[0]}呢~（可多選）：", reply_markup=cloth_markup(user_id, category_stages[0]))
            else:
                bot.reply_to(message, "請輸入有效的年齡數字歐~~（1-110歲）。")
        except ValueError:
            bot.reply_to(message, "請輸入有效的年齡數字歐。")
    print(111, user_data)

bot.infinity_polling()