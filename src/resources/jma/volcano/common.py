# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone
import xml.etree.ElementTree as ET
import configparser
import pprint
import time
import urllib.request
import dateutil.parser

class Common:
    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read('config.ini', encoding='utf-8')
        self.entries_row = 8


    # 任意のタイトルに応じたタイトルがあるエントリのxmlリンクを返す
    def get_detail_url(self, target_title):
        entries = self.__get_entry()
        latest = None
        for entry in entries:
            title = entry[0].text
            if (title == target_title):
                link = entry[4]
                latest = link.attrib['href']
                break
        return latest


    # eqvolの更新時刻を取得する
    def get_update_time(self):
        eqvol_xml = self.__parse_eqvol()
        updated_raw = eqvol_xml[2].text
        updated_time = dateutil.parser.parse(updated_raw)
        return updated_time


    def parse_url(self, url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        return root


    # YYYY/MM/DDThh24:m:s+09:00形式の時刻をYYYY/MM/DD hh24:mm:ssにする
    def parse_time(self, date):
        dt = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        return dt


    # YYYYMMDDhh24msをYYYY/MM/DD hh24:mm:ssに変換する
    def parse_time_str(self, date):
        dt = date[:4] + "/" + date[4:6] + "/" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]
        return dt


    # evol_urlをパースする
    def __parse_eqvol(self):
        eqvol_url = self.config_ini['DEFAULT']['eqvol_url']
        return self.parse_url(eqvol_url)


    # 一覧からentry部分を取得する
    def __get_entry(self):
        eqvol_xml = self.__parse_eqvol()
        entries_row = self.__entries_row
        entries = []
        for entry in eqvol_xml[entries_row:]:
            entries.append(entry)
        return entries
