'''

Runbook: Runbooks

  * Read Runbook configs
    * Validate
    * Store in-memory
  * Start Loop:
    * Lookup Existing Targets
    * Append Runbooks to target configuration
    * Notify Monitor process

'''

import fnmatch
import os
import sys
import signal
import time
import yaml
import json
import core.common
import core.logs
import core.db

def rediscover(config, dbc):
    ''' Clear out target database and rediscover new hosts '''
    targets = dbc.pop_target()
    count = 0
    if targets:
        for target in targets.keys():
            dbc.new_discovery(ip=targets[target]['ip'])
            logger.info("Added target {0} to rediscovery queue".format(targets[target]['ip']))
            count = count + 1
    return count

def process_runbooks(config, dbc):
    ''' Open, read a`nd process runbooks '''
    all_books = {}
    if os.path.isfile(config['runbook_path'] + "/init.yml"):
        with open(config['runbook_path'] + "/init.yml") as fh:
            runbooks = yaml.safe_load(fh)
        for target in runbooks:
            all_books[target] = {}
            for books in runbooks[target]:
                logger.debug("Processing book: {0}".format(books))
                book_path = "{0}/{1}".format(config['runbook_path'], books)
                if os.path.isdir(book_path):
                    book_path = book_path + "/init.yml"
                if os.path.isfile(book_path) is False:
                    logger.warn("Runbook File Error: {0} is not a file".format(book_path))
                else:
                    with open(book_path) as bh:
                        all_books[target][books] = yaml.safe_load(bh)
    return all_books

def apply_to_targets(runbooks, config, dbc):
    ''' Match hosts with runbooks '''
    targets = dbc.get_target()
    logger.debug("Found targets: {0}".format(json.dumps(targets)))
    for target in targets.keys():
        # Create runbook dictionary if it doesn't exist
        if "runbooks" not in targets[target].keys():
            logger.debug("Creating runbook dictionary in target config")
            targets[target]['runbooks'] = {}
        logger.info("Identifying runbooks for target {0}".format(target))
        for matcher in runbooks.keys():
            if fnmatch.fnmatch(targets[target]['hostname'], matcher):
                for runbook in runbooks[matcher].keys():
                    logger.debug("Checking if {0} is already applied".format(runbook))
                    if runbook not in targets[target]['runbooks'].keys():
                        targets[target]['runbooks'][runbook] = runbooks[matcher][runbook]
                        dbc.save_target(target=targets[target])
                        msg = {
                            'msg_type' : 'runbook_add',
                            'runbook' : runbook,
                            'target' : target}
                        logger.debug("Adding runbook policy {0} to target {1}".format(
                            runbook, target))
                        count = dbc.notify("monitors", msg)
                        logger.info("Notified {0} of runbook changes to target {1}".format(
                            count, target))
                    else:
                        logger.debug("{0} is already applied to target {1}".format(runbook, target))
    return True

def shutdown(signum, frame):
    ''' Shutdown this process '''
    dbc.disconnect()
    if signum == 15 or signum == 2:
        logger.info("Received signal {0} shutting down".format(signum))
        sys.exit(0)
    elif signum == 0:
        sys.exit(1)
    else:
        logger.error("Received signal {0} shutting down".format(signum))
        sys.exit(1)

if __name__ == "__main__":
    config = core.common.get_config(description="Runbook: Runbooks")
    if config is False:
        print "Could not get configuration"
        sys.exit(1)

    # Setup Logging
    logs = core.logs.Logger(config=config, proc_name="runbooks")
    logger = logs.getLogger()

    # Listen for signals
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Open Datastore Connection
    db = core.db.SetupDatastore(config=config)
    try:
        dbc = db.get_dbc()
    except Exception as e:
        logger.error("Failed to connect to datastore: {0}".format(e.message))
        shutdown(0, None)

    # Rediscover existing hosts
    logger.info("Starting target rediscovery")
    results = rediscover(config, dbc)
    logger.debug("Rediscovery complete: {0} targets rediscovered".format(results))

    # Get Runbooks from filesystem
    logger.info("Starting runbook processing")
    runbooks = process_runbooks(config, dbc)
    logger.debug("Finished processing runbooks")

    while True:
        # Get new targets and apply runbooks to them
        logger.info("Applying runbooks to targets")
        apply_to_targets(runbooks, config, dbc)
        time.sleep(20)
