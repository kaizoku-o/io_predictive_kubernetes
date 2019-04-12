from SimpleLoadBalance import SimpleLoadBalance
import threading
import logging

log_format='%(asctime)s - %(process)d - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
logging.basicConfig(filename='predictor.log', filemode='a', 
    format=log_format, level=logging.DEBUG)

class AsyncLoadBalance(SimpleLoadBalance):
    """
    This is a singleton class which is used for precomputing the best model.
    To get the instance call AsyncLoadBalance.getInstance()
    """

    # Instances will be stored in __instance
    __instance = None

    @staticmethod
    def getInstance():
        """ 
        Static access method. 
        To get an instance just run AsyncLoadBalance.getInstance().
        """
        if AsyncLoadBalance.__instance == None:
            AsyncLoadBalance()
        return AsyncLoadBalance.__instance 

    def __init__(self):
        """ Private constructor """
        if AsyncLoadBalance.__instance != None:
            raise Exception("This is a singleton class!")
        else:
            AsyncLoadBalance.__instance = self

        self.workers = [];
        self.monitor_handle = None;

        self.lock = threading.Lock();

        self.best_model = {
                'io' : None,
                'mem' : None,
                'cpu' : None
        }

        SimpleLoadBalance.__init__(self);

    def __threaded(self, model: str):
        ##
        #Thread preamble
        ##
        logging.debug("Thread computing best model for %s", model)
        alg = SimpleLoadBalance.getBestModel(self, model)
        self.lock.acquire()
        ##
        #Critical Section
        ##
        logging.debug("****Best model for %s is %s :)****", model, alg)
        self.best_model[model] = alg
        ##
        #Leaving Critical Section
        ##
        self.lock.release()

    def __monitor(self):
        ##
        #There are already Threads running
        ##
        if len(self.workers) > 0:
            return;
    
        model_names = list(self.best_model.keys());
    
        for mn in model_names:
            #create a thread
            logging.debug("Starting thread for %s", mn)
            t = threading.Thread(target=self.__threaded,args=(mn,))
            t.start()
            self.workers.append(t)
    
        for t in self.workers:
            t.join()
        ##
        #all of the threads have terminated
        ##
        self.workers = [];
    
    def populateBestModel(self):
        logging.debug("****Computing best model****")
        if not self.monitor_handle or not self.monitor_handle.isAlive():
            self.monitor_handle = threading.Thread(target=self.__monitor)
            self.monitor_handle.start()
        else:
            logging.debug("****Threads are already running, exiting****")

        return self.monitor_handle

    def getBestModel(self, model: str) -> str:
        logging.debug("****Get best model called for %s****", model)
        self.lock.acquire()
        my_best_pick = self.best_model[model]
        self.lock.release()
    
        if not my_best_pick:
            if self.monitor_handle:
                if self.monitor_handle.isAlive():
                    self.monitor_handle.join()
                else:
                    self.populateBestModel().join();
            else:
                self.populateBestModel().join();
    
            self.lock.acquire()
            my_best_pick = self.best_model[model]
            self.lock.release()
    
        return my_best_pick;
    