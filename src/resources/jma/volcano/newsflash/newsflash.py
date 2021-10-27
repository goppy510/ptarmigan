# -*- coding: utf-8 -*-

import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import urllib.request
import sys, os
import logging
from logging import getLogger, StreamHandler, Formatter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.common import Common

class Newsflash:

    def __init__(self):
        self.logger = getLogger("ptarmigan").getChild(os.path.basename(__file__))
        self.common = Common()
        self.xml_url = self.common.get_flash_url()
        self.pref_row = 2
        self.area_row = 3

    def data(self):
        result = {}

        # テスト用
        # if (self.xml_url == None):
        #     return False
        parsed = self.common.get_debug_url()

        # <Control>
        control = parsed[0]
        # ステータス
        result["status"] = control[2].text

        # <Head>
        head = parsed[1]
        # タイトル
        head_title = head[0].text
        # 発生時刻
        target_datetime = head[2].text
        parsed_time = self.common.parse_time(target_datetime)
        result["target_time"] = parsed_time

        # <Body>
        body = parsed[2]

        # 山名
        volcanoinfo = body[0]
        item = volcanoinfo[0]
        areas = item[2]
        name = areas[0][0].text
        result["name"] = name

        # 対象エリア
        volcanoinfo2 = body[1]
        item = volcanoinfo2[0]
        areas2 = item[1]
        result["city"] = []
        for city in areas2:
            city_name = city[0].text
            city_code = city[1].text

            result["city"].append({
                "name": city_name,
                "code": city_code,
            })
        return result
