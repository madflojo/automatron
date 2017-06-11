'''
Test Web API Functions
'''

import mock
import unittest

import json
import redis
import requests

class APITest(unittest.TestCase):
    ''' Run unit tests against the API Methods '''

    def setUp(self):
        ''' Setup mocked data '''
        self.dbc = redis.Redis(
            host="redis",
            port=6379,
            password=None,
            db=0)

    def tearDown(self):
        ''' Destroy mocked data '''
        self.dbc.flushdb()

class TargetswithoutTargetSpecified(APITest):
    ''' Test /api/targets when no target is specified '''
    def runTest(self):
        ''' Execute test '''
        target = {
            'facts': {},
            'runbooks' : {},
            'hostname' : 'host1.example.com',
            'ip' : '10.0.0.1'
        }
        key = "targets:details:{0}".format(target['hostname'])
        value = json.dumps(target)
        self.dbc.set(key, value)
        self.dbc.sadd('targets:ip:list', target['ip'])
        self.dbc.set('targets:ip:details:' + target['ip'], target['hostname'])

        r = requests.get(url="http://automatron:8000/api/targets")
        self.assertEqual(r.text, json.dumps({'host1.example.com' : target}))
        self.assertEqual(r.status_code, 200)

class TargetswithTargetSpecified(APITest):
    ''' Test /api/targets when a target is specified '''
    def runTest(self):
        ''' Execute test '''
        target = {
            'facts': {},
            'runbooks' : {},
            'hostname' : 'host1.example.com',
            'ip' : '10.0.0.1'
        }
        key = "targets:details:{0}".format(target['hostname'])
        value = json.dumps(target)
        self.dbc.set(key, value)
        self.dbc.sadd('targets:ip:list', target['ip'])
        self.dbc.set('targets:ip:details:' + target['ip'], target['hostname'])

        r = requests.get(url="http://automatron:8000/api/targets/host1.example.com")
        self.assertEqual(r.text, json.dumps(target))
        self.assertEqual(r.status_code, 200)

class Status(APITest):
    ''' Test /api/status '''
    def runTest(self):
        ''' Execute test '''
        target = {
            'facts': {},
            'runbooks' : {},
            'hostname' : 'host1.example.com',
            'ip' : '10.0.0.1'
        }
        key = "targets:details:{0}".format(target['hostname'])
        value = json.dumps(target)
        self.dbc.set(key, value)
        self.dbc.sadd('targets:ip:list', target['ip'])
        self.dbc.set('targets:ip:details:' + target['ip'], target['hostname'])

        r = requests.get(url="http://automatron:8000/api/status")
        self.assertEqual(r.status_code, 200)
        ret = json.loads(r.text)
        self.assertEqual(ret['targets'], 1)
