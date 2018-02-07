# -*- coding: utf-8 -*-

import json
import threading
import os
import time

class StatusWatcher(threading.Thread):
    def __init__(self, filename, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.filename = filename
        self.stop_me = False

    def run(self):
        last_change = 0
        while not self.stop_me:
            time.sleep(0.5)
            mtime = os.path.getmtime(self.filename)
            #plug.show_error("Checked at " + str(mtime))
            if mtime != last_change:
                mtime = last_change
                with open(self.filename, "rt") as status_file:
		    try:
                        status = json.load(status_file)
                        # Report the new status
                        self.queue.put(status)
                    except ValueError:
		        pass

    def stop(self):
        self.stop_me = True

