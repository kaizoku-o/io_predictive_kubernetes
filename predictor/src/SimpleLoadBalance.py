from PrometheusDataHandler import PrometheusDataHandler
from Predictor import Predictor
from GenericLoadBalance import GenericLoadBalance

import logging
import operator

class SimpleLoadBalance(GenericLoadBalance):

    def __init__(self):
        pass

    def __findBestModel(self,model: str) -> str:
        pred = Predictor()

        pdHandler = PrometheusDataHandler(model);

        data = pdHandler.get_data()
        results = {};

        count = 0.0
        print("running")
        #data = { ip, vals }
        for ip in data:
            # data_values = [ (name,value) ]
            values = data[ip]
            data_values = pred.accuracy(values);
            for r in data_values:
                print(r)
                try:
                    results[r[1]] += r[0]
                    #some times it is better to ask for forgiveness than permission :)
                except KeyError as e:
                    results[r[1]] = r[0]
            count += 1.0;

        ##
        #Here we take the average between all of the nodes
        ##
        for k in results.keys():
            val = results[k]
            results[k]= val/count

        order_acc = sorted(results.items(),key=operator.itemgetter(1));
        return order_acc[0][0];

    def getBestModel(self,model: str) -> str:

        return self.__findBestModel(model)
