'''
Test actioning.py execute_runbook()
'''

import mock
import unittest

from actioning import execute_runbook
import actioning


class ExecuteRunbooksTest(unittest.TestCase):
    ''' Run unit tests against the execute_runbook method '''

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
        self.target = {'ip' : '10.0.0.1'}

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.dbc = None
        self.logger = None
        self.target = None

class TestCMDonRemote(ExecuteRunbooksTest):
    ''' Test when the action is a command from Remote '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'cmd',
            'execute_from' : 'remote',
            'cmd' : "bash"
        }
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertTrue(results)
        self.assertFalse(self.logger.warn.called)
        self.assertTrue(mock_local.called)
        mock_local.assert_called_with("bash", capture=True)

class TestCMDonTarget(ExecuteRunbooksTest):
    ''' Test when the action is a command from Remote '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'cmd',
            'execute_from' : 'ontarget',
            'cmd' : "bash"
        }
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertTrue(results)
        self.assertFalse(self.logger.warn.called)
        self.assertFalse(mock_local.called)
        self.assertTrue(mock_run.called)
        mock_run.assert_called_with("bash")

class TestCMDWithBadTarget(ExecuteRunbooksTest):
    ''' Test when the action is a command from Remote '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'cmd',
            'execute_from' : 'flarget',
            'cmd' : "bash"
        }
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertFalse(results)
        self.assertTrue(self.logger.warn.called)

class TestPluginonRemote(ExecuteRunbooksTest):
    ''' Test when the action is a Plugin on Remote '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'plugin',
            'plugin' : 'yes.py',
            'args' : 'arrrrrgs',
            'execute_from' : 'ontarget',
        }
        config = {
            'plugin_path' : '/some/dir',
            'actioning' : {
                'upload_path' : '/some/dir'
            }
        }
        self.config = mock.MagicMock(spec_set=config)
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertTrue(results)
        self.assertFalse(self.logger.warn.called)
        self.assertFalse(mock_local.called)
        self.assertTrue(mock_run.called)
        self.assertTrue(mock_run.call_count == 3)

class TestPluginonTarget(ExecuteRunbooksTest):
    ''' Test when the action is a Plugin on Target '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'plugin',
            'plugin' : 'yes.py',
            'args' : 'arrrrrgs',
            'execute_from' : 'remote',
        }
        config = {
            'plugin_path' : '/some/dir',
            'actioning' : {
                'upload_path' : '/some/dir'
            }
        }
        self.config = mock.MagicMock(spec_set=config)
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertTrue(results)
        self.assertFalse(self.logger.warn.called)
        self.assertFalse(mock_run.called)
        self.assertTrue(mock_local.called)
        self.assertTrue(mock_local.call_count == 1)

class TestPluginBadTarget(ExecuteRunbooksTest):
    ''' Test when the action is a Plugin on an invalid target '''
    @mock.patch('actioning.core.fab.set_env')
    @mock.patch('actioning.fabric.api.env')
    @mock.patch('actioning.fabric.api.hide')
    @mock.patch('actioning.fabric.api.local')
    @mock.patch('actioning.fabric.api.put')
    @mock.patch('actioning.fabric.api.run')
    def runTest(self, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        # Set mock_env to empty dict
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put = True
        mock_hide = True
        action = {
            'type' : 'plugin',
            'plugin' : 'yes.py',
            'args' : 'arrrrrgs',
            'execute_from' : 'plarget',
        }
        config = {
            'plugin_path' : '/some/dir',
            'actioning' : {
                'upload_path' : '/some/dir'
            }
        }
        self.config = mock.MagicMock(spec_set=config)
        results = execute_runbook(action, self.target, self.config, self.logger)
        self.assertFalse(results)
        self.assertTrue(self.logger.warn.called)
