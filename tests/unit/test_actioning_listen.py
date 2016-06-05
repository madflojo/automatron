'''
Test actioning.py listen()
'''

import mock
import unittest

from actioning import listen
import actioning


class ListenTest(unittest.TestCase):
    ''' Run unit tests against the Listen method '''

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

class TestWithNoMsgs(ListenTest):
    ''' Test when there are no messages '''
    def runTest(self):
        ''' Execute test '''
        self.config = mock.Mock()
        pubsub = mock.MagicMock(**{
            'listen.return_value': []
        })
        attr = {
            'subscribe.return_value' : pubsub,
            'get_target.return_value' : None,
        }
        self.dbc.configure_mock(**attr)
        listen(self.config, self.dbc, self.logger)
        self.assertFalse(self.dbc.get_target.called)

class TestWithBadMsgs(ListenTest):
    ''' Test when messages are returned but are unparseable '''
    def runTest(self):
        ''' Execute test '''
        self.config = mock.Mock()
        pubsub = mock.MagicMock(**{
            'listen.return_value': ['{"bad":true}', '{"stillbad":true}']
        })
        attr = {
            'subscribe.return_value' : pubsub,
            'get_target.return_value' : False,
            'save_target.return_value' : False,
            'process_subscription.return_value' : {"junk" : True}
        }
        self.dbc.configure_mock(**attr)
        listen(self.config, self.dbc, self.logger)
        self.assertFalse(self.dbc.save_target.called)
        self.assertTrue(self.logger.warn.called)

class TestWithGoodMsgs(ListenTest):
    ''' Test when messages are returned and are good '''
    @mock.patch('actioning.update_target_status')
    @mock.patch('actioning.get_runbooks_to_exec')
    @mock.patch('actioning.execute_runbook')
    def runTest(self, mock_execute_runbook, mock_get_runbooks_to_exec, mock_update_target_status):
        ''' Execute test '''
        self.config = mock.Mock()
        pubsub = mock.MagicMock(**{
            'listen.return_value': [
                """
                {
                    'msg_type': 'test message',
                    'target': 'localhost',
                    'runbook': 'runbook'
                }
                """
            ]
        })
        target = {
            'hostname': 'localhost',
            'runbooks': {
                'book1': {
                    'actions' : {
                        'action1' : {
                            'last_run' : 0
                        }
                    },
                    'status' : {
                        'WARNING' : 0,
                    }
                }
            }
        }
        item = {
            'msg_type': 'test message',
            'target': 'localhost',
            'runbook': 'book1'
        }
        mock_update_target_status.return_value = target
        mock_get_runbooks_to_exec.return_value = {'book1' : [ 'action1']}
        mock_execute_runbook.return_value = True
        attr = {
            'subscribe.return_value' : pubsub,
            'get_target.return_value' : target,
            'save_target.return_value' : target,
            'process_subscription.return_value' : item,
        }
        self.dbc.configure_mock(**attr)
        listen(self.config, self.dbc, self.logger)
        self.assertFalse(self.logger.warn.called)
        self.assertTrue(self.dbc.save_target.called)
        self.assertEqual(self.dbc.save_target.call_count, 2)
        self.assertTrue(mock_update_target_status.called)
        self.assertTrue(mock_get_runbooks_to_exec.called)
        self.assertTrue(mock_execute_runbook.called)
        mock_get_runbooks_to_exec.assert_called_with(item, target, self.logger)
