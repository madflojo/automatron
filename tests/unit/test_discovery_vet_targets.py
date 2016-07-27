'''
Test discovery.py vet_targets()
'''

import mock
import unittest

from discovery import vet_targets
import discovery
import threading

class VetTargetsTest(unittest.TestCase):
    ''' Run unit tests against the vet_targets method '''

    def setUp(self):
        ''' Setup mocked data '''
        self.config = {
            'discovery' : {
                'vetting_interval': 30,
            },
            'plugin_path' : {
                '/bla/'
            },
            'unit-testing' : True,
        }
        self.dbc = mock.Mock()
        self.logger = mock.Mock(**{
            'info.return_value' : True,
            'debug.return_value' : True,
            'critical.return_value' : True,
            'warn.return_value' : True,
            'error.return_value' : True
        })
        self.target = {'ip' : '10.0.0.1', 'hostname' : 'localhost'}

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.dbc = None
        self.logger = None
        self.target = None

class TestFoundHost(VetTargetsTest):
    ''' Test when a target host is already found '''
    @mock.patch('discovery.os.listdir')
    def runTest(self, mock_listdir):
        ''' Execute test '''
        attr = {
            'discovery_queue.return_value' : ['10.0.0.1'],
            'get_target.return_value': self.target,
            'pop_discovery.return_value': True,
            'save_target.return_value' : False
        }
        self.dbc.configure_mock(**attr)
        vet_targets(self.config, self.dbc, self.logger)
        self.assertFalse(mock_listdir.called)
        self.assertTrue(self.dbc.pop_discovery.called)
        self.assertFalse(self.dbc.save_target.called)

class TestNewHostHappyPath(VetTargetsTest):
    ''' Test when a target host is not already found '''
    @mock.patch('discovery.core.fab.set_env')
    @mock.patch('discovery.fabric.api.env')
    @mock.patch('discovery.fabric.api.hide')
    @mock.patch('discovery.fabric.api.local')
    @mock.patch('discovery.fabric.api.put')
    @mock.patch('discovery.fabric.api.run')
    @mock.patch('discovery.os.listdir', create=True)
    def runTest(self, mock_listdir, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': True})
        mock_put.return_value = True
        mock_hide = True
        mock_listdir.return_value = ['plugin.sh']
        attr = {
            'discovery_queue.return_value' : ['10.0.0.1'],
            'get_target.return_value': None,
            'pop_discovery.return_value': True,
            'save_target.return_value' : True,
        }
        self.dbc.configure_mock(**attr)
        self.config = {
            'discovery' : {
                'vetting_interval': 30,
                'upload_path': '/path/'
            },
            'plugin_path' : '/bla/',
            'unit-testing' : True,
        }
        vet_targets(self.config, self.dbc, self.logger)
        self.assertTrue(mock_listdir.called)
        self.assertTrue(mock_local.called)
        self.assertTrue(self.dbc.save_target.called)

class TestNewHostFailPath(VetTargetsTest):
    ''' Test when a target host is already found '''
    @mock.patch('discovery.core.fab.set_env')
    @mock.patch('discovery.fabric.api.env')
    @mock.patch('discovery.fabric.api.hide')
    @mock.patch('discovery.fabric.api.local')
    @mock.patch('discovery.fabric.api.put')
    @mock.patch('discovery.fabric.api.run')
    @mock.patch('discovery.os.listdir', create=True)
    def runTest(self, mock_listdir, mock_run, mock_put, mock_local, mock_hide, mock_env, mock_set_env):
        ''' Execute test '''
        mock_env = mock.MagicMock(spec={})
        mock_set_env.return_value = mock_env
        mock_local.return_value = mock.MagicMock(**{ 'succeeded': False})
        mock_run.return_value = mock.MagicMock(**{ 'succeeded': False})
        mock_put.return_value = False
        mock_hide = True
        mock_listdir.return_value = ['plugin.sh']
        attr = {
            'discovery_queue.return_value' : ['10.0.0.1'],
            'get_target.return_value': None,
            'pop_discovery.return_value': True,
            'save_target.return_value' : True,
        }
        self.dbc.configure_mock(**attr)
        self.config = {
            'discovery' : {
                'vetting_interval': 30,
                'upload_path': '/path/'
            },
            'plugin_path' : '/bla/',
            'unit-testing' : True,
        }
        vet_targets(self.config, self.dbc, self.logger)
        self.assertTrue(mock_listdir.called)
        self.assertTrue(mock_local.called)
        self.assertTrue(self.dbc.save_target.called)
        target = self.target
        target.update({'facts': {}})
        target['hostname'] = "10.0.0.1"
        self.dbc.save_target.assert_called_with(target=target)
