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
#                   PyUnit Tests for nholuongut.DeadNodesNagiosPlugin
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
from nholuongut.utils import log
from nholuongut.nagiosplugin import DeadNodesNagiosPlugin

class DeadNodesNagiosPluginTester(unittest.TestCase):

    # must prefix with test_ in order for the tests to be called

    # Not using assertRaises >= 2.7 and maintaining compatibility with Python 2.6 servers

    class SubDeadNodesNagiosPlugin(DeadNodesNagiosPlugin):
        def __init__(self):
            # Python 2.x
            #DeadNodesNagiosPlugin.__init__(self)
            super(DeadNodesNagiosPluginTester.SubDeadNodesNagiosPlugin, self).__init__()
            # Python 3.x
            # super().__init__()
            self.name = 'test'
            self.default_port = 80
        def get_nodecount(self):
            print("running SubDeadNodesNagiosPlugin().get_nodecount()")
            return 0

    #def setUp(self):
        #self.plugin = self.SubDeadNodesNagiosPlugin()

    def test_exit_0(self):
        plugin = self.SubDeadNodesNagiosPlugin()
        try:
            plugin.main()
            raise AssertionError('DeadNodes plugin failed to terminate')
        except SystemExit as _:
            if _.code != 0:
                raise AssertionError('DeadNodesNagiosPlugin failed to exit OK (0), got exit code {0} instead'
                                     .format(_.code))

    def test_exit_2(self):
        plugin = self.SubDeadNodesNagiosPlugin()
        plugin.get_nodecount = lambda: 2
        try:
            plugin.main()
            raise AssertionError('DeadNodes plugin failed to terminate')
        except SystemExit as _:
            if _.code != 2:
                raise AssertionError('DeadNodesNagiosPlugin failed to exit CRITICAL (2), got exit code {0} instead'
                                     .format(_.code))

    def test_plugin_abstract(self):  # pylint: disable=no-self-use
        try:
            DeadNodesNagiosPlugin()  # pylint: disable=abstract-class-instantiated
            # broken in Python 3
            #raise AssertionError('failed to raise a TypeError when attempting to instantiate abstract class ' +
            #                     'DeadNodesNagiosPlugin')
        except TypeError as _:  # only seems to enforce abstract type error in Python 2
            pass


def main():
    # increase the verbosity
    # verbosity Python >= 2.7
    #unittest.main(verbosity=2)
    log.setLevel(logging.DEBUG)
    suite = unittest.TestLoader().loadTestsFromTestCase(DeadNodesNagiosPluginTester)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
