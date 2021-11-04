# -*- coding: utf-8 -*-

import requests
import json
import sys, os
import logging
from logging import getLogger, StreamHandler, Formatter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from user.user import Users
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from resources.jma.volcano.newsflash.newsflash import Newsflash

class PostNewsFlash:

    def __init__(self):
        self.logger = getLogger("ptarmigan").getChild(os.path.basename(__file__))
        self.users = Users()
        self.user_list_id = int(self.users.get_user_list_id())
        self.public_type = self.users.get_public_type()

        self.newsflash = Newsflash()
        self.data = self.newsflash.data()

        # tokenファイルが無い場合は取得する
        self.token = ""
        self.token_path = os.path.dirname(os.path.abspath(__file__)) + '/token'
        if os.path.exists(self.token_path):
            self.token = self.__read_token()
        else:
            self.__update_token()

    # データが存在するかチェック
    def has_data(self):
        self.logger.info(self.data)
        if self.data:
            return True
        return False

    # YMAAPのモーメントに投稿する
    def post(self):
        url = self.__get_api()
        header = self.__create_header()

        payload = self.__create_payload()
        self.logger.info("post parameter: " + str(payload))

        self.logger.debug("token:" + self.token)

        try:
            response = requests.post(url, headers=header, json=payload)
            self.logger.info("post status code: " + str(response.status_code))
            # 認証エラー時はtoken再取得して再投稿する
            if response.status_code == 401:
                self.__update_token()
                self.logger.debug("Authorized Error. token: " + self.token)
                self.post()
            elif response.status_code == 200 or response.status_code == 201:
                self.logger.info("newsflash request successed. status_code: " + str(response.status_code))
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return False


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
                # 内容
                'text': self.__create_text()
                # 公開・非公開情報
                ,'public_type': self.public_type
                ,'allow_users_list': {
                    'id': self.user_list_id
                }
                ,'images': []
            }
        }
        return payload


    # 噴火速報の本文を作成する
    def __create_text(self):
        # xmlのデータを整形したやつ
        mountain = self.data["name"]
        event_time = self.data["target_time"]
        area = self.__area_list()
        return mountain + "で " + event_time + " 頃、噴火が発生しました。\n\n" \
            + "下記の地域の方々は今後の情報にご注意ください。\n\n" \
            + area + "\n\n\n\n" \
            + "※この記事は当該ユーザー作成のプログラムによる自動投稿です。"


    # bodyに記入する地域をstringで羅列する
    def __area_list(self):
        city = self.data["city"]
        city_name = []
        for i in city:
            city_name.append(i["name"])
        target_city = ""
        for name in city_name:
            target_city += name + "\n"
        return target_city


    # tokenアップデート
    def __update_token(self):
        self.token = self.users.get_token()
        self.__write_token(self.token)


    # tokenを読み出す
    def __read_token(self):
        with open(self.token_path, mode='r') as f:
            fread = f.read()
            return fread


    # tokenを書き出す
    def __write_token(self, token):
        with open(self.token_path, mode='w') as f:
            f.write(token)
