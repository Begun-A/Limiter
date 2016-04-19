import os, sys
from unittest.case import TestCase
import time

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(APP_ROOT))

from handlers import count_timeout

ACCURACY = 2
GEN_TIME = 0.5  # generation time page
RATE_LIMIT = 1


class TestAlgorithmCountTimeOutFunction(TestCase):
    """Testing algorithm count_timeout function"""

    def setUp(self):
        from handlers import DOMENS
        DOMENS.clear()

    def test_requests_at_the_same_time(self):
        """Test count_timeout when 3 requests sent at the same time"""
        for i in range(3):
            timeout = count_timeout('domen', GEN_TIME, RATE_LIMIT)
            self.assertEqual(round(timeout, ACCURACY), i * RATE_LIMIT)

    def test_requests_with_interval(self):
        """Test count_timeout when requests sent with inteval"""
        timeout1 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        time.sleep(1)
        timeout2 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        timeout3 = count_timeout('domen', GEN_TIME, RATE_LIMIT)

        self.assertEqual(round(timeout1, ACCURACY), 0)
        self.assertEqual(round(timeout2, ACCURACY), 1)
        self.assertEqual(round(timeout3, ACCURACY), 3)

    def test_requests_with_interval_more_than_stap(self):
        """Test count_timeout when requests sent with iterval more than rate limit"""
        timeout1 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        time.sleep(2)
        timeout2 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        time.sleep(1)
        timeout3 = count_timeout('domen', GEN_TIME, RATE_LIMIT)

        self.assertEqual(round(timeout1, ACCURACY), 0)
        self.assertEqual(round(timeout2, ACCURACY), 0)
        self.assertEqual(round(timeout3, ACCURACY), 1)

    def test_when_two_different_domens(self):
        """Test count_timeout when requests sent with two differenet domens"""
        timeout1 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        timeout2 = count_timeout('domen1', GEN_TIME, RATE_LIMIT)
        time.sleep(1)
        timeout3 = count_timeout('domen', GEN_TIME, RATE_LIMIT)
        time.sleep(1)
        timeout4 = count_timeout('domen1', GEN_TIME, RATE_LIMIT)

        self.assertEqual(round(timeout1, ACCURACY), 0)
        self.assertEqual(round(timeout2, ACCURACY), 0)
        self.assertEqual(round(timeout3, ACCURACY), 1)
        self.assertEqual(round(timeout4, ACCURACY), 0)

    def test_when_generation_time_page_greater(self):
        """Test count_timeout when geration time page greater than rate limit"""
        timeout1 = count_timeout('domen', 3, RATE_LIMIT)
        timeout2 = count_timeout('domen', 4, RATE_LIMIT)
        time.sleep(1)
        timeout3 = count_timeout('domen', 4, RATE_LIMIT)
        time.sleep(6)
        timeout4 = count_timeout('domen', 0.5, RATE_LIMIT)
        time.sleep(6)
        timeout5 = count_timeout('domen', 4, RATE_LIMIT)

        self.assertEqual(round(timeout1, ACCURACY), 0)
        self.assertEqual(round(timeout2, ACCURACY), 4)
        self.assertEqual(round(timeout3, ACCURACY), 7)
        self.assertEqual(round(timeout4, ACCURACY), 3)
        self.assertEqual(round(timeout5, ACCURACY), 1)
