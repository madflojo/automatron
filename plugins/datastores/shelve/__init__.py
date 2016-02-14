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
            self.dbc = shelve.open(self.config['datastore']['plugins']['shelve']['filename'])
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

        # Possible Targets queue
        if "possible_targets" not in self.dbc.keys():
            self.dbc['possible_targets'] = []

        return True

    def new_target(self, ip=None):
        ''' Add new IP to target list '''
        self.dbc['possible_targets'].append(ip)
        return True

    def save_target(self, target=None):
        ''' Save a target system to monitor '''
        self.dbc['targets'].update({target['name'] : target})
        return True

    def get_target(self, id=None):
        ''' Grab a dictionary of targets '''
        if id is None or id not in self.dbc['targets']:
            return self.dbc['targets']
        else:
            return self.dbc['targets'][id]
