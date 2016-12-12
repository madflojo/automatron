'''
Test Runbooks.py render_runbooks()
'''

import mock
import unittest

from runbooks import render_runbooks


class RenderRunbooksIntegrationTest(unittest.TestCase):
    ''' Run unit tests against the cache_runbooks method '''

    def setUp(self):
        ''' Setup mocked data '''
        self.runbooks = """
            yaml: {{facts['data']}}
        """
        self.facts = {'data': True}

    def tearDown(self):
        ''' Destroy mocked data '''
        self.runbooks = None
        self.facts = None

class RunwithGoodData(RenderRunbooksIntegrationTest):
    ''' Test when given good data '''
    def runTest(self):
        ''' Execute test '''
        self.assertEqual(render_runbooks(self.runbooks, self.facts), {'yaml': True})

class RunwithNoData(RenderRunbooksIntegrationTest):
    ''' Test when given no data '''
    def runTest(self):
        ''' Execute test '''
        self.runbooks = ""
        self.facts = ""
        self.assertIsNone(render_runbooks(self.runbooks, self.facts))

class RunwithBadData(RenderRunbooksIntegrationTest):
    ''' Test when given bad data '''
    def runTest(self):
        ''' Execute test '''
        self.runbooks = "notrealyaml"
        # Output should be same as input
        self.assertEqual(render_runbooks(self.runbooks, self.facts), "notrealyaml")
