import logging
from datetime import datetime

class Logger:
    
    def __init__(self):
        # 로그 생성
        self.logger = logging.getLogger()

        # 로그의 레벨
        self.logger.setLevel(logging.INFO)

        # log 출력 형식
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # log를 터미널에 출력
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # log를 파일에 출력
        filename = datetime.today().strftime('%y%m%d')
        file_handler = logging.FileHandler(f"example_{filename}.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # for i in range(10):
        #     log.info(f"테스트 로그 입니다. {i}")


    def info(self, value):
        self.logger.info(f'{value}')

    def error(self, err):
        self.logger.error(err)