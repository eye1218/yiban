# @Time : 2022/9/3 19:00 
# @Author : kang
# @File : healthy_report.py
import json

import config
import requests
import base64
import re

import log


def is_report(username: str, session_id: str, xm_id: str) -> bool:
    """
    检查是否已经完成健康报送
    :return: 是否完成健康上报
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Cookie': f'JSESSIONID={session_id}; username={username}; menuVisible=1',
        }
        data = {
            'xmid': xm_id,
            'pdnf': 2020,
        }
        res = requests.post(config.check_url, headers=headers, data=data)
        res.raise_for_status()
        if '今日已经申请' in res.content.decode():
            return True
        else:
            return False
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def is_login(username: str, session_id: str):
    """
    检查是否登录
    :return:
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Cookie': f'JSESSIONID={session_id}; username={username}; menuVisible=1',
        }
        res = requests.post(url=config.check_login_url, headers=headers)
        res.raise_for_status()
        if 'true' in res.content.decode():
            return True
        else:
            return False
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def healthy_report(username: str, session_id: str, xm_id: str) -> bool:
    """
    健康上报
    :return:
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
            'Cookie': f'JSESSIONID={session_id}; username={username}; menuVisible=1',
        }
        info = {"xmqkb": {"id": xm_id},
                "c1": "小于37.3℃", "c2": "否",
                "type": "XSFXTWJC",
                "pdnf": "2020",
                "sqbzt": "提交",
                "location_longitude": config.location.get('location_longitude'),
                "location_latitude": config.location.get('location_latitude'),
                "location_address": config.location.get('address'),
                }
        data = {
            'data': json.dumps(info),
            'msgUrl': 'syt/zzglappro/index.htm?type=xsfxtwjc&xmid={xmid}'.format(xmid=xm_id),
            'multiSelectData': '',
            'verCode': '',
        }
        res = requests.post(config.report_url, headers=headers, data=data)
        res.raise_for_status()
        if res.content.decode() == 'success' or res.content.decode() == 'Applied today':
            return True
        else:
            return False
    except Exception as e:
        log.file_logger.exception(f'错误信息: {e}, username: {username}, session_id: {session_id}, xm_id: {xm_id}')
        log.console_logger.exception(f'错误信息: {e}, username: {username}, session_id: {session_id}, xm_id: {xm_id}')


def get_token() -> str:
    """
    获取token
    :return:
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        res = requests.get(config.token_url, headers=headers)
        res.raise_for_status()
        cookie = res.headers.get('Set-Cookie')
        token = re.findall(r'token=(.*?);', cookie)
        if len(token) == 1:
            return token[0]
        else:
            return ''
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def get_cookie(username: str, password: str, token: str) -> str:
    """
    登录，返回cookie
    :return: cookie
    """
    try:
        e_username = base64.b64encode(username.encode())
        e_password = base64.b64encode(password.encode())
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        }
        data = {
            'username': e_username,
            'password': e_password,
            'verification': '',
            'token': token,
        }
        res = requests.post(config.login_url, headers=headers, data=data)
        res.raise_for_status()
        cookie = res.headers.get('Set-Cookie')
        session_id = re.findall(r'JSESSIONID=(.*?);', cookie)
        if len(session_id) == 1:
            log.file_logger.info(f'登录成功, student: {username}, password: {password}, session_id: {session_id[0]}')
            return session_id[0]
        else:
            log.file_logger.warning(f'登录失败, student: {username}, password: {password}')
            return ''
    except Exception as e:
        log.file_logger.exception(f'错误信息：{e}, student: {username}, password: {password}')
        log.console_logger.exception(f'错误信息：{e}, student: {username}, password: {password}')
