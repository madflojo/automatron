'''
Test plugins/discovery/roster/__init__.py Discovery() class
'''

import mock
import unittest

from plugins.discovery.roster import Discover

class DiscoveryTest(unittest.TestCase):
    ''' Run unit tests against the Discovery() class '''

    def setUp(self):
        ''' Setup mocked data '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'roster' : {
                        'hosts': ['10.0.0.1', '10.0.0.2']
                    }
                }
            },
            'unit_testing': True,
            'logging' : {
                'debug' : True,
                'plugins' : {
                    'console' : True
                }
            }
        }
        self.logger = mock.Mock(**{
            'info.return_value' : True,
            'debug.return_value' : True,
            'critical.return_value' : True,
            'warn.return_value' : True,
            'error.return_value' : True
        })
        self.dbc = mock.Mock()

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.logger = None
        self.dbc = None

class RunwithValidHosts(DiscoveryTest):
    ''' Test with valid reply '''
    def runTest(self):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertTrue(self.dbc.new_discovery.called, "dbc.new_discovery was not called")
        self.assertEqual(
            self.dbc.new_discovery.call_count,
            2,
            "dbc.new_discovery call count is not 2: {0}".format(self.dbc.new_discovery.call_count)
        )

class RunwithNoHosts(DiscoveryTest):
    ''' Test with valid reply '''
    def runTest(self):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        # Set hosts list to an empty list
        self.config['discovery']['plugins']['roster']['hosts'] = []
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithNoHostsKey(DiscoveryTest):
    ''' Test with invalid JSON reply '''
    def runTest(self):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        # Remove hosts key
        self.config['discovery']['plugins']['roster'] = {'interval': 30}
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")
