# @Time : 2022/10/7 13:51 
# @Author : kang
# @File : user_info_check.py
# @Description: 检测用户信息是否完整,如果不完整则添加至完整
import config
import log
from models import Session as TSession
from models import StudentInfo
import healthy_report


def check_session_and_token():
    """
    检查session表中的session_id和token是否完整，不完整的话补充完整
    :return:
    """
    try:
        session = config.get_session()
        sessions = session.query(TSession)
        for item in sessions:
            try:
                # 检查session_id
                if not item.session_id:
                    log.file_logger.debug(f'Session表中session_id为空, username: {item.username}')
                    session_id = healthy_report.get_cookie(
                        item.username,
                        session.query(StudentInfo).filter(StudentInfo.number == item.username).first().password,
                        healthy_report.get_token()
                    )
                    if session_id:
                        session.query(TSession).filter(TSession.username == item.username).update(
                            {'session_id': session_id})
                    else:
                        continue

                # 检查token
                if not item.token:
                    token = healthy_report.get_token()
                    if token:
                        session.query(TSession).filter(TSession.username == item.username).update({'token': token})
                    else:
                        log.file_logger.warning(f'获取token失败, username: {item.username}')
                        continue

            except Exception as e:
                log.file_logger.exception(f'异常信息: {e}, username: {item.username}')
                log.console_logger.exception(f'异常信息: {e}, username: {item.username}')
        session.commit()
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


def check_session_aliveness():
    """
    检查session_id是否存活
    :return:
    """
    try:
        session = config.get_session()
        sessions = session.query(TSession)
        for item in sessions:
            try:
                status = healthy_report.is_login(item.username, item.session_id)
                if not status:
                    session_id = healthy_report.get_cookie(
                        item.username,
                        session.query(StudentInfo).filter(StudentInfo.number == item.username).first().password,
                        token=item.token,
                    )
                    if session_id:
                        session.query(TSession).filter(TSession.username == item.username).update(
                            {'session_id': session_id})
                    else:
                        continue
            except Exception as e:
                log.console_logger.exception(f'异常信息: {e}, username: {item.username}')
                log.file_logger.exception(f'异常信息: {e}, username: {item.username}')
                pass
        session.commit()
    except Exception as e:
        log.file_logger.exception(e)
        log.console_logger.exception(e)


if __name__ == '__main__':
    check_session_and_token()
    check_session_aliveness()
