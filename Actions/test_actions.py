from Paths.paden import pad_naar_test_file
from .actions import timeblock_to_watch_in
from datetime import datetime, timedelta, date


def test_timeblock_to_watch_in():
    test = timeblock_to_watch_in(pad_naar_test_file)
    assert test == 0

