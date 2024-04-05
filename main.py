from flask import Flask, request, jsonify,abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import json

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = 'vIoR1hbMadmys/MHLEjPGnEF6VVIZV7h3YvlkuXHxO9yp7omafUdXtphmd1CSe1FnOziLM3n/pATy4tynAPuamHGRUzQ4P/C5hsMKOjljU3xBhuzTARpSb5vkQ0fOPnxtIyaQstVpxq1awKL42j9EQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '9f176dc65193f5c70c1627560d814c1e'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 定義一個全域變數用來存儲最新的溫溼度資訊
temperature={}
humidity={}

# 接收esp8266_json檔案
@app.route('/data', methods=['POST'])
def receive_data():
    global temperature
    global humidity
    data = request.get_json()
    temperature= data ['temperature']
    humidity=data['humidity']
    print(f"Received data    溫度：{temperature}°C，濕度：{humidity}%")
    return "Data received successfully"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = str(event.message.text)
    global temperature
    global humidity
    # 如果收到訊息，回覆最新的溫溼度資訊
    if msg=="現在溫濕度是多少":
        reply_message = f"溫度：{temperature}°C，濕度：{humidity}%"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    elif msg=="危險指數是多少":
        dangerIndex=temperature+humidity*0.8
        if dangerIndex > 40:
            reply_message=f'危險指數為{dangerIndex}，不建議外出活動'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        elif dangerIndex  >  35:
            reply_message=f'危險指數為{dangerIndex}，避免激烈運動，注意水分補充'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        elif dangerIndex  <=  35:
            reply_message=f'危險指數為{dangerIndex}，可正常活動，注意水分補充'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    else:
            reply_message=f'很抱歉，我無法知道您的意思，你可以問我"現在溫濕度是多少"或是"危險指數是多少"'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入，你可以問我"現在溫濕度是多少"或是"危險指數是多少"')
    line_bot_api.reply_message(event.reply_token, message)
        
@app.route("/")
def test_XX():
    return "<p>監聽中</p>"

if __name__ == '__main__':    
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port,debug=True)

# # 提供時間溫度濕度資料
# @app.route('/data', methods=['GET'])
# def get_data():
#     data_files = os.listdir('data')
#     data = []
#     for file_name in data_files:
#         with open(os.path.join('data', file_name), 'r') as f:
#             data.append({
#                 'file_name': file_name,
#                 'content': f.read()
#             })
#     return jsonify(data)

# yiyangteacher
# @app.route('/h/<h>')
# def get_humidity(h):
#     return f'humidity : {escape(h)}!'

# @app.route('/t/<t>')
# def get_temperature(t):
#     return f'temperature : {escape(t)}!'

# db=[]
# @app.route("/th")
# def getTemperatureHumidity():
#     global db
#     args = request.args
#     if args.get("temperature") is not None and args.get("humidity") is not None :
#        db += [[args.get("temperature"), args.get("temperature")]]
       
#     return db