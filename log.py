# @Time : 2022/10/8 22:33 
# @Author : kang
# @File : log.py
# @Desc: 日志模块
import datetime
import logging
from logging import handlers

# 定义logger
console_logger = logging.getLogger('console_logger')
file_logger = logging.getLogger('file_logger')

console_handler = logging.StreamHandler()
file_handler = handlers.TimedRotatingFileHandler(
    filename='/var/log/yiban/daka.log',
    # filename='daka.log',
    when='midnight',
    interval=1,
    atTime=datetime.datetime(year=2022, month=10, day=7),
)

fmt = logging.Formatter(
    fmt='%(asctime)s| %(levelname)-8s | %(name)-10s | %(pathname)-50s | %(lineno)-5d | %(funcName)-15s |  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(fmt)
console_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)
file_handler.setLevel(logging.DEBUG)

console_logger.setLevel(logging.DEBUG)
console_logger.addHandler(console_handler)
file_logger.setLevel(logging.DEBUG)
file_logger.addHandler(file_handler)
