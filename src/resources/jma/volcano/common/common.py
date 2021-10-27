# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone
import xml.etree.ElementTree as ET
import configparser
import pprint
import time
import urllib.request
import dateutil.parser
import sys, os
import errno

class Common:

    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        config_ini_path = 'config.ini'
        # config.iniが存在しない場合は例外発生させる
        if not os.path.exists(config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        self.config_ini.read(config_ini_path, encoding='utf-8')
        # <entry>タグの位置
        self.entries_row = 8

    # for debug
    def get_debug_url(self):
        url = 'https://www.gpvweather.com/jmaxml-view.php?k=%E5%99%B4%E7%81%AB%E9%80%9F%E5%A0%B1&p=%E6%B0%97%E8%B1%A1%E5%BA%81%E5%9C%B0%E9%9C%87%E7%81%AB%E5%B1%B1%E9%83%A8&ym=2019-08&f=2019-08-07T13%3A10%3A51-a5016fd9-d433-3fc6-9aac-c12bc4edba0b.xml'
        return self.__parse_url(url)

    # 噴火速報のエントリのxmlリンクを返す
    def get_flash_url(self):
        entries = self.__get_entry()
        latest = None
        for entry in entries:
            title = entry[0].text
            if (title == self.__get_flash_title()):
                link = entry[4]
                return self.__parse_url(link.attrib['href'])


    # 噴火警報・予報のエントリのxmlリンクを返す
    def get_flash_url(self):
        entries = self.__get_entry()
        latest = None
        for entry in entries:
            title = entry[0].text
            if (title == self.__get_alert_title()):
                link = entry[4]
                return self.__parse_url(link.attrib['href'])


    # eqvolの更新時刻を取得する
    def get_update_time(self):
        eqvol_xml = self.__parse_eqvol()
        updated_raw = eqvol_xml[2].text
        return dateutil.parser.parse(updated_raw)


    # YYYY-MM-DDThh24:m:s+09:00形式の時刻をYYYY/MM/DD hh24:mm:ssにする
    def parse_time(self, date):
        dt = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        return dt.strftime('%Y/%m/%d %H:%M:%S')
    


    # YYYYMMDDhh24msをYYYY/MM/DD hh24:mm:ssに変換する
    def parse_time_str(self, date):
        return date[:4] + "/" + date[4:6] + "/" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]


    # 一覧からentry部分を取得する
    def __get_entry(self):
        eqvol_xml = self.__parse_eqvol()
        entries_row = self.entries_row
        entries = []
        for entry in eqvol_xml[entries_row:]:
            entries.append(entry)
        return entries


    # evol_urlをパースする
    def __parse_eqvol(self):
        eqvol_url = self.config_ini['DEFAULT']['eqvol_url']
        return self.__parse_url(eqvol_url)


    def __parse_url(self, url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        return ET.fromstring(xml_data)


    # 噴火速報タイトル
    def __get_flash_title(self):
        return self.config_ini['DEFAULT']['flash_title']


    # 噴火警報・予報タイトル
    def __get_alert_title(self):
        return self.config_ini['DEFAULT']['alert_title']

    