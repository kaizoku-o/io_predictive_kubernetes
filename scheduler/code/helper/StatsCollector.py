import json

class StatsCollector(object):
    def __init__(self):
        self.fin = open("./decision.log","w");

    def write_log(self,msg):
        self.fin.write(msg + "\n");
        self.fin.flush();
