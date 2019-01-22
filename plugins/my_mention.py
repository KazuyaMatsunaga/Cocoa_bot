# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import random
import json
import requests
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

@respond_to('もふもふ')
def mention_func(message):
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
def mention_func(message):
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
def listen_func(message):
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

#以下定期的に画像を投稿する処理
#def image_post_job():
#   imagefile_list = ['plugins/images/mofumofu/mofumofu_1.gif',
#                      'plugins/images/mofumofu/mofumofu_2.gif',
#                      'plugins/images/mofumofu/mofumofu_3.gif',
#                      'plugins/images/mofumofu/mofumofu_4.gif',
#                      'plugins/images/mofumofu/mofumofu_5.gif',
#                      'plugins/images/lunch/lunch_1.gif',
#                      'plugins/images/lunch/lunch_2.gif',
#                      'plugins/images/lunch/lunch_3.gif',
#                      'plugins/images/lunch/lunch_4.gif',
#                      'plugins/images/lunch/lunch_5.gif',
#                      'plugins/images/lunch/lunch_6.gif',
#                      'plugins/images/lunch/lunch_7.gif'] # 画像ファイルのパスを代入
#    filepath = os.path.abspath(random.choice(imagefile_list))
    # 画像の投稿
#    files = {'file': open(filepath, 'rb')}
#    param = {
#        'token':TOKEN,
#        'channels':CHANNEL,
#        'title': "img"
#    }
#    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)

#AM7:30に画像を投稿
#schedule.every().day.at("7:30").do(image_post_job)

#while True:
#   schedule.run_pending()
#    time.sleep(1)
