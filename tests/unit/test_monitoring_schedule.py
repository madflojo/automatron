'''
Test monitoring.py schedule()
'''

import mock
import unittest

from monitoring import schedule

class ScheduleTest(unittest.TestCase):
    ''' Run unit tests against the schedule method '''

    def setUp(self):
        ''' Setup mocked data '''
        self.config = {}
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

class TestCronSchedule(ScheduleTest):
    ''' Test when a cron based schedule is provided '''
    @mock.patch('monitoring.CronTrigger')
    @mock.patch('monitoring.fnmatch.fnmatch', new=mock.MagicMock(return_value=True))
    def runTest(self, mock_triggered):
        ''' Execute test '''
        scheduler = mock.Mock(**{
            'add_job.return_value' : True
        })
        self.target.update({
            'runbooks' : {
                'test' : {
                    'schedule' : "* * * * *",
                    'nodes' : [
                        'tes*'
                    ]
                }
            }
        })
        self.assertTrue(schedule(
            scheduler,
            "test",
            self.target,
            self.config,
            self.dbc,
            self.logger))
        self.assertTrue(mock_triggered.called_with(
            minute="*",
            hour="*",
            day="*",
            month="*",
            day_of_week="*"))

class TestSpecificSchedule(ScheduleTest):
    ''' Test when a cron based schedule is provided '''
    @mock.patch('monitoring.CronTrigger')
    @mock.patch('monitoring.fnmatch.fnmatch', new=mock.MagicMock(return_value=True))
    def runTest(self, mock_triggered):
        ''' Execute test '''
        scheduler = mock.Mock(**{
            'add_job.return_value' : True
        })
        self.target.update({
            'runbooks' : {
                'test' : {
                    'schedule' : {
                        'second' : 1,
                        'minute' : 1,
                        'hour' : 1,
                        'day' : 1,
                        'month' : 1,
                        'day_of_week' : 1
                    },
                    'nodes' : [
                        'tes*'
                    ]
                }
            }
        })
        self.assertTrue(schedule(
            scheduler,
            "test",
            self.target,
            self.config,
            self.dbc,
            self.logger))
        self.assertTrue(mock_triggered.called_with(
            second=1,
            minute=1,
            hour=1,
            day=1,
            month=1,
            day_of_week=1))

class TestNoSchedule(ScheduleTest):
    ''' Test when a cron based schedule is provided '''
    @mock.patch('monitoring.CronTrigger')
    @mock.patch('monitoring.fnmatch.fnmatch', new=mock.MagicMock(return_value=True))
    def runTest(self, mock_triggered):
        ''' Execute test '''
        scheduler = mock.Mock(**{
            'add_job.return_value' : True
        })
        self.target.update({
            'runbooks' : {
                'test' : {
                    'nodes' : [
                        'tes*'
                    ]
                }
            }
        })
        self.assertTrue(schedule(
            scheduler,
            "test",
            self.target,
            self.config,
            self.dbc,
            self.logger))
        self.assertTrue(mock_triggered.called_with(
            second=0,
            minute='*',
            hour='*',
            day='*',
            month='*',
            day_of_week='*'))
