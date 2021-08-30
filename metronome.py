#!/usr/bin/env python3
"""A source of time events."""
import datetime
import queue
import threading
import time

class Metronome:
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
        self._thread = threading.Thread(name="Metronome", target=self._run)
        self._lock = threading.RLock()
        self._period = period
        self._out_queue = queue.Queue()
        self._done = threading.Event()
        self._done.clear()

    def _run(self):
        """Periodically enqueues tick events; runs in the self._thread."""
        with self._lock:
            while not self._out_queue.empty():
                self._out_queue.get()
        self._done.clear()
        while not self._done.is_set():
            time.sleep(self._period.total_seconds())
            with self._lock:
                if not self._out_queue.full():
                    self._out_queue.put_nowait(time.time())

    def start(self):
        """Starts the metronome."""
        self._thread.start()

    def close(self):
        """Stops the metronome from generating events.
        Typically called via a contextlib.closing context manager
        on client exit from a with-clause.
        """
        self._done.set()
        self._thread.join()

    def get(self):
        """Blocking call to retrieve tick events."""
        with self._lock:
            return self._out_queue.get()
