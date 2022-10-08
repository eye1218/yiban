# @Time : 2022/10/7 20:51 
# @Author : kang
# @File : report_check.py
# @Desc: 检查是否上报
import datetime
import logging
import qq
import config
import healthy_report
from models import Session as TSession
from models import StudentInfo


def get_not_report() -> list:
    """
    获取没有打卡的同学名单
    :return:
    """
    session = config.get_session()
    students = session.query(TSession)

    not_report = []

    during = 'morning' if datetime.datetime.now().hour < 12 else 'afternoon'
    for item in students:
        is_report = healthy_report.is_report(username=item.username, session_id=item.session_id,
                                             xm_id=config.xm_id.get(during))
        if not is_report:
            not_report.append(session.query(StudentInfo).filter(StudentInfo.number == item.username).first().name)
    return not_report


def remind_not_report(students: list = None, mode: int = 0):
    if not students:
        students = get_not_report()
        if students:
            if mode == 1:
                message = "[CQ:at,qq=all]请以下同学尽快打卡："
                for item in students:
                    message += f'\n - {item}'
            else:
                message = f"[CQ:at,qq=all]还有{len(students)}位同学未打卡，请未打卡的同学尽快打卡。"
            qq.send_group_message(message, '837047229')


if __name__ == '__main__':
    remind_not_report()
