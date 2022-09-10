# @Time : 2022/9/3 19:12 
# @Author : kang
# @File : student.py
from dataclasses import dataclass


@dataclass
class Student:
    username: str
    password: str
    token: str
    session_id: str = ''
    xm_id: list = None

    def __str__(self):
        return str(locals())