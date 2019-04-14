import json
from . import logit

class GenericStatsCollector(object):
    def __init__(self):
        self.logging = logit.get_logger()

    def write_log(self,msg):
        self.logging.info(msg)
