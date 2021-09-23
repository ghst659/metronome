#!/usr/bin/env python3
import sys                      # access to basic things like sys.argv
import os                       # access pathname utilities
import argparse                 # for command-line options parsing
import contextlib
import datetime
import math
import time

from collections.abc import Sequence

import metronome

def main(argv: Sequence[str]) -> int:
    """A simple programme using the metronome."""
    exit_code = 0
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-p","--period", metavar='PERIOD', type=float,
                        dest="period", default=2,
                        help="Metronome period.")
    parser.add_argument("--action", metavar="ACTION", type=float,
                        dest="action", default=1.5,
                        help="Workload duration.")
    args = parser.parse_args(args=argv[1:])  # will exit on parse error
    period = f2s(args.period)
    with contextlib.closing(metronome.Metronome(period)) as ticker:
        ticker.start()
        for i in range(10):
            unused_t = ticker.get()
            blocking_work(args.action)
    return exit_code

def blocking_work(duration_secs: float):
    """Some blocking task that takes time."""
    print("work start", time.time())
    time.sleep(duration_secs)
    print("       end", time.time())
    
def f2s(float_secs: float) -> datetime.timedelta:
    """Converts float seconds to a timedelta."""
    MILLION = 1000000
    micros = math.trunc(float_secs * MILLION)
    sec = micros // MILLION
    usec = micros % MILLION
    return datetime.timedelta(seconds=sec, microseconds=usec)

if __name__ == "__main__":
    sys.exit(main(sys.argv))


# Local Variables:
# mode: python
# python-indent: 4
# End:
# vim: set expandtab:
