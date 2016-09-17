import time
import threading
from concurrent import futures
from utils import logger
from collections import deque

class TaskTracker:

    def __init__(self):
        self.expiration_time = 300 # in seconds
        self.future_dictionary_lock = threading.Lock()
        self.current_taskID = 0
        self.taskID_to_future = {}
        self.completed_futures = deque(maxlen=1000000)

    # Keep track of a future with a new taskID
    def register_future(self,future):
        with self.future_dictionary_lock:
            self.current_taskID += 1
            future.__taskID__ = self.current_taskID
            self.taskID_to_future[future.__taskID__] = future
        logger.info("Registered task "+str(future.__taskID__)+": "+str(future))
        future.add_done_callback(self.on_future_done)
        return future.__taskID__

    # Lookup a future by its taskID
    def lookup_future(self,taskID):
        with self.future_dictionary_lock:
            return self.taskID_to_future[taskID]

    # Callback when a future finishes
    def on_future_done(self,future):
        # Let the result stick around for a little while so it can be queried.
        future.__expiration_time__ = time.time() + self.expiration_time
        logger.info("Task "+str(future.__taskID__)+" finished, expiring at "+str(future.__expiration_time__))
        with self.future_dictionary_lock:
            self.completed_futures.append(future)
        self.remove_expired_futures()

    # Clean up old expired futures
    def remove_expired_futures(self):
        with self.future_dictionary_lock:
            now = time.time()
            while len(self.completed_futures) > 0:
                future = self.completed_futures.popleft()
                if future.__expiration_time__ > now:
                    self.completed_futures.appendleft(future)
                    break
                logger.info("Task "+str(future.__taskID__)+" expired, removing")
                self.taskID_to_future.pop(future.__taskID__)

