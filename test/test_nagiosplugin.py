#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Nho Luong
#  Date: 2014-09-15 20:49:22 +0100 (Mon, 15 Sep 2014)
#
#  https://github.com/nholuongut/pylib
#
#  License: see accompanying Nho Luong LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback
#  to help improve or steer this or other code I publish
#
#  https://www.linkedin.com/in/nholuong
#

"""
# ============================================================================ #
#                   PyUnit Tests for nholuongut.NagiosPlugin
# ============================================================================ #
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import sys
import unittest
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(libdir)
# pylint: disable=wrong-import-position
from nholuongut.utils import log, CodingError
from nholuongut import NagiosPlugin
from nholuongut.nagiosplugin import Threshold

class NagiosPluginTester(unittest.TestCase):

    # must prefix with test_ in order for the tests to be called

    # Not using assertRaises >= 2.7 and maintaining compatibility with Python 2.6 servers

    class SubNagiosPlugin(NagiosPlugin):
        def __init__(self):
            # Python 2.x
            #NagiosPlugin.__init__(self)
            super(NagiosPluginTester.SubNagiosPlugin, self).__init__()
            # Python 3.x
            # super().__init__()
            self.name = 'test'
            self.percentage = True
            self.default_warning = 1
            self.default_critical = 2
        def run(self):
            print("running SubNagiosPlugin()")

    def setUp(self):
        self.plugin = self.SubNagiosPlugin()

    def test_threshold(self):
        self.plugin.set_threshold('test', Threshold(5))
        self.assertTrue(isinstance(self.plugin.get_threshold('test'), Threshold))

    def test_set_threshold_invalid(self):
        try:
            self.plugin.set_threshold('test', 5)
            raise AssertionError('failed to raise CodingError on passing in non-threshold object to Threshold.set_threshold()') # pylint: disable=line-too-long
        except CodingError:
            pass

    def test_get_threshold_nonexistent(self):
        try:
            self.plugin.get_threshold('nonexistent')
            raise AssertionError('failed to raise CodingError for Threshold.get_threshold(nonexistent)')
        except CodingError:
            pass

    # def test_get_threshold_none(self):
    #     self.plugin.set_threshold('setToNone', Threshold(None))
    #     try:
    #         self.plugin.get_threshold('setToNone')
    #         raise AssertionError('failed to raise CodingError for Threshold.get_threshold(setToNone)')
    #     except CodingError:
    #         pass

    def test_add_thresholds(self):
        self.plugin.add_thresholds()
        self.plugin.add_thresholds('test')

    def test_add_thresholds_nonstring_name_exception(self):
        try:
            self.plugin.add_thresholds(None)
            raise AssertionError('failed to raise exception when passing None to add_thresholds()')
        except CodingError:
            pass

    def test_validate_threshold(self):
        self.assertEqual(self.plugin.validate_threshold('warning', threshold=4, optional=False), None)
        self.assertTrue(isinstance(self.plugin.get_threshold('warning'), Threshold))

    def test_validate_threshold_not_set_exception(self):
        try:
            self.assertEqual(self.plugin.validate_threshold('nonexistent'), None)
            raise AssertionError('failed to raise CodingError when threshold is not set')
        except CodingError:
            pass

    def test_validate_thresholds(self):
        self.plugin.validate_thresholds('test', 2, 3)
        self.plugin.check_threshold('test_warning', 1)

    # def test_validate_thresholds_nonexistent(self):
    #     try:
    #         self.plugin.validate_thresholds()
    #         raise AssertionError('failed to raise exception for validate_thresholds() when no thresholds set')
    #     except SystemExit as _:
    #         if _.code != 3:
    #             raise AssertionError('invalid exit code raised when thresholds are not set')

    def test_check_thresholds(self):
        try:
            self.plugin.check_thresholds(10, 'nonexistent')
            raise AssertionError('failed to raise exception for check_thresholds() when thresholds are not set')
        except CodingError:
            pass

    def test_check_thresholds_nonstring_name(self):
        try:
            self.plugin.check_thresholds(10, None)
            raise AssertionError('failed to raise exception for check_thresholds() when name is None')
        except CodingError:
            pass

    def test_get_perf_thresholds(self):
        self.assertEqual(self.plugin.get_perf_thresholds(), ';;')

    def test_statuses(self):
        self.assertTrue(self.plugin.is_unknown())
        self.plugin.ok()
        self.assertTrue(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_critical())
        self.assertFalse(self.plugin.is_unknown())
        self.plugin.unknown()
        self.assertTrue(self.plugin.is_unknown())
        self.assertFalse(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_critical())
        self.plugin.warning()
        self.assertTrue(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_critical())
        self.assertFalse(self.plugin.is_unknown())
        self.plugin.unknown()
        self.assertTrue(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_critical())
        self.assertFalse(self.plugin.is_unknown())
        self.plugin.critical()
        self.assertTrue(self.plugin.is_critical())
        self.assertFalse(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_unknown())
        self.plugin.warning()
        self.assertTrue(self.plugin.is_critical())
        self.assertFalse(self.plugin.is_ok())
        self.assertFalse(self.plugin.is_warning())
        self.assertFalse(self.plugin.is_unknown())

    def test_invalid_status(self):
        try:
            self.plugin.status = 'invalidstatus'
        except CodingError:
            pass

    def test_main_unhandled_exception(self):
        def raise_exception():
            raise AssertionError('this is an unhandled exception to be caught')
        self.plugin.run = raise_exception
        try:
            self.plugin.main()
            raise AssertionError('failed to exit on unhandled exception')
        except SystemExit as _:
            if _.code != 3:
                raise AssertionError('failed to exit with code 3 upon unhandled exception')
            # if _.message[:7] != 'UNKNOWN':
            #     raise AssertionError('unhandled exception failed to add UNKNOWN prefix')


    def test_critical_exit(self):
        try:
            self.plugin.critical()
            self.plugin.main()
            raise AssertionError('plugin failed to terminate')
        except SystemExit as _:
            if _.code != 2:
                raise AssertionError('NagiosPlugin failed to exit CRITICAL (2), got exit code {0} instead'\
                                     .format(_.code))

    def test_nagiosplugin_abstract(self): # pylint: disable=no-self-use
        try:
            NagiosPlugin() # pylint: disable=abstract-class-instantiated
            # broken in Python 3
            #raise AssertionError('failed to raise a TypeError when attempting ' +
            #                      'to instantiate abstract class NagiosPlugin')
        except TypeError as _:  # only seems to enforce abstract type error in Python 2
            pass


def main():
    # increase the verbosity
    # verbosity Python >= 2.7
    #unittest.main(verbosity=2)
    log.setLevel(logging.DEBUG)
    suite = unittest.TestLoader().loadTestsFromTestCase(NagiosPluginTester)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
