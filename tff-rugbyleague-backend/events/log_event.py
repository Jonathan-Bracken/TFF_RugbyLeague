# events/log_event.py

import time

def log_event(self, commentary, timeToAdd, timeToWait = 5):
    self.commentary.append(commentary)
    self.current_seconds += timeToAdd
    time.sleep(min(timeToWait, 2))