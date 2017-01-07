''' webping discovery plugin '''

from core.discover import BaseDiscover
import core.logs
import time

from gevent.pywsgi import WSGIServer

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def grab_ip(self, env, start_response):
        ''' Grab IP from Webserver event '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.webping")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        up = []
        ip = env['REMOTE_ADDR']
        if ip not in up:
            up.append(ip)
            logger.debug("Found new host: {0}".format(ip))
            if self.dbc.new_discovery(ip=ip):
                logger.debug("Added host {0} to discovery queue".format(ip))
            else:
                logger.debug("Failed to add host {0} to discovery queue".format(ip))
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Success']


    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.webping")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.info("Listening for web pings")
        WSGIServer((self.config['discovery']['plugins']['webping']['ip'],
                    self.config['discovery']['plugins']['webping']['port']),
                    application=self.grab_ip, log=None).serve_forever()
