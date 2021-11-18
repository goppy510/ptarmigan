# -*- coding: utf-8 -*-

import sys, os
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter
import dateutil.parser

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from post_newsflash import PostNewsFlash
from post_alert import PostAlert
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from resources.jma.volcano.common.common import Common

class Mains():
    def __init__(self):
        self.time_path         = sys.path.append(os.path.dirname(os.path.abspath(__file__))) + '/timelog/updated_time.txt'
        self.news_path         = sys.path.append(os.path.dirname(os.path.abspath(__file__))) + '/xml_url/newsflash_xml.txt'
        self.alert_path        = sys.path.append(os.path.dirname(os.path.abspath(__file__))) + '/xml_url/alert_xml.txt'
        self.common            = Common()
        self.latest_news_xml   = None
        self.local_news_xml    = None
        self.latest_alert_xml  = None
        self.local_alert_xml   = None
        self.local_time        = None
        self.updated_time      = None

        # ログ周り
        self.logger = getLogger("ptarmigan")
        self.logger.setLevel(logging.DEBUG)
        self.handler_format = Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        self.stream_handler = StreamHandler()
        self.stream_handler.setLevel(logging.DEBUG)
        self.stream_handler.setFormatter(self.handler_format)
        self.file_handler = FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/log/ptarmigan.log', 'a')
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.handler_format)
        self.logger.addHandler(self.stream_handler)
        self.logger.addHandler(self.file_handler)

    def execute(self):
        self.update_time = self.common.get_update_time()
        self.__execute_news()
        self.__execute_alert()

    def __execute_news(self):
        # 最終更新時刻が記録されたファイルの存在チェック
        if (os.path.exists(self.time_path)):
            # 書かれている時刻を読み込む
            self.__read_time_log()
            # xmlのエンドポイントが書かれたファイルがあれば読み込む
            if (os.path.exists(self.news_path)):
                self.__read_news_xml()
            if (self.updated_time > self.local_time):
                if (self.local_news_xml != self.latest_news_xml):
                    self.__post_newsflash()
        else:
            self.__post_newsflash()
            self.__write_time_log()

    def __execute_alert(self):
        # 最終更新時刻が記録されたファイルの存在チェック
        if (os.path.exists(self.time_path)):
            # 書かれている時刻を読み込む
            self.__read_time_log()
            # xmlのエンドポイントが書かれたファイルがあれば読み込む
            if (os.path.exists(self.alert_path)):
                self.__read_alert_xml()
            if (self.updated_time > self.local_time):
                if (self.local_alert_xml != self.latest_alert_xml):
                    self.__post_alert()
        else:
            self.__post_alert()
            self.__write_time_log()


    # 最後に記録した時間が書かれたファイルを読み込む
    def __read_time_log(self):
        with open(self.time_path, mode='r') as f:
            lt = f.read()
            self.local_time = dateutil.parser.parse(lt)

    # xmlの時刻が更新されていた場合、その時刻をファイルに書き込む
    def __write_time_log(self):
        with open(self.time_path, mode='w') as f:
            updated_time = self.updated_time
            updated_time_str = updated_time.strftime('%Y/%m/%d %H:%M:%S%z')
            f.write(updated_time_str)

    # 噴火速報に関する情報の最新xmlを読み込む
    def __read_news_xml(self):
        with open(self.news_path, mode='r') as f:
            self.local_news_xml = f.read()

    # 噴火速報に関する情報の最新xmlを書き込む
    def __write_news_xml(self):
        with open(self.news_path, mode='w') as f:
            latest_xml_url = self.latest_news_xml
            f.write(latest_xml_url)

    # 噴火警報・予報の最新xmlを読み込む
    def __read_alert_xml(self):
        with open(self.alert_path, mode='r') as f:
            self.local_alert_xml = f.read()

    # 噴火警報・予報の最新xmlを書き込む
    def __write_alert_xml(self):
        with open(self.alert_path, mode='w') as f:
            latest_xml_url = self.latest_alert_xml
            f.write(latest_xml_url)


    # 最後に記録した時間が書かれたファイルを読み込む
    def __read_time_log(self):
        with open(self.time_path, mode='r') as f:
            self.local_time = f.read()
            self.local_time = dateutil.parser.parse(self.local_time)

    # 噴火速報の処理実行
    def __post_newsflash(self):
        self.logger.info("---噴火速報処理 start---")
        post_newsflash = PostNewsFlash()
        if post_newsflash.has_data():
            post_newsflash.post()
        else:
            self.logger.warning("newsflash: データが無いので実行しません。")
        self.logger.info("---噴火速報処理 end---")

    # 噴火警報・予報の処理実行
    def __post_alert(self):
        self.logger.info("---噴火警報・予報 start---")
        post_alert = PostAlert()
        if post_alert.has_data():
            post_alert.post()
        else:
            self.logger.warning("alert: データが無いので実行しません。")
        self.logger.info("---噴火警報・予報 end---")


if __name__ == "__main__":
    main = Mains()
    main.execute()
