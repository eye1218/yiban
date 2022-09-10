# @Time : 2022/9/3 19:00 
# @Author : kang
# @File : healthy_report.py
import datetime
import json

import requests

from generate_student import generate_student
from student import Student
import log

check_url = 'http://202.203.16.42/syt/zzapply/checkrestrict.htm'
report_url = 'http://202.203.16.42/syt/zzapply/operation.htm'
logger = log.get_file_logger()


def is_report(student: Student, xm_id: str) -> bool:
    """
    检查是否已经完成健康报送
    :param student: 学生信息
    :param xm_id: 填报标识
    :return: 是否完成健康上报
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Cookie': f'JSESSIONID={student.session_id}; username={student.username}; menuVisible=1',
    }
    data = [{
        'xmid': xm_id,
        'pdnf': 2020,
    } for xm_id in student.xm_id]
    res = requests.post(check_url, headers=headers, data=data)
    res.raise_for_status()
    if '今日已经申请' in res.content.decode():
        logger.info(f'用户：{student.username} 今日已经申请')
        return True
    else:
        logger.info(f'用户：{student.username} 未完成申请，即将自动报送健康信息')
        return False


def healthy_report(student: Student):
    """
    健康上报
    :param student: 学生信息
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Cookie': f'JSESSIONID={student.session_id}; username={student.username}; menuVisible=1',
    }
    flag = True
    for item in student.xm_id:
        if not is_report(student, item):
            info = {"xmqkb": {"id": item},
                    "c1": "小于37.3℃", "c2": "否",
                    "type": "XSFXTWJC",
                    "location_longitude": 100.157767,
                    "location_latitude": 25.668927,
                    "location_address": "云南省 大理白族自治州 大理市 至理南路 3号 靠近瑞幸咖啡(大理大学校区店) ",
                    }
            data = {
                'data': json.dumps(info),
                'msgUrl': 'syt/zzglappro/index.htm?type=xsfxtwjc&xmid={xmid}'.format(xmid=item),
                'multiSelectData': '',
                'verCode': '',
            }
            res = requests.post(report_url, headers=headers, data=data)
            res.raise_for_status()
            if res.content.decode() == 'success' or res.content.decode() == 'Applied today':
                logger.info(f'用户；{student.username} 打卡成功')
            else:
                logger.error(f'用户：{student.username} 打卡失败，请求体：{str(data)}, 返回体：{res.content.decode()}')
                flag = False
    return flag


def daka(username: str, password: str = None):
    student = generate_student(username, password)
    return healthy_report(student)


if __name__ == '__main__':
    username = '20222015120003'
    with open('/tmp/daka.log', 'a', encoding='utf8') as f:
        try:
            if daka(username):
                f.write(f'打卡成功 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            else:
                f.write(f'打卡失败 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        except Exception as e:
            logger.error(f'{str(e)}')
            f.write(str(e))
            f.write('\n')
