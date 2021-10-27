# -*- coding: utf-8 -*-

import sys, os
import logging
from logging import getLogger, StreamHandler, FileHandler, Formatter

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from post_newsflash import PostNewsFlash


def main():
    # ログ周り
    logger = getLogger("ptarmigan")
    logger.setLevel(logging.DEBUG)
    handler_format = Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(handler_format)
    file_handler = FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/log/ptarmigan.log', 'a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    logger.info("---噴火速報処理 start---")
    post_newsflash = PostNewsFlash()
    post_newsflash.post()
    logger.info("---噴火速報処理 end---")
    


if __name__ == "__main__":
    main()