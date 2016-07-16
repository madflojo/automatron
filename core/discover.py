''' Base Discovery Class '''

class BaseDiscover(object):
    ''' Base Class '''

    def __init__(self, config=None, dbc=None):
        ''' Initialize the database class '''
        self.config = config
        self.dbc = dbc

    def start(self):
        ''' Start Discovery process '''
        return True
