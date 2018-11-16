# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import random
import json
import requests
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

@respond_to('もふもふ')
def mention_func(message):
    message.reply('もふもふ！☆') # メンション
    message.react('mofumofu')

@respond_to('ブス')
def mention_func(message):
    message.send('(`0言0́*)<ヴェアアアアアアアアアアアアアア')
    message.react('broken_heart')

@listen_to('ランチ食べたい')
def listen_func(message):
    message.send('ご注文はランチですか？')
    message.react('heart')
    lunch_list = ["一平ソバ","東館食堂","旧スエヒロ食堂","松屋","がんま","高園","モンスン"]
    text = '今日は' + random.choice(lunch_list) + 'に行こう！！☆'
    message.reply(text)
