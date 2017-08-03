'''
Test Runbooks.py cache_runbooks()
'''

import mock
import unittest

from runbooks import cache_runbooks


class CacheRunbooksTest(unittest.TestCase):
    ''' Run unit tests against the cache_runbooks method '''

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

    def tearDown(self):
        ''' Destroy mocked data '''
        self.config = None
        self.logger = None

class RunwithNoFile(CacheRunbooksTest):
    ''' Test when no init.yml file is found '''
    @mock.patch('runbooks.open', create=True)
    @mock.patch('runbooks.os.path.isfile')
    @mock.patch('runbooks.yaml.load')
    def runTest(self, mock_yaml, mock_isfile, mock_open):
        ''' Execute test '''
        self.config = mock.MagicMock(spec_set={'runbook_path' : '/path/'})
        mock_isfile.return_value = False
        mock_yaml.return_value = None
        self.assertEqual(cache_runbooks(self.config, self.logger), {})
        self.assertFalse(mock_open.called)

class RunwithEmptyFile(CacheRunbooksTest):
    ''' Test with empty init.yml file '''
    @mock.patch('runbooks.open', create=True)
    @mock.patch('runbooks.os.path.isfile')
    @mock.patch('runbooks.yaml.load')
    @mock.patch('runbooks.Template')
    def runTest(self, mock_template, mock_yaml, mock_isfile, mock_open):
        ''' Execute test '''
        self.config = mock.MagicMock(spec_set={'runbook_path' : '/path/'})
        mock_isfile.return_value = True
        mock_yaml.return_value = None
        mock_template = mock.MagicMock(**{
            'render.return_value' : ""
        })
        mock_open.return_value = mock.MagicMock(spec=file)
        self.assertEqual(cache_runbooks(self.config, self.logger), {})
        self.assertTrue(mock_open.called)
        self.assertTrue(mock_yaml.called)

class RunwithNoBooks(CacheRunbooksTest):
    ''' Test with a partially created init.yml file '''
    @mock.patch('runbooks.open', create=True)
    @mock.patch('runbooks.os.path.isfile')
    @mock.patch('runbooks.yaml.load')
    @mock.patch('runbooks.Template')
    def runTest(self, mock_template, mock_yaml, mock_isfile, mock_open):
        ''' Execute test '''
        self.config = mock.MagicMock(spec_set={'runbook_path' : '/path/'})
        mock_isfile.return_value = True
        mock_yaml.return_value = None
        mock_template = mock.MagicMock(**{
            'render.return_value' : { '*': None }
        })
        mock_open.return_value = mock.MagicMock(spec=file)
        self.assertEqual(cache_runbooks(self.config, self.logger), {})
        self.assertTrue(mock_open.called)
        self.assertTrue(mock_yaml.called)

class RunwithYMLFile(CacheRunbooksTest):
    ''' Test with a valid YML file '''
    @mock.patch('runbooks.open', create=True)
    @mock.patch('runbooks.os.path.isfile')
    @mock.patch('runbooks.os.path.isdir')
    @mock.patch('runbooks.yaml.load')
    @mock.patch('runbooks.Template')
    def runTest(self, mock_template, mock_yaml, mock_isdir, mock_isfile, mock_open):
        ''' Execute test '''
        self.config = mock.MagicMock(spec_set={'runbook_path' : '/path/'})
        mock_isfile.return_value = True
        mock_isdir.return_value = True
        mock_template = mock.MagicMock(**{
            'render.return_value' : """
                '*':
                  - book
                'target':
                  - book1
                  - book2
            """
        })
        mock_yaml.return_value = {'*':['book'], 'target':['book1', 'book2']}
        mock_open.return_value = mock.MagicMock(spec=file)
        result = cache_runbooks(self.config, self.logger)
        self.assertEqual(result.keys(), ['*', 'target'], "Expected dictionary keys not found")
        self.assertTrue(mock_open.called, "open not called")
        self.assertTrue(mock_yaml.called, "yaml.safe_load not called")
        self.assertTrue(mock_isdir.called, "os.path.isdir not called")
        self.assertEqual(mock_isfile.call_count, 4,
            "mock_open.call_count {0} is not 4".format(mock_open.call_count))
