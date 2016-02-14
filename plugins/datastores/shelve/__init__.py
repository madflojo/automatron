''' Datastore module for Shelve '''
from core.db import BaseDatastore
import shelve
import os


class Datastore(BaseDatastore):
    ''' Datastore class for Shelve '''


    def connect(self):
        ''' Open Shelve DB file '''
        if os.path.isfile(self.config['datastore']['plugins']['shelve']['filename']) is False:
            full_name = self.config['datastore']['plugins']['shelve']['filename'].split("/")
            path = "/".join(full_name[:-1])
            try:
                os.makedirs(path)
            except:
                raise Exception("Failed to create file path {0}".format(path))
        try:
            self.dbc = shelve.open(self.config['datastore']['plugins']['shelve']['filename'], writeback=True)
        except:
            raise Exception("Failed to open database file".format(
                self.config['datastore']['plugins']['shelve']['filename']))
        self.initialize_db()
        return True

    def disconnect(self):
        ''' Close Shelve DB file '''
        self.dbc.close()
        return True

    def initialize_db(self):
        ''' Ensure all required keys exist '''

        # Runbooks Dictionary
        if "runbooks" not in self.dbc.keys():
            self.dbc['runbooks'] = {}

        # Targets Dictionary
        if "targets" not in self.dbc.keys():
            self.dbc['targets'] = {}
        if "target_ips" not in self.dbc.keys():
            self.dbc['target_ips'] = {}

        # Possible Targets queue
        if "discovered" not in self.dbc.keys():
            self.dbc['discovered'] = []

        return True

    def new_discovery(self, ip=None):
        ''' Add new IP to target list '''
        self.dbc['discovered'].append(ip)
        self.dbc.sync()
        return True

    def discovery_queue(self):
        ''' Grab from discovery queue '''
        return self.dbc['discovered']

    def pop_discovery(self, ip=None):
        ''' Pop IP off target list '''
        if ip is None:
            return False

        try:
            self.dbc['discovered'].remove(ip)
        except Exception:
            return False

        self.dbc.sync()
        return True

    def save_target(self, target=None):
        ''' Save a target system to monitor '''
        self.dbc['targets'].update({target['hostname'] : target})
        self.dbc['target_ips'].update({target['ip'] : target['hostname']})
        self.dbc.sync()
        return True

    def get_target(self, target_id=None, ip=None):
        ''' Grab a dictionary of targets '''
        # Return all targets when given nothing
        if target_id is None and ip is None:
            return self.dbc['targets']

        # Return target by specific IP
        if ip is not None:
            if ip in self.dbc['target_ips'].keys():
                return self.dbc['targets'][self.dbc['target_ips'][ip]]
            else:
                return False

        # Return target by ID "Hostname"
        if target_id in self.dbc['targets']:
            return self.dbc['targets'][target_id]
        else:
            return False

        return False
