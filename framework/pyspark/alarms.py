#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author: zhengchubin
# @time: 2024/12/31 10:41
# @function:
import base64
import hashlib
import hmac
import time
import urllib.parse
import requests


class DingDingAlarm:
    def __init__(self,
                 secret='',
                 webhook="https://oapi.dingtalk.com/robot/send?access_token="):
        self.webhook = webhook
        self.secret = secret
        self.headers = {'Content-Type': 'application/json;charset=utf-8'}

    @staticmethod
    def generate_sign(timestamp, secret):
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def post_msg(self, text, telephone="15521147129"):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    telephone
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        timestamp = str(round(time.time() * 1000))
        sign = self.generate_sign(timestamp, self.secret)
        api_url = self.webhook + f"&timestamp={timestamp}&sign={sign}"
        response = requests.post(api_url, json=json_text, headers=self.headers)
        print(response.json())


if __name__ == '__main__':
    ding_alarm = DingDingAlarm()
    ding_alarm.post_msg("hi", "")
