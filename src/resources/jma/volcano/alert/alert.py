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

# 噴火警報・予報を取得するクラス

class Alert:

    def __init__(self):
        self.logger = getLogger("ptarmigan").getChild(os.path.basename(__file__))
        self.common = Common()
        self.xml_url = self.common.get_alert_url()
        self.pref_row = 2
        self.area_row = 3

    def data(self):
        result = {}

        if (self.xml_url == None):
            return False
        parsed = self.xml_url

        # <Control>
        control = parsed[0]
        # ステータス
        result["status"] = control[2].text

        # <Head>
        head = parsed[1]

        # 発生時刻
        target_datetime = head[2].text
        parsed_time = self.common.parse_time(target_datetime)
        result["target_time"] = parsed_time

        # レベル
        headline = head[8]
        information = headline[1]
        item = information[0]
        kind = item[0]
        # 入山規制レベル
        result["level"] = kind[0].text
        # 引き上げ・継続等の状態のこと
        result["condition"] = kind[2].text
        

        # <Body>
        body = parsed[2]

        # 山名
        volcanoinfo = body[0]
        item = volcanoinfo[0]
        areas = item[2]
        area = areas[0]
        name = area[0].text
        result["name"] = name
        # 経緯度・標高
        result["coordinate"] = area[2].text

        # 対象エリア 気象・地震・火山情報／市町村等
        volcanoinfo2 = body[2]
        item = volcanoinfo2[0]
        areas2 = item[2]
        result["city"] = []
        for city in areas2:
            city_name = city[0].text
            city_code = city[1].text

            result["city"].append({
                "name": city_name,
                "code": city_code,
            })
        
        volcanoinfocontent = body[3]
        headline = volcanoinfocontent[0].text
        activity = volcanoinfocontent[1].text
        prevention = volcanoinfocontent[2].text
        result["headline"] = headline
        result["activity"] = activity
        result['prevention'] = prevention

        return result
