'''
Runbook: Discovery

* Launch sub processes to perform discovery
* Poll process for JSON list of new targets
* Check if target already exists
  * If yes break out of loops
* Login to new targets
* Perform host level fact finding
* Add to target inventory

'''

import core.common
import core.logs
import core.fab
import fabric.api
import sys
import time
import multiprocessing
import signal
import json

def run_plugin(plugin_name, config, dbc):
    ''' Kick off a thread to perform plugin actions '''
    finder = __import__("plugins.discovery." + plugin_name, globals(), locals(), ['Discover'], -1)
    find = finder.Discover(config=config, dbc=dbc)
    try:
        logger.info("Launching discovery plugin: {0}".format(plugin_name))
        find.start()
    except Exception as e:
        logger.error("Got an exception from discovery plugin: {0} - {1}".format(
            plugin_name, e.message))
    return False

def vet_targets(config, dbc):
    ''' Get new targets and gather facts about them '''
    while True:
        logger.debug(dbc.discovery_queue())
        for host in dbc.discovery_queue():
            lookup = dbc.get_target(ip=host)
            if lookup is not False:
                logger.debug("Target {0} already found as {1}".format(lookup['ip'], lookup['hostname']))
                dbc.pop_discovery(ip=host)
            else:
                logger.debug("Attempting to gather facts on host {0}".format(host))
                fabric.api.env = core.fab.set_env(config, fabric.api.env)
                fabric.api.env.host_string = host
                finder_upload = "{0}/fact_finder.py".format(config['discovery']['upload_path'])
                with fabric.api.hide('output', 'running', 'warnings'):
                    try:
                        fabric.api.put('fact_finder.py', finder_upload)
                        results = fabric.api.run("python " + finder_upload)
                    except Exception as e:
                        logger.debug("Could not login to discovered host {0} - {1}".format(
                            host, e.message))
                if results.succeeded:
                    try:
                        system_info = json.loads(results)
                    except Exception as e:
                        logger.debug("Could not parse fact finder output: {0}".format(e.message))
                    system_info['ip'] = host
                    if dbc.save_target(target=system_info):
                        dbc.pop_discovery(ip=host)
        time.sleep(config['discovery']['vetting_interval'])


def shutdown(signum, frame):
    ''' Shutdown this process '''
    dbc.disconnect()
    if signum == 15 or signum == 2:
        logger.info("Received signal {0} shutting down".format(signum))
        sys.exit(0)
    elif signum == 0:
        sys.exit(1)
    else:
        logger.info("Received signal {0} shutting down".format(signum))
        sys.exit(1)

if __name__ == "__main__":
    config = core.common.get_config(description="Runbook: Discovery")
    if config is False:
        print "Could not get configuration"
        sys.exit(1)

    # Setup Logging
    logs = core.logs.Logger(config=config, proc_name="discovery")
    logger = logs.getLogger()

    # Listen for signals
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    # Open Datastore Connection
    logger.info("Importing datastore {0}".format(config['datastore']['engine']))
    db = __import__("plugins.datastores." + config['datastore']['engine'], globals(), locals(),
                    ['Datastore'], -1)
    dbc = db.Datastore(config=config)
    if dbc.connect() is False:
        logger.error("Failed to connect to datastore")
        shutdown(0, None)

    threads = []
    # Start plugin threads
    for plugin_name in config['discovery']['plugins'].keys():
        t = multiprocessing.Process(target=run_plugin, args=(plugin_name, config, dbc), name=plugin_name)
        threads.append(t)
        t.start()

    # Start vetting thread
    t = multiprocessing.Process(target=vet_targets, args=(config, dbc), name="Target Vetting")
    threads.append(t)
    t.start()

    while True:
      for thread in threads:
          if thread.is_alive() is False:
              logger.debug("Thread for {0} has exited, shutting down".format(t.name))
              core.common.kill_threads(threads)
              shutdown(0, None)
      time.sleep(.5)
