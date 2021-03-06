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
    _thread: threading.Thread
    _period: datetime.timedelta
    _out_queue: queue.Queue
    _done: threading.Event

    def __init__(self, period: datetime.timedelta, name: str = "Metronome"):
        """Initialises the metronome with a given period."""
        self._thread = threading.Thread(name=name, target=self._run)
        self._period = period
        self._out_queue = queue.Queue(maxsize=0)
        self._done = threading.Event()
        self._done.clear()

    def _run(self):
        """Periodically enqueues tick events; runs in the self._thread."""
        while not self._out_queue.empty():
            self._out_queue.get()
        self._done.clear()
        while not self._done.is_set():
            time.sleep(self._period.total_seconds())
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

    def get(self) -> float:
        """Blocking call to retrieve tick events."""
        result = self._out_queue.get()
        self._out_queue.task_done()
        return result

    def backlog(self) -> int:
        """Returns the count of events in the queue."""
        return self._out_queue.qsize()
