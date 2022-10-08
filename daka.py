# @Time : 2022/10/7 22:11 
# @Author : kang
# @File : daka.py
# @Desc: daka
import datetime

import config
import healthy_report
import log
import qq
from models import Session as TSession
from models import StudentInfo, Attendance, AttendanceHistory


def daka():
    """
    完成易班健康填报
    :return:
    """
    # 筛选出未打卡同学
    try:
        session = config.get_session()
        fil = Attendance.morning if datetime.datetime.now().hour < 12 else Attendance.afternoon
        during = 'morning' if datetime.datetime.now().hour < 12 else 'afternoon'
        during_name = '上午' if during == 'morning' else '下午'
        xm_id = config.xm_id.get(during)
        students = session.query(Attendance).filter(fil == 0)
        for item in students:
            qq_number = session.query(StudentInfo).filter(StudentInfo.number == item.username).first().qq
            try:
                result = healthy_report.healthy_report(username=item.username, session_id=session.query(TSession).filter(
                    TSession.username == item.username).first().session_id, xm_id=xm_id)
                if result:
                    message = f'{during_name}: 打卡成功 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                    session.query(Attendance).filter(Attendance.username == item.username).update(values={during: 1})
                    log.file_logger.info(f'打卡成功，学号：{item.username}')
                else:
                    message = f'[X] {during_name}: 打卡失败，请手动完成打卡 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                    log.file_logger.warning(f'打卡过程中出现错误，已QQ提醒。学号：{item.username}')
                if qq_number:
                    qq.send_private_message(qq=qq_number, message=message)
                    log.file_logger.info(f'已QQ提醒打卡信息，学号：{item.username}, QQ：{qq_number}')
            except Exception as e:
                qq.send_private_message(qq=qq_number,
                                        message=f'{during_name}: 打卡时发生了异常，异常信息：{e},请手动完成打卡')
                log.file_logger.warning(f'打卡过程中发生异常，已QQ提醒。学号：{item.username}, QQ：{qq_number}')
                log.file_logger.exception(e)
                log.console_logger.exception(e)
        session.commit()
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def reset():
    """
    将Attendance表里的数据重置
    :return:
    """
    try:
        session = config.get_session()
        session.query(Attendance).update({'morning': 0, 'afternoon': 0})
        session.commit()
        log.file_logger.info('Attendance表已重置')
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def store_data():
    """
    存储打卡记录
    :return:
    """
    try:
        session = config.get_session()
        messages = session.query(Attendance)
        for item in messages:
            obj = AttendanceHistory(
                username=item.username,
                date=datetime.date.today(),
                morning=item.morning,
                afternoon=item.afternoon,
            )
            session.add(obj)
        session.commit()
        log.file_logger.info('Attendance表的数据已备份至AttendanceHistory表中')
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


if __name__ == '__main__':
    daka()
