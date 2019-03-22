from .GenericNodeSelector import GenericNodeSelector

class PrometheusNodeSelector(GenericNodeSelector):
    def __init__(self,alg):
        self.alg = alg;
        super().__init__()
