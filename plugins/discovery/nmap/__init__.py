''' nmap discovery plugin '''

import time
from core.discover import BaseDiscover
import core.logs

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.nmap")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.info("Starting scan of environment")
        try:
            nmap = NmapProcess(self.config['discovery']['plugins']['nmap']['target'],
                               options=self.config['discovery']['plugins']['nmap']['flags'])
        except Exception as e:
            raise Exception("Failed to execute nmap process: {0}".format(e.message))
        up = []
        while True:
            nmap.run()
            nmap_report = NmapParser.parse(nmap.stdout)
            for scanned_host in nmap_report.hosts:
                if "up" in scanned_host.status and scanned_host.address not in up:
                    up.append(scanned_host.address)
                    logger.debug("Found new host: {0}".format(scanned_host.address))
                    if self.dbc.new_discovery(ip=scanned_host.address):
                        logger.debug("Added host {0} to discovery queue".format(
                            scanned_host.address))
                    else:
                        logger.debug("Failed to add host {0} to discovery queue".format(
                            scanned_host.address))
            logger.debug("Scanned {0} hosts, {1} found up".format(
                len(nmap_report.hosts), len(up)))
            time.sleep(self.config['discovery']['plugins']['nmap']['interval'])
        return True
