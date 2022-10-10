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
import log


def get_not_report() -> list:
    """
    获取没有打卡的同学名单
    :return:
    """
    session = config.get_session()
    students = session.query(TSession)

    not_report = []

    during = 'morning' if datetime.datetime.now().hour < 12 else 'afternoon'
    try:
        for item in students:
            is_report = healthy_report.is_report(username=item.username, session_id=item.session_id,
                                                 xm_id=config.xm_id.get(during))
            if not is_report:
                not_report.append(session.query(StudentInfo).filter(StudentInfo.number == item.username).first().name)
        log.file_logger.info(f'获取未打卡同学名单完成，未打卡名单：{str(not_report)}')
        return not_report
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def remind_not_report(students: list = None, mode: int = 0):
    try:
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
                log.file_logger.info(f'已提醒未打卡同学, 提醒模式: {"人数模式" if mode == 0 else "姓名模式"}')
        else:
            log.file_logger.info(f"所有同学均已打卡")
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


if __name__ == '__main__':
    remind_not_report()
