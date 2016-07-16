'''
Test actioning.py get_runbooks_to_exec()
'''

import mock
import unittest

from sets import Set
import time

from actioning import get_runbooks_to_exec
import actioning


class GetRunbooksToExecTest(unittest.TestCase):
    ''' Run unit tests against the get_runbooks_to_exec method '''

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
                'failwhale': 'OK'
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
                    },
                    'actions': {
                    },
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

class TestWithNoActions(GetRunbooksToExecTest):
    ''' Test when there are no actions '''
    def runTest(self):
        ''' Execute test '''
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set([])})

class TestWithNoCallOnMatches(GetRunbooksToExecTest):
    ''' Test when there are no matching actions '''
    def runTest(self):
        ''' Execute test '''
        self.target['runbooks']['book1']['actions'].update({
            'flop': {'call_on': ['WARNING', 'CRITICAL'], 'trigger': 1, 'frequency': 0}
        })
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set([])})

class TestWithCallOnMatches(GetRunbooksToExecTest):
    ''' Test when there are matching actions '''
    def runTest(self):
        ''' Execute test '''
        self.target['runbooks']['book1']['actions'].update({
            'flop': {'call_on': ['OK', 'WARNING', 'CRITICAL'], 'trigger': 1, 'frequency': 0}
        })
        self.target['runbooks']['book1']['status']['OK'] = 1
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set(['flop'])})

class TestWithTriggerNotMet(GetRunbooksToExecTest):
    ''' Test when the trigger requirement is not met '''
    def runTest(self):
        ''' Execute test '''
        self.target['runbooks']['book1']['actions'].update({
            'flop': {'call_on': ['OK', 'WARNING', 'CRITICAL'], 'trigger': 5, 'frequency': 0}
        })
        self.target['runbooks']['book1']['status']['OK'] = 2
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set([])})

class TestWithFrequencyNotMet(GetRunbooksToExecTest):
    ''' Test when the trigger requirement is not met '''
    def runTest(self):
        ''' Execute test '''
        self.target['runbooks']['book1']['actions'].update({
            'flop': {'call_on': ['OK', 'WARNING', 'CRITICAL'], 'trigger': 5, 'frequency': 900,
                'last_run': time.time()}
        })
        self.target['runbooks']['book1']['status']['OK'] = 5
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set([])})

class TestWithFrequencyMet(GetRunbooksToExecTest):
    ''' Test when the trigger requirement is not met '''
    def runTest(self):
        ''' Execute test '''
        self.target['runbooks']['book1']['actions'].update({
            'flop': {'call_on': ['OK', 'WARNING', 'CRITICAL'], 'trigger': 5, 'frequency': 900,
                'last_run': time.time() - 1000}
        })
        self.target['runbooks']['book1']['status']['OK'] = 5
        run_these = get_runbooks_to_exec(self.item, self.target, self.logger)
        self.assertTrue(run_these == {'book1': Set(['flop'])})
