# @Time : 2022/9/3 20:12 
# @Author : kang
# @File : generate_student.py
from login import get_token, login, get_xm_id
from student import Student
import log


def generate_student(username: str, password: str = None) -> Student:
    """
    生成学生信息
    :param username: 学号
    :param password: 密码
    :return: 学生对象
    """
    if password is None:
        password = '@c' + username
    token = get_token()
    student = Student(username=username, password=password, token=token)
    session_id = login(student)
    student.session_id = session_id
    student.xm_id = get_xm_id(student)
    log.get_file_logger().info(f'学生：{username} 信息获取完成, 信息：{str(student)}')
    return student


if __name__ == '__main__':
    student = generate_student('20222015120003')
    print(student)
