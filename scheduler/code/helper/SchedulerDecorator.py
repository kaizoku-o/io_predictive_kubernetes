from time import time
from kubernetes.client.rest import ApiException
from . import logit

scheduler_state = {};
backoff_count = 1.0;
logging = logit.get_logger()


##
#A function decorator used to wrap the schedule function within main.py
#This function prevents immediate duplicated scheduling requests and handles runtime errors that occur when
#the scheduler is unable to connect to tetris predicator.
##
#Future work could be for requeue and retrying pods that have actually failed to be scheduled here.
#though in our setup we had not experienced any issues with pods failing to be scheduled.
##
def backoff(func):
   
   def wrapper(*args, **kw):
      global scheduler_state
      global backoff_count

      ts = time()

      shadow_copy = dict(scheduler_state);

      for k,v in scheduler_state.items():
         if v['te'] < ts:
            del shadow_copy[k];

      scheduler_state = shadow_copy
      pod = args[0];

      if pod in scheduler_state:
         logging.info(pod + ": A Scheduling attempt has already occured: Ignore");
      else:
         try:
             func(*args, **kw)
             backoff_count = 1.0
         except ApiException as e:
            if backoff_count <  8.0:
               backoff_count += 1
            logging.info("Recieved API Exception due Conflict! Backoff is now: {0}".format(backoff_count));
         except ValueError as e:
            backoff_count = 1.0
            ###
            #Recieved ValueError for Null target, 
            #Ignoring because https://github.com/kubernetes-client/python/issues/547#issuecomment-455362558\n
            ##
         except RuntimeError as e:
            backoff_count = 8.0
            logging.warning(e)
         finally:
            ts = time();
            scheduler_state[pod] = {
               'te' : ts + backoff_count*10,
            }
   return wrapper
