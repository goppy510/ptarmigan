# -*- coding: utf-8 -*-

import configparser
import requests
import json
import sys, os

class Users:
    
    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read('config.ini', encoding='utf-8')

    
    # トークン取得
    def get_token(self):
        res = self.login()
        return res['user']['token']
    
    # ユーザーリストID取得
    def get_user_list_id(self):
        return self.config_ini['DEFAULT']['user_list_id']
    
    # 公開ステータス取得
    def get_public_type(self):
        return self.config_ini['DEFAULT']['public_type']

    # ログインする
    def login(self):
        url = self.__get_login_url()
        payload = {
            'session': {
                'email': self.email,
                'password': self.password
            }
        }
        res = requests.post(url, json=payload)
        return res.json()
    
    # ログインURLを取得する
    def __get_login_url(self):
        url = 'https://api.yamap.com/session'
        return url

    # email取得
    def __get_email(self):
        return self.config_ini['DEFAULT']['email']

    # パスワード取得
    def __get_password(self):
        return self.config_ini['DEFAULT']['password']

