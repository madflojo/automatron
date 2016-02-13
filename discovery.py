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
import sys
import time
import threading

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
    


if __name__ == "__main__":
    config = core.common.get_config(description="Runbook: Discovery")
    if config is False:
        print "Could not get configuration"
        sys.exit(1)

    # Setup Logging
    logs = core.logs.Logger(config=config, proc_name="discovery")
    logger = logs.getLogger()

    # Open Datastore Connection
    logger.info("Importing datastore {0}".format(config['datastore']['engine']))
    db = __import__("plugins.datastores." + config['datastore']['engine'], globals(), locals(),
                    ['Datastore'], -1)
    dbc = db.Datastore(config=config)
    if dbc.connect() is False:
        logger.error("Failed to connect to datastore")
        sys.exit(1)

    threads = []
    for plugin_name in config['discovery']['plugins'].keys():
        t = threading.Thread(target=run_plugin, args=(plugin_name, config, dbc), name=plugin_name)
        threads.append(t)
        t.start()

    while True:
      for thread in threads:
          if thread.isAlive() is False:
              logger.debug("Thread for {0} has exited".format(t.name))
              sys.exit(1)
      time.sleep(.5)
