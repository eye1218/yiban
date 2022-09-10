# @Time : 2022/9/4 11:24 
# @Author : kang
# @File : qq.py
import requests

report_url = 'http://8.210.0.124:5700'
import log

logger = log.get_file_logger()


def send_private_message(qq: str, message: str):
    url = f'{report_url}/send_msg?message_type=private&user_id={qq}&&message={message}'
    res = requests.get(url)
    logger.info(f'QQ消息已发送, {res.content.decode()}')


if __name__ == '__main__':
    send_private_message('1454147447', 'hello')
