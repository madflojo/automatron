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

    # Events
    def publish_event(self, event=None):
        ''' Publish an event to the event stream '''
        pass

    def subscribe_events(self, event_queue=None):
        ''' Subscribe to an event queue '''
        pass

    # Runbooks
    def get_runbook(self, id=None):
        ''' Pull all Runbooks from datastore '''
        pass

    def store_runbook(self, runbook=None):
        ''' Store dictionary object into datastore '''
        pass
