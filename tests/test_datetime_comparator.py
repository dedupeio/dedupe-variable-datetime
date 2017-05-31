import math
import unittest

import numpy as np

from dedupe.variables.datetime import DateTimeType



def test_datetime_to_datetime_comparison():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('2017-05-25',
                                                '2017-01-01'),
        np.array([1, 0, 1, 0, 0, math.sqrt(144), 0, 0, 0]))

def test_datetime_to_timestamp_comparison():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('2017-05-25',
                                                '2017-01-01 12:30:05'),
        np.array([1, 0, 1, 0, 0, math.sqrt(143), 0, 0, 0]))

def test_timestamp_to_timestamp_comparison():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('2017-05-25 21:08:09',
                                                '2017-01-01 12:30:05'),
        np.array([1, 1, 0, 0, math.sqrt(12472684), 0, 0, 0, 0]))

def test_years():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('2012',
                                                '2010'),
        np.array([1, 0, 0, 0, 0, 0, 0, math.sqrt(2), 0]))

def test_months():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('May 2012',
                                                'June 2013'),
        np.array([1, 0, 0, 1, 0, 0, math.sqrt(13), 0, 0]))

def test_days():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('5 May 2013',
                                                '9 June 2013'),
        np.array([1, 0, 1, 0, 0, math.sqrt(35), 0, 0, 0]))

def test_alternate_formats():
    dt = DateTimeType({'field': 'foo'})
    comp = dt.comparator('May 5th, 2013','2013-06-09')
    np.testing.assert_almost_equal(comp,
        np.array([1, 0, 1, 0, 0, math.sqrt(35), 0, 0, 0]))

    np.testing.assert_almost_equal(dt.comparator('11am May 5th, 2013',
                                                'June 9th 2013'),
        np.array([1, 0, 1, 0, 0, math.sqrt(34), 0, 0, 0]))

    np.testing.assert_almost_equal(dt.comparator('5/5/2013',
                                         '6/9/2013'),
                            dt.comparator('May 5th, 2013',
                                         '2013-06-09'))

def test_bad_parse():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('foo',
                                                'bar'),
        np.array([1, 0, 0, 0, 0, 0, 0, 0, 5.5]))

    assert len(dt.comparator('foo', 'bar') == len(dt.higher_vars))

def test_missing():
    dt = DateTimeType({'field': 'foo'})
    np.testing.assert_almost_equal(dt.comparator('', 'non-empty'),
                            np.zeros(len(dt)))
