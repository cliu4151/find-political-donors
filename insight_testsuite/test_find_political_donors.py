#!/usr/bin/env python

import unittest
import sys

sys.path.append('../src/')
from find_political_donors import checkDate

class FindPoliticalDonorsHelperFuncTestCase(unittest.TestCase):
    """Tests for checkDate in `find_political_donors.py`."""

    def test_is_date_not_valid(self):
        """Is 012017 a valid date?"""
        self.assertFalse(checkDate('012017'))
    def test_is_date_valid(self):
        """Is 01312017 a valid date?"""
        self.assertTrue(checkDate('01312017'))
    def test_is_empty_date_not_valid(self):
        """Is '' a valid date?"""
        self.assertFalse(checkDate(''))

if __name__ == "__main__":
    unittest.main()