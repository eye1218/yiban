# @Time : 2022/10/7 15:14 
# @Author : kang
# @File : scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
import daka
import report_check
import user_info_check

# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.INFO)


scheduler = BlockingScheduler()

scheduler.add_job(
    func=user_info_check.check_session_and_token,
    trigger='cron',
    name='检查session是否完整',
    minute='*/25',
)

scheduler.add_job(
    func=user_info_check.check_session_aliveness,
    trigger='cron',
    name='检查session是否过期',
    minute='*/25',
)

scheduler.add_job(
    func=report_check.remind_not_report,
    trigger='cron',
    name='早打卡提醒(人数)',
    hour='10',
    minute='0',
)

scheduler.add_job(
    func=report_check.remind_not_report,
    kwargs={'mode': 1},
    trigger='cron',
    name='早打卡提醒(名字)',
    hour='11',
    minute='0',
)

scheduler.add_job(
    func=report_check.remind_not_report,
    trigger='cron',
    name='晚打卡提醒(人数)',
    hour='16',
    minute='0',
)

scheduler.add_job(
    func=report_check.remind_not_report,
    trigger='cron',
    kwargs={'mode': 1},
    name='晚打卡提醒(名字)',
    hour='19',
    minute='0',
)

scheduler.add_job(
    func=daka.reset,
    trigger='cron',
    name='每日数据清零',
    hour='23',
    minute='57',
)

scheduler.add_job(
    func=daka.store_data,
    trigger='cron',
    name='存储每日数据',
    hour='23',
    minute='55',
)

scheduler.add_job(
    func=daka.daka,
    trigger='cron',
    name='自动打卡',
    hour='*/1',
)

scheduler.start()
