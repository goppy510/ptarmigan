# -*- coding: utf-8 -*-

import requests
import json
import sys, os
import logging
from logging import getLogger, StreamHandler, Formatter
from requests.api import head

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from user.user import Users
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from resources.jma.volcano.alert.alert import Alert

class PostAlert:

    def __init__(self):
        self.logger = getLogger("ptarmigan").getChild(os.path.basename(__file__))
        self.users = Users()
        self.user_list_id = int(self.users.get_user_list_id())
        self.public_type = self.users.get_public_type()

        self.alert = Alert()
        self.data = self.alert.data()

        # tokenファイルが無い場合は取得する
        self.token = ""
        self.token_path = os.path.dirname(os.path.abspath(__file__)) + '/token'
        if os.path.exists(self.token_path):
            self.token = self.__read_token()
        else:
            self.__update_token()


    # YMAAPのモーメントに投稿する
    def post(self):
        url = self.__get_api()
        header = self.__create_header()

        payload = self.__create_payload()
        self.logger.info("post parameter: " + str(payload))

        self.logger.debug("token:" + self.token)

        response = requests.post(url, headers=header, json=payload)
        self.logger.info("post status code: " + str(response.status_code))
        # 認証エラー時はtoken再取得して再投稿する
        if response.status_code == 401 or response.status_code == 400:
            self.__update_token()
            self.logger.debug(self.token)
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
                'text': self.__create_text()
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
        headline = self.data["headline"]
        level = self.data["level"]
        condition = self.data["condition"]
        event_time = self.data["target_time"]
        activity = self.data["activity"]
        prevention = self.data["prevention"]

        area = self.__area_list()
        return headline + "\n\n" \
            + "■ 警戒レベル ■\n" \
            + level + "\n" \
            + condition + "\n\n" \
            + "■ 発表時刻 ■\n" \
            + event_time + "\n\n" \
            + "■ 火山活動の状況及び予報警報事項 ■\n" \
            + activity + "\n\n"\
            + "■ 防災上の警戒事項等 ■\n" \
            + prevention + "\n\n" \
            + "■ 対象市町村等 ■\n" \
            + area + "\n\n" \
            + "＊＊（参考：噴火警戒レベルの説明）＊＊\n" \
            + "【レベル５（避難）】：危険な居住地域からの避難等が必要。\n" \
            + "【レベル４（避難準備）】：警戒が必要な居住地域での避難の準備、要配慮者の避難等が必要。\n" \
            + "【レベル３（入山規制）】：登山禁止や入山規制等危険な地域への立入規制等。状況に応じて要配慮者の避難準備等。\n" \
            + "【レベル２（火口周辺規制）】：火口周辺への立入規制等。\n" \
            + "【レベル１（活火山であることに留意）】：状況に応じて火口内への立入規制等。\n" \
            + "（注：避難や規制の対象地域は、地域の状況や火山活動状況により異なる）\n\n\n\n"\
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
