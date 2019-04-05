import threading

from SimpleLoadBalance import SimpleLoadBalance

class AsyncLoadBalance(SimpleLoadBalance):
	def __init__(self):
            self.workers = [];
            self.monitor_handle = None;

            self.lock = Lock();

            self.best_model = {
                    'io' : None,
                    'mem' : None,
                    'cpu' : None
            }

            SimpleLoadBalance.__init__(self);

        ##
        #Worker thread that will update the best_model probably should add some short of logging to determine why
        #a certain model was picked or isolated
        ##
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

        ##
        #A monitor thread to determine when the workers are done, or even if that making a new predicition is in progress
        ##
        def __monitor(self):
            ##
            #There are already Threads running
            ##
            if len(self.workers) > 0:
                return;

            model_names = list(self.best_model.keys());

            for mn in model_names:
                #create a thread
                t = threading.Thread(target=self.__threaded,args=(mn))
                t.start()
                self.workers.append(t)

            for t in self.threads:
                t.join()
            ##
            #all of the threads have terminated
            ##
            self.threads = [];

        ##
        #Kicks off the AsyncWorkers to determine the best model to use in the future
        ##
        def populateBestModel(self):
            self.monitor_handle = Threading.Thread(target=self.__monitor)
            return self.monitor_handle;

        ##
        #determines the best model to use.  If a model was never found it will block on the monitoring thread to garentee that it will return a
        #result
        ##
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

