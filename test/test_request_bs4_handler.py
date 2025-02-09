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
#                   PyUnit Tests for nholuongut.RequestBS4Handler
# ============================================================================ #
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# from __future__ import unicode_literals

import logging
import os
import sys
import unittest
# inspect.getfile(inspect.currentframe()) # filename
import requests
libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(libdir)
# pylint: disable=wrong-import-position
from nholuongut.utils import log
from nholuongut import RequestBS4Handler


class RequestBS4HandlerTester(unittest.TestCase):

    # must prefix with test_ in order for the tests to be called

    # Not using assertRaises >= 2.7 and maintaining compatibility with Python 2.6 servers

    class SubRequestBS4Handler(RequestBS4Handler):
        def parse(self, soup):
            pass

    # TODO: mock this
    def test_request_bs4_handler(self):
        req = self.SubRequestBS4Handler().get('www.travis-ci.com')
        self.assertTrue(isinstance, requests.Response)
        self.SubRequestBS4Handler(req)


def main():
    # increase the verbosity
    # verbosity Python >= 2.7
    #unittest.main(verbosity=2)
    log.setLevel(logging.DEBUG)
    suite = unittest.TestLoader().loadTestsFromTestCase(RequestBS4HandlerTester)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    main()
