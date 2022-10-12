# @Time     : 2022/10/12 20:38 
# @Author   : kang
# @File     : data.py
# @Desc     : 数据同步
import datetime

import config
import log
from models import StudentInfo, Attendance, AttendanceHistory


def sync_auto_student():
    """
    同步student_info表中的自动打卡同学的信息到attendance表中
    :return:
    """
    try:
        session = config.get_session()
        auto_added_student = [item.username for item in session.query(Attendance).with_entities(Attendance.username)]
        auto_student = (item.number for item in session.query(StudentInfo).filter(StudentInfo.auto == 1).with_entities(StudentInfo.number))

        for item in auto_student:
            if item not in auto_added_student:
                attendance = Attendance(
                    username=item,
                )
                session.add(attendance)
                log.file_logger.info(f'正在添加自动打卡, username: {item}')
        session.commit()
        log.file_logger.info(f'student_info表中的自动打卡信息已同步到attendance数据库')
    except Exception as e:
        log.file_logger.exception(f'自动打卡信息同步失败，信息：{e}')
        log.console_logger.exception(f'自动打卡信息同步失败，信息：{e}')


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


if __name__ == '__main__':
    sync_auto_student()
