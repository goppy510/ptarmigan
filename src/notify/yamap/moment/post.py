# -*- coding: utf-8 -*-

import requests
import json
import sys, os

from ..user import Users

class Posts():

    def __init__(self):
        self.users = Users.Users()
        self.token = self.users.get_token()
        self.user_list_id = self.users.get_user_list_id()

    # YMAAPのモーメントに投稿する
    def post(self):
        url = self.__get_api()
        header = self.__create_header()
        payload = self.__create_payload()
        requests.post(url, headers=header, json=payload)


    # モーメント投稿用のエンドポイント
    def __get_api(self):
        url = 'https://api.yamap.com/journals/'
        return url

    # トークンを入れたヘッダーを取得
    def __create_header(self):
        header = {
            'Authorization': 'Bearer ' + self.token
        }
        return header

    # 投稿するデータ用のペイロードを作成
    def __create_payload(self):
        payload = {
            'journal': {
                'text': self.__get_text()
                ,'public_type': self.user_list_id
                ,'allow_user_list': {
                    'id': self.user_list_id
                }
                ,'images': []
            }
        }
        return payload
    
    def __get_text(self):
        # xmlのデータを整形したやつ
