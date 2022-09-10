# @Time : 2022/9/4 11:14 
# @Author : kang
# @File : daka.py
import datetime
import os

import healthy_report
from qq import send_private_message
import log

logger = log.get_file_logger()


def daka():
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'student.txt'), 'r', encoding='utf8') as f:
        while True:
            line = f.readline()
            if line:
                try:
                    info = line.split()
                    username = info[0]
                    password = info[1]
                    qq = info[2]
                    if healthy_report.daka(username, password):
                        send_private_message(qq, f'打卡成功 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    else:
                        send_private_message(qq,
                                             f'打卡失败，请手动打卡 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                except Exception as e:
                    with open('/tmp/daka.log', 'a', encoding='utf8') as f:
                        logger.error(f'学生：{line[0]} 打卡过程发生异常发生，异常信息：{str(e)}')
                        f.write(str(e))
            else:
                break


if __name__ == '__main__':
    daka()
