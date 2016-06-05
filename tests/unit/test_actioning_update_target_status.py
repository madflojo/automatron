'''
Test actioning.py update_target_status()
'''

import mock
import unittest

from actioning import update_target_status
import actioning


class UpdateTargetStatusTest(unittest.TestCase):
    ''' Run unit tests against the update_target_status method '''

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
        self.item = {
            'runbook' : 'book1',
            'checks' : {
            }
        }
        self.target = {
            'runbooks' : {
                'book1' : {
                    'status': {
                        'OK' : 0,
                        'WARNING' : 0,
                        'CRITICAL' : 0,
                        'UNKNOWN' : 0
                    }
                }
            }
        }

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.dbc = None
        self.logger = None
        self.item = None
        self.target = None

class TestWithNoChecks(UpdateTargetStatusTest):
    ''' Test when there are no messages '''
    def runTest(self):
        ''' Execute test '''
        returned_target = update_target_status(self.item, self.target)
        self.assertTrue(returned_target['runbooks']['book1']['status']['CRITICAL'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['OK'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['WARNING'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['UNKNOWN'] == 0)

class TestWith1CriticalFail(UpdateTargetStatusTest):
    ''' Test when there are no messages '''
    def runTest(self):
        ''' Execute test '''
        self.item['checks'].update({
            'fails' : 'CRITICAL'
        })
        returned_target = update_target_status(self.item, self.target)
        self.assertTrue(returned_target['runbooks']['book1']['status']['CRITICAL'] == 1)
        self.assertTrue(returned_target['runbooks']['book1']['status']['OK'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['WARNING'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['UNKNOWN'] == 0)


class TestWith1OK(UpdateTargetStatusTest):
    ''' Test when there are no messages '''
    def runTest(self):
        ''' Execute test '''
        self.item['checks'].update({
            'fails' : 'OK'
        })
        returned_target = update_target_status(self.item, self.target)
        self.assertTrue(returned_target['runbooks']['book1']['status']['OK'] == 1)
        self.assertTrue(returned_target['runbooks']['book1']['status']['CRITICAL'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['WARNING'] == 0)
        self.assertTrue(returned_target['runbooks']['book1']['status']['UNKNOWN'] == 0)
