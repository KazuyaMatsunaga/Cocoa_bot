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

@respond_to('ランチ食べたい')
def lunch(message):
    message.react('heart')
    message.send('ご注文はランチですか？\n')
    message.reply('現在地を教えてね！')

    @listen_to(r'[^0-9]')
    def place_question(message):
        place = message.body['text'] # メッセージを取り出す
        message.reply(place + 'だね！料理のジャンルは何にしようか？')
        @listen_to(r'[^0-9]')
        def genre_question(message):
            genre = message.body['text'] # メッセージを取り出す
            message.reply(genre + 'だね！予算はどれくらいがいいかな？\n' + '下の中から好きなのを選んでね！(番号で答えてね)\n')
            message.send('1:～500円\n')
            message.send('2:501～1000円\n')
            message.send('3:1001～1500円\n')
            @listen_to(r'[1-3]')
            def budget_question(message):
                budget_number = message.body['text'] # メッセージを取り出す
                message.reply('OK！ちょっと待っててね！')
                # ここから検索処理

                # 予算コードを取得
                hotpepper_gourmet_budget_url = "http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=" + HOTPEPPER_GOURMET_APIKEY + "&" + "format=" + "json"
                return_gourmet_budget = requests.get(hotpepper_gourmet_budget_url).json()

                print(return_gourmet_budget)

                gourmet_budget_list = return_gourmet_budget['results']['budget']

                if budget_number == "1":
                    gourmet_budget_code = gourmet_budget_list[0]['code']
                elif budget_number == "2":
                    gourmet_budget_code = gourmet_budget_list[1]['code']
                elif budget_number == "3":
                    gourmet_budget_code = gourmet_budget_list[2]['code']

                print(gourmet_budget_code)
                
                # リクエストURL
                hotpepper_gourmet_url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=" + HOTPEPPER_GOURMET_APIKEY + "&" + "keyword=" + place + " " + genre + "&" + "budget=" + gourmet_budget_code+ "&" + "lunch=" + "1" + "&" + "format=" + "json" + "&" + "type=" + "lite"

                return_gourmet = requests.get(hotpepper_gourmet_url).json()

                print(return_gourmet)

                choiced_gourmet_name = None
                choiced_gourmet_urls = None

                if return_gourmet['results']['shop'] != []:
                    return_gourmet_list = return_gourmet['results']['shop']
                    choiced_gourmet = random.choice(return_gourmet_list)
                    choiced_gourmet_name = choiced_gourmet['name']
                    choiced_gourmet_urls = choiced_gourmet['urls']['pc']
                # ここまで検索処理

                if (choiced_gourmet_name is not None) and (choiced_gourmet_urls is not None):
                    message.reply('このお店はどうかな？\n' + choiced_gourmet_name + "\n" + choiced_gourmet_urls)
                else:
                    message.reply('いいお店が見つからなかった...ごめんね...')
                
                @respond_to('ありがとう')
                def thank_you_response(message):
                    imagefile_list = ['plugins/images/lunch/lunch_1.gif',
                                    'plugins/images/lunch/lunch_2.gif',
                                    'plugins/images/lunch/lunch_3.gif',
                                    'plugins/images/lunch/lunch_4.gif',
                                    'plugins/images/lunch/lunch_5.gif',
                                    'plugins/images/lunch/lunch_6.gif',
                                    'plugins/images/lunch/lunch_7.gif'] # 画像ファイルのパスを代入
                    filepath = os.path.abspath(random.choice(imagefile_list))
                    files = {'file': open(filepath, 'rb')}
                    param = {
                        'token':TOKEN,
                        'channels':CHANNEL,
                        'title': "img"
                    }
                    message.react('heart')
                    message.reply('うん！どういたしまして！')
                    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)
