import threading

from SimpleLoadBalance import SimpleLoadBalance

class AsyncLoadBalance(SimpleLoadBalance):
    def __init__(self):
        self.workers = [];
        self.monitor_handle = None;

        self.lock = threading.Lock();

        self.best_model = {
                'io' : None,
                'mem' : None,
                'cpu' : None
        }

        SimpleLoadBalance.__init__(self);

    def __threaded(self,model: str):
        ##
        #Thread preamble
        ##
        alg = SimpleLoadBalance.getBestModel(self,model)
        self.lock.acquire()
        ##
        #Critical Section
        ##
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
        if not self.monitor_handle or not self.monitor_handle.isAlive():
            self.monitor_handle = threading.Thread(target=self.__monitor)
            self.monitor_handle.start()
        else:
            print("~~~~~~~~~~~~~~~~ALREADY RUNNING~~~~~~~~~~~~~")

        return self.monitor_handle
    def getBestModel(self,model: str) -> str:
    
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
    
