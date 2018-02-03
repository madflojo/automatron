'''
Automatron: Discovery

* Launch sub processes to perform discovery
* Poll process for JSON list of new targets
* Check if target already exists
  * If yes break out of loops
* Login to new targets
* Perform host level fact finding
* Add to target inventory

'''

import fabric.api
import subprocess
import sys
import os
import time
import multiprocessing
import signal
import json
import tempfile
import socket
import core.common
import core.logs
import core.fab
import core.db

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

def vet_targets(config, dbc, logger):
    ''' Get new targets and gather facts about them '''
    logger.debug("Starting Target Vetting process")
    while True:
        logger.debug("{0} Items in discovery queue".format(len(dbc.discovery_queue())))
        for host in dbc.discovery_queue():
            lookup = dbc.get_target(ip=host)
            facts_by_plugin = {}
            if lookup:
                logger.debug("Target {0} already found as {1}".format(
                    lookup['ip'], lookup['hostname']))
                dbc.pop_discovery(ip=host)
            else:
                logger.debug("Attempting to gather facts on host {0}".format(host))
                plugins = {
                    'remote' : os.listdir("{0}/vetting/remote".format(config['plugin_path'])),
                    'ontarget' : os.listdir("{0}/vetting/ontarget".format(config['plugin_path']))
                }
                for local in plugins['remote']:
                    logger.debug("Executing vetting plugin (local): {0}".format(local))
                    local_cmd = "{0}/vetting/remote/{1} {2}".format(
                        config['plugin_path'], local, host)
                    with fabric.api.hide('output', 'running', 'warnings'):
                        try:
                            results = fabric.api.local(local_cmd, capture=True)
                            if results.succeeded:
                                try:
                                    facts_by_plugin[local] = json.loads(results)
                                    logger.debug("Found facts: {0}".format(
                                        len(facts_by_plugin[local])))
                                except Exception as e:
                                    logger.debug("Could not parse output" + \
                                                 " from vetting plugin {0}".format(local))
                        except Exception as e:
                            logger.debug("Could not execute local vetting" + \
                                         " plugin {0} against host {1}: {2}".format(
                                             local_cmd, host, e.message))
                for ontarget in plugins['ontarget']:
                    logger.debug("Executing vetting plugin (ontarget): {0}".format(ontarget))
                    fabric.api.env = core.fab.set_env(config, fabric.api.env)
                    fabric.api.env.host_string = host
                    dest_name = next(tempfile._get_candidate_names())
                    destination = "{0}/{1}".format(config['discovery']['upload_path'], dest_name)
                    ontarget_plugin = "{0}/vetting/ontarget/{1}".format(
                        config['plugin_path'], ontarget)
                    with fabric.api.hide('output', 'running', 'warnings'):
                        try:
                            logger.debug("Uploading vetting plugin on target: {0}".format(
                                destination))
                            upload_results = fabric.api.put(ontarget_plugin, destination)
                            if upload_results.succeeded:
                                logger.debug("Executing {0} on target".format(destination))
                                results = fabric.api.run("chmod 700 {0} && {0}".format(destination))
                                if results.succeeded:
                                    try:
                                        facts_by_plugin[ontarget] = json.loads(results)
                                        logger.debug("Found facts: {0}".format(
                                            len(facts_by_plugin[ontarget])))
                                    except Exception as e:
                                        logger.debug("Could not parse output" + \
                                                     " from vetting plugin {0}".format(ontarget))
                        except Exception as e:
                            logger.debug("Could not login to discovered host {0} - {1}".format(
                                host, e.message))
                # Save gathered facts
                system_info = {'facts':{}}
                for item in facts_by_plugin.keys():
                    logger.debug("Appending facts: {0}".format(facts_by_plugin[item]))
                    system_info['facts'].update(facts_by_plugin[item])
                system_info['ip'] = host
                if "hostname" not in system_info:
                    try:
                        system_info["hostname"] = socket.gethostbyaddr(host)[0]
                    except Exception as e:
                        logger.debug("Exception while looking up target hostname: {0}".format(
                            e.message))
                        system_info["hostname"] = host
                if dbc.save_target(target=system_info):
                    dbc.pop_discovery(ip=host)
        if "unit-testing" in config.keys():
            break
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
        logger.error("Received signal {0} shutting down".format(signum))
        sys.exit(1)

if __name__ == "__main__":
    # pylint: disable=C0103
    config = core.common.get_config(description="Automatron: Discovery")
    if config is False:
        print("Could not get configuration")
        sys.exit(1)

    # Setup Logging
    logs = core.logs.Logger(config=config, proc_name="discovery")
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

    threads = []
    # Start plugin threads
    for plugin_name in config['discovery']['plugins'].keys():
        t = multiprocessing.Process(
            target=run_plugin, args=(plugin_name, config, dbc), name=plugin_name)
        threads.append(t)
        t.start()

    # Start vetting thread
    t = multiprocessing.Process(target=vet_targets, args=(config, dbc, logger), name="Target Vetting")
    threads.append(t)
    t.start()

    while True:
        for thread in threads:
            if thread.is_alive() is False:
                logger.debug("Thread for {0} has exited {1}, shutting down".format(t.name, t.exitcode))
                core.common.kill_threads(threads)
                shutdown(0, None)
        time.sleep(.5)
