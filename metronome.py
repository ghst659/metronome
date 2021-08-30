#!/usr/bin/env python3
"""A source of time events."""
import datetime
import queue
import threading
import time

class Metronome(threading.Thread):
    """A source of time events.
    Example usage:
      period = datetime.timedelta(seconds=1)
      with contextlib.closing(Metronome(period)) as ticker:
        ticker.start()
        for i in range(10):
          t = ticker.get()
          print("tick at", t)
    """

    def __init__(self, period: datetime.timedelta):
        """Initialises the metronome with a given period."""
        threading.Thread.__init__(self)
        self._period = period
        self._out_queue = queue.SimpleQueue()
        self._end_run = threading.Event()
        self._end_run.clear()

    def close(self):
        """Stops the metronome from generating events.
        Typically called via a contextlib.closing context manager
        on client exit from a with-clause.
        """
        self._end_run.set()
        self.join()

    def run(self):
        """Periodically enqueues tick events.
        Called by self.start(); not to be directly called by the client.
        """
        while not self._out_queue.empty():
            self._out_queue.get()
        self._end_run.clear()
        while not self._end_run.is_set():
            time.sleep(self._period.total_seconds())
            self._out_queue.put_nowait(time.time())

    def get(self):
        """Blocking call to retrieve tick events."""
        return self._out_queue.get()
