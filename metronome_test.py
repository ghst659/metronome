#!/usr/bin/env python3

import metronome

import contextlib
import datetime
import unittest

from unittest.mock import patch

class MockTime:
    def __init__(self):
        self._time = 0

    def sleep(self, seconds):
        self._time += seconds

    def time(self):
        return self._time


class TestMetronome(unittest.TestCase):
    def test_five_ticks(self):
        got = []
        period = datetime.timedelta(seconds=2)
        mt = MockTime()
        with patch("time.sleep", side_effect=mt.sleep), \
             patch("time.time", side_effect=mt.time):
            with contextlib.closing(metronome.Metronome(period)) as ticker:
                ticker.start()
                for i in range(5):
                    got.append(ticker.get())
        self.assertEqual(got, [2.0, 4.0, 6.0, 8.0, 10.0])

if __name__ == "__main__":
    unittest.main()
