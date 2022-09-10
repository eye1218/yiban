# @Time : 2022/9/4 16:57 
# @Author : kang
# @File : log.py
import logging


def get_file_logger(filename: str = '/var/log/daka.log'):
    logging.basicConfig(filename=filename, encoding='utf8', level=logging.DEBUG,
                        format='%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    ch = logging.StreamHandler()
    fmt = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(fmt)
    logger = logging.getLogger()
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    log = get_file_logger()
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.critical('critical')
