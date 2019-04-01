import logging

from time import time
from kubernetes.client.rest import ApiException

scheduler_state = {};
backoff_count = 1.0;
logging.basicConfig(level=logging.INFO)

def backoff(func):
	global scheduler_state
	global backoff_count

	ts = time();

	shadow_copy = dict(scheduler_state);

	for k,v in scheduler_state.items():
		if v['te'] < ts:
			del shadow_copy[k];

	scheduler_state = shadow_copy
	
	def wrapper(*args, **kw):
		pod = args[0];
		if pod in scheduler_state:
			logging.info(pod + ": A Scheduling attempt has already occured: Ignore");
		else:
			try:
				func(args);
			except ApiException as e:
				if backoff_count <  8.0:
					backoff_count += 1;
				logging.info("Recieved API Exception due Conflict! Backoff is now: {0}".format(backoff_count));
			except ValueError as e:
				backoff_count = 1.0;
				###
				#Recieved ValueError for Null target, 
				#Ignoring because https://github.com/kubernetes-client/python/issues/547#issuecomment-455362558\n
				##
			except RuntimeError as e:
				backoff_count = 8.0;
				logging.warning(e);
			finally:
				ts = time();
				scheduler_state[pod] = {
					'te' : ts + backoff_count*10,
				}
	return wrapper


##
#
##
def handle_runtime_error(func):

    def wrapper(*args, **kw):
        try 
            return func(args);
        except RuntimeError as e:
            logging.warning(e);
            return None;

    return wrapper
