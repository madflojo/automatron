'''
Test plugins/discovery/linode/__init__.py Discovery() class
'''

import mock
import unittest

from plugins.discovery.linode import Discover

class ResponseMock:
    ''' Mocked Class for requests '''
    def __init__(self, text, status_code, errors=None):
        self.text = text
        self.status_code = status_code

        if errors == True:
            raise Exception("Unit testing is good")

def mocked_get_success(*args, **kwargs):
    ''' Run with example json from API docs '''
    response = """
        {
           "ERRORARRAY":[],
           "ACTION":"linode.ip.list",
           "DATA":[
              {
                 "LINODEID":8098,
                 "ISPUBLIC":1,
                 "IPADDRESS":"75.127.96.54",
                 "RDNS_NAME":"li22-54.members.linode.com",
                 "IPADDRESSID":5384
              },
              {
                 "LINODEID":8099,
                 "ISPUBLIC":1,
                 "IPADDRESS":"75.127.96.245",
                 "RDNS_NAME":"li22-245.members.linode.com",
                 "IPADDRESSID":5575
              }
           ]
        }
    """
    return_code = 200
    return ResponseMock(response, return_code)

def mocked_get_bad_json(*args, **kwargs):
    ''' Run with bad json from API docs '''
    response = """
        {asdfasdjaflsdjflksj}
    """
    return_code = 200
    return ResponseMock(response, return_code)

def mocked_get_no_json(*args, **kwargs):
    ''' Run with no json from API docs '''
    response = ""
    return_code = 200
    return ResponseMock(response, return_code)

def mocked_get_status_error(*args, **kwargs):
    ''' Run with Status Code Error '''
    response = ""
    return_code = 400
    return ResponseMock(response, return_code)

def mocked_get_raise(*args, **kwargs):
    ''' Run with Exception '''
    return ResponseMock("", 400, errors=True)

class DiscoveryTest(unittest.TestCase):
    ''' Run unit tests against the Discovery() class '''

    def setUp(self):
        ''' Setup mocked data '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'linode' : {
                        'url': 'https://example.com/',
                        'api_key': 'executing_unit_test',
                        'interval': '1'
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

class RunwithValidReply(DiscoveryTest):
    ''' Test with valid reply '''
    @mock.patch('plugins.discovery.linode.requests.get', side_effect=mocked_get_success)
    def runTest(self, mock_get):
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

class RunwithInValidJSON(DiscoveryTest):
    ''' Test with invalid JSON reply '''
    @mock.patch('plugins.discovery.linode.requests.get', side_effect=mocked_get_bad_json)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithNoJSON(DiscoveryTest):
    ''' Test with invalid reply '''
    @mock.patch('plugins.discovery.linode.requests.get', side_effect=mocked_get_no_json)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithStatusError(DiscoveryTest):
    ''' Test with error reply '''
    @mock.patch('plugins.discovery.linode.requests.get', side_effect=mocked_get_status_error)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithException(DiscoveryTest):
    ''' Test with error reply '''
    @mock.patch('plugins.discovery.linode.requests.get', side_effect=mocked_get_raise)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        try:
            find.start()
        except Exception as e:
            if "Unit testing" in e.message:
                return True
            else:
                raise Exception(e.message)
        raise Exception("Unit test failed to create exception")
