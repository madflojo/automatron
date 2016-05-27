'''
Test Runbooks.py rediscover()
'''

import mock
import unittest

from runbooks import rediscover


class RediscoverTest(unittest.TestCase):
    ''' Run unit tests against the Rediscover method '''

    def setUp(self):
        ''' Setup mocked data '''
        self.config = mock.Mock()
        self.dbc = mock.Mock()
        self.logger = mock.Mock(**{
            'info.return_value' : True,
            'debug.return_value' : True,
            'critical.return_value' : True,
            'warn.return_value' : True,
            'error.return_value' : True
        })

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.dbc = None
        self.logger = None

class RunwithNoTargets(RediscoverTest):
    ''' Test when no targets are found in Redis '''
    def runTest(self):
        ''' Execute test '''
        self.config = mock.Mock()
        attr = {
            'pop_target.return_value' :{},
            'new_discovery.return_value' : True
        }
        self.dbc.configure_mock(**attr)
        self.assertEqual(rediscover(self.config, self.dbc, self.logger), 0)


class RunwithBasicTargets(RediscoverTest):
    ''' Test with a basic Target dictionary '''
    def runTest(self):
        ''' Execute test '''
        self.config = mock.Mock()
        attr = {
            'pop_target.return_value' :{
                'target1' : { 'ip' : "127.0.0.1" },
                'target2' : { 'ip' : "127.0.0.1" },
            },
            'new_discovery.return_value' : True
        }
        self.dbc.configure_mock(**attr)
        self.assertEqual(rediscover(self.config, self.dbc, self.logger), 2)
        self.assertTrue(self.dbc.new_discovery.called, "Function new_discovery was not called")



class RunwithFailedNewDiscoveryCall(RediscoverTest):
    ''' Test with a Failed call to New Discovery '''
    def runTest(self):
        ''' Execute test '''
        self.config = mock.Mock()
        attr = {
            'pop_target.return_value' :{
                'target1' : { 'ip' : "127.0.0.1" },
                'target2' : { 'ip' : "127.0.0.1" },
            },
            'new_discovery.side_effect' : Exception
        }
        self.dbc.configure_mock(**attr)
        self.assertEqual(rediscover(self.config, self.dbc, self.logger), 0)
