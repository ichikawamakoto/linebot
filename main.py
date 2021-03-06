# coding:utf-8
from flask import Flask, request, abort
import os
import re
import datetime
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback")
def webhook():
    return "hello webhook!"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return
    Msa = ["へー","それでそれで？","で？","すごいすごい","大丈夫？","なんでやねん"]
    resMessage = random.choice(Msa)
    reqMessage = event.message.text
    if re.match(r"こんにちは",reqMessage):
        resMessage = "こんにちは"
    elif re.match(r"日付",reqMessage):
        date_now = datetime.datetime.now()
        resMessage = date_now.strftime('%Y年%m月%d日')
    elif re.match(r"時間",reqMessage):
        time_now = datetime.datetime.now()
        resMessage = time_now.strftime("%H:%M:%S")
    elif re.match(r".*ありがとう",reqMessage) or re.match(r".*ありがとうございます",reqMessage):
        resMessage = "どういたしまして"
    elif re.match(r".*褒めて",reqMessage):
        homeru = ["すごいやん","やるやん","よくやった","君は天才だ！"]
        resMessage = random.choice(homeru)
    elif re.match(r"高輪のパスワード",reqMessage):
        resMessage = "dp968604"
    elif re.match(r".*googleアカウント",reqMessage) or re.match(r".*グーグルアカウント"):
        resMessage = "dppts0044"


    line_bot_api.reply_message(
        event.reply_token,
        # TextSendMessage(text=event.message.text))
        TextSendMessage(text=resMessage))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)