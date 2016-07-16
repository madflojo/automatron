''' Datastore module for Redis '''
from core.db import BaseDatastore
import redis
import json


class Datastore(BaseDatastore):
    ''' Datastore class for Redis'''

    def connect(self):
        ''' Open Connection to Redis '''
        if "password" not in self.config['datastore']['plugins']['redis'].keys():
            password = None
        else:
            password = self.config['datastore']['plugins']['redis']['password']
        try:
            self.dbc = redis.Redis(
                host=self.config['datastore']['plugins']['redis']['host'],
                port=self.config['datastore']['plugins']['redis']['port'],
                password=None,
                db=self.config['datastore']['plugins']['redis']['db'])
        except Exception as e:
            raise Exception("Failed to connect to Redis: {0}".format(e.message))
        self.initialize_db()
        return True

    def new_discovery(self, ip=None):
        ''' Add new IP to target list '''
        return self.dbc.sadd("discovered", ip)

    def discovery_queue(self):
        ''' Grab from discovery queue '''
        return self.dbc.smembers("discovered")

    def pop_discovery(self, ip=None):
        ''' Pop IP off target list '''
        if ip is None:
            return False
        self.dbc.srem("discovered", ip)
        return True


    def save_target(self, target=None):
        ''' Save a target system to monitor '''
        key = "targets:details:{0}".format(target['hostname'])
        value = json.dumps(target)
        self.dbc.set(key, value)
        self.dbc.sadd('targets:ip:list', target['ip'])
        self.dbc.set('targets:ip:details:' + target['ip'], target['hostname']) 
        return True

    def get_target(self, target_id=None, ip=None):
        ''' Grab a dictionary of targets '''
        # Return all targets when given nothing
        if target_id is None and ip is None:
            targets = {}
            for ipaddr in self.dbc.smembers('targets:ip:list'):
                result = self.get_target(ip=ipaddr)
                if result:
                    targets[result['hostname']] = result
            return targets

        # Return target by specific IP
        if ip is not None:
            if ip in self.dbc.smembers('targets:ip:list'):
                key = self.dbc.get('targets:ip:details:' + ip)
                return self.get_target(target_id=key)
            else:
                return False

        # Return target by ID "Hostname"
        if target_id:
            result = self.dbc.get('targets:details:' + target_id)
            if result:
                return json.loads(result)
            else:
                return result
        else:
            return False

        return False

    def pop_target(self, target_id=None):
        ''' Grab a dictionary of targets, then clear it '''
        targets = self.get_target(target_id=target_id)
        if target_id:
            self.dbc.delete('targets:details:' + target_id)
            self.dbc.delete('targets:ip:details:' + targets['ip'])
            self.dbc.srem('targets:ip:list', targets['ip'])
        return targets

    def notify(self, channel, details):
        ''' Notify subscribers of a channel the defined details '''
        return self.dbc.publish(channel, json.dumps(details))

    def subscribe(self, channel):
        ''' Subscribe to a channel '''
        pubsub = self.dbc.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def process_subscription(self, msg):
        ''' Turn subscription message into dictionary '''
        return json.loads(msg['data'])
