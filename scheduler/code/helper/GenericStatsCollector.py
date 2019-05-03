import json
from . import logit

##
#Generic class to garentee functionality to children classes
##
class GenericStatsCollector(object):
    def __init__(self):
        self.logging = logit.get_logger()

    def write_log(self,msg):
        self.logging.info(msg)
