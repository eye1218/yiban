# @Time : 2022/10/7 11:11 
# @Author : kang
# @File : config.py
import random
from sqlalchemy import select, update, create_engine
from sqlalchemy.orm import Session

host = '8.210.0.124'
password = 'wintel@123456'
user = 'root'
port = 3306
database = 'student'

check_url = 'http://202.203.16.42/syt/zzapply/checkrestrict.htm'
report_url = 'http://202.203.16.42/syt/zzapply/operation.htm'
check_login_url = 'http://202.203.16.42/nonlogin/login/isLogin.htm'
login_url = 'http://202.203.16.42//login/Login.htm'
token_url = 'http://202.203.16.42/'
xm_url = 'http://202.203.16.42/syt/zzapply/queryxmqks.htm?type=xsfxtwjc'

xm_id = {
    'morning': 'ff8080817f8b5c9e017fdf5314b13a7e',
    'afternoon': 'ff8080817f8b5da8017fdf53e9af3ac3',
}

location = {
    'location_longitude': 100.15 + random.randint(1, 9999) / 1000000,
    'location_latitude': 25.66 + random.randint(1, 9999) / 1000000,
    'address': random.choice([
        '云南省 大理白族自治州 大理市 至理南路 3号 靠近瑞幸咖啡(大理大学校区店)',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学第一综合教学楼',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学工科楼',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学东北门',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学第二教学综合楼',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学随意美食城',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学体育馆',
        '云南省 大理白族自治州 大理市 至理南路 3号 靠大理大学智慧物流中心',
    ])
}


def get_session():
    engine = create_engine(url='mysql+pymysql://root:wintel%40123456@8.210.0.124:3306/student')
    session = Session(bind=engine)
    return session
