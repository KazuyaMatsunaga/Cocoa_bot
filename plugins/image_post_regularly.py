# coding: utf-8

import random
import json
import requests
from slacker import Slacker
import os
import sys
sys.path.append('..')
import config

# 以下定期的に画像を投稿する処理
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