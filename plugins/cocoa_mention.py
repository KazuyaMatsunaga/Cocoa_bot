# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import random
import json
import requests
from datetime import datetime
from slacker import Slacker
import os
import sys
sys.path.append('..')
import config
import schedule
import time

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
TOKEN = config.TOKEN
CHANNEL = config.CHANNEL
C_NAME = config.CHANNEL_NAME

# ここから自然対話用パラメータ
appId = config.appId
APIKEY = config.DOCOMO_COMMUNICATION_APIKEY

# リクエストボディ(JSON形式)
send_data = {
    "language": "ja-JP",
    "botId": "Chatting",
    "appId": appId,
    "voiceText": "",
    "appSendTime": ""
    }

# リクエストヘッダ
headers = {'Context-type': 'application/json'}

# リクエストURL
url = "https://api.apigw.smt.docomo.ne.jp/naturalChatting/v1/dialogue?APIKEY={}".format(APIKEY)
# ここまで自然対話用パラメータ

@respond_to('もふもふ')
def mofumofu(message):
    message.reply('もふもふ！☆') # メンション
    message.react('mofumofu')
    imagefile_list = ['plugins/images/mofumofu/mofumofu_1.gif',
                      'plugins/images/mofumofu/mofumofu_2.gif',
                      'plugins/images/mofumofu/mofumofu_3.gif',
                      'plugins/images/mofumofu/mofumofu_4.gif',
                      'plugins/images/mofumofu/mofumofu_5.gif'] # 画像ファイルのパスを代入
    filepath = os.path.abspath(random.choice(imagefile_list))
    # 画像の投稿
    files = {'file': open(filepath, 'rb')}
    param = {
        'token':TOKEN,
        'channels':CHANNEL,
        'title': "img"
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

@respond_to('ブス')
def busu(message):
    message.send('(`0言0́*)<ヴェアアアアアアアアアアアアアア')
    message.react('broken_heart')
    imagefile_path = 'plugins/images/veaa/veaa.gif' # 画像ファイルのパスを代入
    filepath = os.path.abspath(imagefile_path)
    # 画像の投稿
    files = {'file': open(filepath, 'rb')}
    param = {
        'token':TOKEN,
        'channels':CHANNEL,
        'title': "img"
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

@listen_to('ランチ食べたい')
def lunch(message):
    message.send('ご注文はランチですか？')
    message.react('heart')
    lunch_list = ["一平ソバ","東館食堂","旧スエヒロ食堂","松屋","がんま","高園","モンスン"]
    text = '今日は' + random.choice(lunch_list) + 'に行こう！！☆'
    message.reply(text)
    imagefile_list = ['plugins/images/lunch/lunch_1.gif',
                      'plugins/images/lunch/lunch_2.gif',
                      'plugins/images/lunch/lunch_3.gif',
                      'plugins/images/lunch/lunch_4.gif',
                      'plugins/images/lunch/lunch_5.gif',
                      'plugins/images/lunch/lunch_6.gif',
                      'plugins/images/lunch/lunch_7.gif'] # 画像ファイルのパスを代入
    filepath = os.path.abspath(random.choice(imagefile_list))
    # 画像の投稿
    files = {'file': open(filepath, 'rb')}
    param = {
        'token':TOKEN,
        'channels':CHANNEL,
        'title': "img"
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

# 毎日AM8:00になるとランダムでGIFを投稿するコード
def regularly_image_post():
    # 画像を投稿する処理
    def image_post_job():
        imagefile_list = ['plugins/images/mofumofu/mofumofu_1.gif',
                        'plugins/images/mofumofu/mofumofu_2.gif',
                        'plugins/images/mofumofu/mofumofu_3.gif',
                        'plugins/images/mofumofu/mofumofu_4.gif',
                        'plugins/images/mofumofu/mofumofu_5.gif',
                        'plugins/images/lunch/lunch_1.gif',
                        'plugins/images/lunch/lunch_2.gif',
                        'plugins/images/lunch/lunch_3.gif',
                        'plugins/images/lunch/lunch_4.gif',
                        'plugins/images/lunch/lunch_5.gif',
                        'plugins/images/lunch/lunch_6.gif',
                        'plugins/images/lunch/lunch_7.gif'] # 画像ファイルのパスを代入
        filepath = os.path.abspath(random.choice(imagefile_list))
        # 画像の投稿
        files = {'file': open(filepath, 'rb')}
        param = {
            'token':TOKEN,
            'channels':CHANNEL,
            'title': "img"
        }
        requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

    # AM8:00に画像を投稿
    schedule.every().day.at("8:00").do(image_post_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 自然対話コード
@respond_to(r'.*')
def chatting(message):
    send_text = message.body['text'] # メッセージを取り出す

    send_data['voiceText'] = send_text
    # 送信時間を取得
    send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    send_data['appSendTime'] = send_time

    # メッセージを送信
    r = requests.post(url, data=json.dumps(send_data), headers=headers)
    # レスポンスデータから返答内容を取得
    return_data = r.json()
    return_message = return_data['systemText']['expression']
    # 返答を投稿
    message.send(return_message)
