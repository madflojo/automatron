''' Base datastore class for Runbook '''

class BaseDatastore(object):
    ''' Base class for Runbook datastore plugins to import '''

    def __init__(self, config=None):
        ''' Initialize the database class '''
        self.config = config
        self.dbc = None

    def connect(self):
        ''' Connect to database '''
        pass

    def disconnect(self):
        ''' Disconnect from DB '''
        pass

    def initialize_db(self):
        ''' Initialize the datastore ''' 

    # Events
    def publish_event(self, event=None):
        ''' Publish an event to the event stream '''
        pass

    def subscribe_events(self, event_queue=None):
        ''' Subscribe to an event queue '''
        pass

    # Targets
    def new_target(self, ip=None):
        ''' Add new target ip to queue '''
        pass

    def save_target(self, target=None):
        ''' Save a new target '''
        pass

    def get_target(self, target_id=None, ip=None):
        ''' Pull Details of Targets '''
        pass

    # Runbooks
    def get_runbook(self, id=None):
        ''' Pull all Runbooks from datastore '''
        pass

    def store_runbook(self, runbook=None):
        ''' Store dictionary object into datastore '''
        pass


class SetupDatastore(object):
    ''' Helper class to setup datastore '''

    def __init__(self, config=None):
        ''' Initializing the helper class'''
        self.config = config
        self.dbc = None

    def get_dbc(self):
        ''' Get the dbc object '''
        db = __import__("plugins.datastores." + self.config['datastore']['engine'], globals(), locals(),
                        ['Datastore'], -1)
        dbc = db.Datastore(config=self.config)
        if dbc:
            dbc.connect()
            return dbc
        else:
            raise Exception("Could not load DB module")
