from PrometheusDataHandler import PrometheusDataHandler
from Predictor import Predictor

import logging
import operator

def SimpleLoadBalance(GenericLoadBalance):

    def __init__(self):
        pass

    def __findBestModel(self,model: str) -> str:
        pred = Predictor()

        pdHandler = PrometheusDataHandler(model);

        data = pdHandler.get_data()
        results = {}

        count = 0.0

        #data = { ip, vals }
        for data_values in data.values():
            # data_values = [ (name,value) ]
            for r in data_values:
                try:
                    results[r[0]] += r[1]
                    #some times it is better to ask for forgiveness than permission :)
                except KeyError as e:
                    results[r[0]] = r[1]

            count += 1.0;

        ##
        #Here we take the average between all of the nodes
        ##
        for k in results.keys():
            val = results[k]
            results[k]= val/count

        order_acc = sorted(results.items(),key=operator.itemgetter(1));
        
        return order_acc.keys()[0];

    def getBestModel(self,model: str) -> str:

        return self.__findBestModel(model)
