# @Time : 2022/9/3 17:16 
# @Author : kang
# @File : login.py
import base64
import json
import re
import requests

import log
from student import Student

login_url = 'http://202.203.16.42//login/Login.htm'
token_url = 'http://202.203.16.42/'
xm_url = 'http://202.203.16.42/syt/zzapply/queryxmqks.htm?type=xsfxtwjc'

logger = log.get_file_logger()


def get_token() -> str:
    """
    获取token
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    res = requests.get(token_url, headers=headers)
    res.raise_for_status()
    cookie = res.headers.get('Set-Cookie')
    token = re.findall(r'token=(.*?);', cookie)
    if len(token) == 1:
        logger.info(f'获取token成功, token:{token[0]}')
        return token[0]
    else:
        logger.error('获取token失败')
        return ''


def login(student: Student) -> str:
    """
    登录，返回cookie
    :param student: 学生信息
    :return: cookie
    """
    if student.password is None:
        student.password = '@c' + student.username
    username = base64.b64encode(student.username.encode())
    password = base64.b64encode(student.password.encode())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    data = {
        'username': username,
        'password': password,
        'verification': '',
        'token': student.token,
    }
    res = requests.post(login_url, headers=headers, data=data)
    res.raise_for_status()
    cookie = res.headers.get('Set-Cookie')
    session_id = re.findall(r'JSESSIONID=(.*?);', cookie)
    if len(session_id) == 1:
        logger.info(f'用户：{student.username}获取session_id成功，session_id: {session_id[0]}')
        return session_id[0]
    else:
        logger.info(f'用户：{student.username}获取session_id失败')
        return ''


def get_xm_id(student: Student):
    """
    获取学生标识
    :param student: 学生信息
    :return: xm_id
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Cookie': f'JSESSIONID={student.session_id}; username={student.username}; menuVisible=1',
    }
    data = {
        'pageIndex': 0,
        'pageSize': 20,
        'sortField': '',
        'sortOrder': '',
    }
    res = requests.post(xm_url, headers=headers, data=data)
    res.raise_for_status()
    res = json.loads(res.content.decode())
    data = res.get('data')
    xm_id = [x.get('id') for x in data if x.get('sfksq')]
    if len(xm_id):
        logger.info(f'用户：{student.username} 已获取xmid, xmid: {str(xm_id)}')
    else:
        logger.warning(f'用户：{student.username} 未获取xmid')
    return xm_id


if __name__ == '__main__':
    # print(get_token())
    # print(login('2018189112'))
    pass
