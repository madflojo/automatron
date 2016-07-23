'''
Test plugins/discovery/digitalocean/__init__.py Discovery() class
'''

import mock
import unittest

from plugins.discovery.digitalocean import Discover

class ResponseMock:
    ''' Mocked Class for requests '''
    def __init__(self, text, status_code, errors=None):
        self.text = text
        self.status_code = status_code

        if errors == True:
            raise Exception("Unit testing is good")

def mocked_get_success(*args, **kwargs):
    ''' Run with example json from DO docs '''
    response = """
        {
          "droplets": [
            {
              "id": 3164444,
              "name": "example.com",
              "memory": 512,
              "vcpus": 1,
              "disk": 20,
              "locked": false,
              "status": "active",
              "kernel": {
                "id": 2233,
                "name": "Ubuntu 14.04 x64 vmlinuz-3.13.0-37-generic",
                "version": "3.13.0-37-generic"
              },
              "created_at": "2014-11-14T16:29:21Z",
              "features": [
                "backups",
                "ipv6",
                "virtio"
              ],
              "backup_ids": [
                7938002
              ],
              "snapshot_ids": [

              ],
              "image": {
                "id": 6918990,
                "name": "14.04 x64",
                "distribution": "Ubuntu",
                "slug": "ubuntu-14-04-x64",
                "public": true,
                "regions": [
                  "nyc1",
                  "ams1",
                  "sfo1",
                  "nyc2",
                  "ams2",
                  "sgp1",
                  "lon1",
                  "nyc3",
                  "ams3",
                  "nyc3"
                ],
                "created_at": "2014-10-17T20:24:33Z",
                "type": "snapshot",
                "min_disk_size": 20,
                "size_gigabytes": 2.34
              },
              "volumes": [

              ],
              "size": {
              },
              "size_slug": "512mb",
              "networks": {
                "v4": [
                  {
                    "ip_address": "104.236.32.182",
                    "netmask": "255.255.192.0",
                    "gateway": "104.236.0.1",
                    "type": "public"
                  }
                ],
                "v6": [
                  {
                    "ip_address": "2604:A880:0800:0010:0000:0000:02DD:4001",
                    "netmask": 64,
                    "gateway": "2604:A880:0800:0010:0000:0000:0000:0001",
                    "type": "public"
                  }
                ]
              },
              "region": {
                "name": "New York 3",
                "slug": "nyc3",
                "sizes": [

                ],
                "features": [
                  "virtio",
                  "private_networking",
                  "backups",
                  "ipv6",
                  "metadata"
                ],
                "available": null
              },
              "tags": [

              ]
            }
          ],
          "links": {
            "pages": {
              "last": "https://api.digitalocean.com/v2/droplets?page=3&per_page=1",
              "next": "https://api.digitalocean.com/v2/droplets?page=2&per_page=1"
            }
          },
          "meta": {
            "total": 3
          }
        }
    """
    return_code = 200
    return ResponseMock(response, return_code)

def mocked_get_bad_json(*args, **kwargs):
    ''' Run with bad json from DO docs '''
    response = """
        {asdfasdjaflsdjflksj}
    """
    return_code = 200
    return ResponseMock(response, return_code)

def mocked_get_no_json(*args, **kwargs):
    ''' Run with no json from DO docs '''
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
        self.config = mock.Mock()
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
    ''' Test with valid reply from DO '''
    @mock.patch('plugins.discovery.digitalocean.requests.get', side_effect=mocked_get_success)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'digitalocean' : {
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
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertTrue(self.dbc.new_discovery.called, "dbc.new_discovery was not called")
        self.assertEqual(
            self.dbc.new_discovery.call_count,
            2,
            "dbc.new_discovery was not called twice"
        )

class RunwithInValidJSON(DiscoveryTest):
    ''' Test with invalid JSON reply from DO '''
    @mock.patch('plugins.discovery.digitalocean.requests.get', side_effect=mocked_get_bad_json)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'digitalocean' : {
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
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithNoJSON(DiscoveryTest):
    ''' Test with invalid reply from DO '''
    @mock.patch('plugins.discovery.digitalocean.requests.get', side_effect=mocked_get_no_json)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'digitalocean' : {
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
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithStatusError(DiscoveryTest):
    ''' Test with error reply from DO '''
    @mock.patch('plugins.discovery.digitalocean.requests.get', side_effect=mocked_get_status_error)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'digitalocean' : {
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
        self.dbc = mock.MagicMock(**{
            'new_discovery.return_value' : True
        })
        find = Discover(config=self.config, dbc=self.dbc)
        self.assertTrue(find.start())
        self.assertFalse(self.dbc.new_discovery.called, "dbc.new_discovery was called in error")

class RunwithException(DiscoveryTest):
    ''' Test with error reply from DO '''
    @mock.patch('plugins.discovery.digitalocean.requests.get', side_effect=mocked_get_raise)
    def runTest(self, mock_get):
        ''' Execute test '''
        self.config = {
            'discovery' : {
                'plugins' : {
                    'digitalocean' : {
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
