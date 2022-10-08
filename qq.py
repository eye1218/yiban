# @Time : 2022/9/4 11:24 
# @Author : kang
# @File : qq.py
import requests

report_url = 'http://8.210.0.124:5700'


def send_group_message(remind_message: str, group_id: str):
    send_url = f'http://8.210.0.124:5700/send_group_msg?group_id={group_id}&message={remind_message}&auto_escape=false'
    requests.get(send_url)


def send_private_message(qq: str, message: str):
    url = f'{report_url}/send_msg?message_type=private&user_id={qq}&&message={message}'
    requests.get(url)


if __name__ == '__main__':
    send_private_message('1454147447', 'hello')
