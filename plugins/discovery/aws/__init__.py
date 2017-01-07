''' AWS discovery plugin '''

import time
import json
import requests
from core.discover import BaseDiscover
import core.logs
import boto3

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.aws")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.info("Getting hosts from AWS")


        while True:
            # Setup IP List
            ip_addrs = []

            try:
                # Connect to AWS
                session = boto3.session.Session(
                    aws_access_key_id=self.config['discovery']['plugins']['aws']['aws_access_key_id'],
                    aws_secret_access_key=self.config['discovery']['plugins']['aws']['aws_secret_access_key'])
                # Get Regions then connect to each and list instances
                for region in session.get_available_regions('ec2'):
                    ec2 = session.client("ec2", region)
                    data = ec2.describe_instances()
                    for reservation in data['Reservations']:
                        for instance in reservation['Instances']:
                            # Check if filter should be public or private IP's
                            if 'filter' in self.config['discovery']['plugins']['aws']:
                                ip_types = self.config['discovery']['plugins']['aws']['filter']
                            else: # Default to both
                                ip_types = [ 'PrivateIPAddress', 'PublicIPAddress' ]
                            # Get IP's and Append to list
                            for ip_type in ip_types:
                                ip_addrs.append(instance[ip_type])
            except Exception as e:
                logger.debug("Failed to query AWS: {0}".format(e.message))

            # Process found IP's
            for ip in ip_addrs:
                if self.dbc.new_discovery(ip=ip):
                    logger.debug("Added host {0} to discovery queue".format(ip))
                else:
                    logger.debug("Failed to add host {0} to discovery queue".format(ip))

            logger.debug("Found {0} hosts".format(len(ip_addrs)))
            if "unit_testing" in self.config.keys():
                # Break out of loop for unit testing
                break
            else:
                time.sleep(self.config['discovery']['plugins']['aws']['interval'])
        # Return true for unit testing
        return True
