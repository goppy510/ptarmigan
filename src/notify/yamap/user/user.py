# -*- coding: utf-8 -*-

import configparser
import requests
import json
import sys, os
import errno
import logging
from logging import getLogger, StreamHandler, Formatter

class Users:
    
    def __init__(self):
        self.logger = getLogger("ptarmigan").getChild(os.path.basename(__file__))
        self.config_ini = configparser.ConfigParser()
        config_ini_path = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
        # config.iniが存在しない場合は例外発生させる
        if not os.path.exists(config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        self.config_ini.read(config_ini_path, encoding='utf-8')

    
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
                'email': self.__get_email(),
                'password': self.__get_password()
            }
        }
        res = requests.post(url, json=payload)
        self.logger.info("user login status: " + str(res.status_code))
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

