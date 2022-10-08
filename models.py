# coding: utf-8
from sqlalchemy import Column, Date, String, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Attendance(Base):
    __tablename__ = 'attendance'

    username = Column(String(20), primary_key=True)
    morning = Column(TINYINT(1), server_default=text("'0'"))
    afternoon = Column(TINYINT(1), server_default=text("'0'"))


class AttendanceHistory(Base):
    __tablename__ = 'attendance_history'

    username = Column(String(20), primary_key=True)
    date = Column(Date, nullable=False)
    morning = Column(TINYINT(1), server_default=text("'0'"))
    afternoon = Column(TINYINT(1), server_default=text("'0'"))


class Session(Base):
    __tablename__ = 'session'

    username = Column(String(20), primary_key=True)
    session_id = Column(String(100))
    token = Column(String(100))


class StudentInfo(Base):
    __tablename__ = 'student_info'

    number = Column(String(20), primary_key=True, unique=True)
    name = Column(String(10), nullable=False)
    auto = Column(TINYINT(1), server_default=text("'0'"))
    qq = Column(String(20))
    password = Column(String(20))
