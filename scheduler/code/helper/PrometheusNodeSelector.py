from .GenericNodeSelector import GenericNodeSelector
from .PrometheusQuery import get_predict_workload
class PrometheusNodeSelector(GenericNodeSelector):
    def __init__(self,alg,api):
        self.alg = alg;
        self.api = api;
        super().__init__()

