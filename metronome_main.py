#!/usr/bin/env python3
import sys                      # access to basic things like sys.argv
import os                       # access pathname utilities
import argparse                 # for command-line options parsing
import contextlib
import datetime

import metronome

def main(argv):
    """A simple programme using the metronome."""
    exit_code = 0
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("-p","--period", metavar='PERIOD', type=int,
                        dest="period", default=1,
                        help="Metronome period.")
    args = parser.parse_args(args=argv[1:])  # will exit on parse error
    period = datetime.timedelta(seconds=args.period)
    with contextlib.closing(metronome.Metronome(period)) as ticker:
        ticker.start()
        for i in range(10):
            t = ticker.get()
            print("tick at", t)
    return exit_code

if __name__ == "__main__":
    sys.exit(main(sys.argv))


# Local Variables:
# mode: python
# python-indent: 4
# End:
# vim: set expandtab:
