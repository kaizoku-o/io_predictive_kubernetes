import logging

LOG_FILE = '/var/log/predictor.log'

def get_logger():
    log_format = '%(asctime)s - %(process)d - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
    logging.basicConfig(filename=LOG_FILE, filemode='a', format=log_format, level=logging.DEBUG)
    return logging