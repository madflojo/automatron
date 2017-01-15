'''

Automatron: Monitoring

  * Get all Targets and Runbooks
    * Schedule Checks
    * Execute Checks per schedule
    * Notify Check status
  * Listen for Runbook and Target changes
    * Reschedule Checks

'''

import fnmatch
import os
import sys
import signal
import json
import tempfile
import fabric.api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import core.common
import core.logs
import core.db
import core.fab

def monitor(runbook, target, config, dbc, logger):
    ''' Execute monitor against target '''
    # Clear out APSchedulers default loggin
    import logging
    logging.getLogger('apscheduler.scheduler').setLevel('WARNING')
    logging.getLogger('apscheduler.scheduler').propagate = False

    runbook_status = {
        'msg_type' : 'runbook_status',
        'runbook' : runbook,
        'target' : target['hostname'],
        'checks' : {}
    }

    logger.debug("Executing runbook {0} against target {1}".format(runbook, target['hostname']))

    fabric.api.env = core.fab.set_env(config, fabric.api.env)
    fabric.api.env.host_string = target['ip']

    for check_name in target['runbooks'][runbook]['checks'].keys():
        check = target['runbooks'][runbook]['checks'][check_name]
        if "plugin" in check['type']:
            plugin_file = check['plugin']
            plugin_file = '{0}/checks/{1}'.format(config['plugin_path'], plugin_file)
            dest_name = next(tempfile._get_candidate_names())
            destination = "{0}/{1}".format(config['monitoring']['upload_path'], dest_name)
            with fabric.api.hide('output', 'running', 'warnings'):
                try:
                    if check["execute_from"] == "ontarget":
                        logger.debug("Placing plugin script into {0}".format(destination))
                        fabric.api.put(plugin_file, destination)
                        fabric.api.run("chmod 700 {0}".format(destination))
                        cmd = "{0} {1}".format(destination, check['args'])
                        results = fabric.api.run(cmd)
                        fabric.api.run("rm {0}".format(destination))
                    elif check["execute_from"] == "remote":
                        cmd = "{0} {1}".format(plugin_file, check['args'])
                        results = fabric.api.local(cmd, capture=True)
                    else:
                        logger.warn('Unknown "execute_from" specified in check')
                        return False
                except Exception as e:
                    logger.debug("Could not put plugin file {0} on remote host {1}".format(
                        plugin_file, target['ip']))
        else:
            cmd = check['cmd']
            # Perform Check
            with fabric.api.hide('output', 'running', 'warnings'):
                try:
                    if check["execute_from"] == "ontarget":
                        results = fabric.api.run(cmd)
                    elif check["execute_from"] == "remote":
                        results = fabric.api.local(cmd, capture=True)
                    else:
                        logger.warn('Unknown "execute_from" specified in check')
                        return False
                except Exception as e:
                    logger.debug("Could not execute command {0}".format(cmd))
        if results.return_code == 0:
            check_return = "OK"
        elif results.return_code == 1:
            check_return = "WARNING"
        elif results.return_code == 2:
            check_return = "CRITICAL"
        else:
            check_return = "UNKNOWN"

        runbook_status['checks'][check_name] = check_return
        logger.info("Check {0} for target {1} returned {2}".format(
            check_name, target['hostname'], check_return))

    dbc.notify("check:results", runbook_status)

def schedule(scheduler, runbook, target, config, dbc, logger):
    ''' Setup schedule for new runbooks and targets '''
    task_schedule = target['runbooks'][runbook]['schedule'].split(" ")
    cron = CronTrigger(
        minute=task_schedule[0],
        hour=task_schedule[1],
        day=task_schedule[2],
        month=task_schedule[3],
        day_of_week=task_schedule[4],
    )
    should_schedule = False
    for node in target['runbooks'][runbook]['nodes']:
        if fnmatch.fnmatch(os.uname()[1], node):
            should_schedule = True

    if should_schedule:
        return scheduler.add_job(
            monitor,
            trigger=cron,
            args=[runbook, target, config, dbc, logger]
        )
    else:
        return False

def listen(scheduler, config, dbc, logger):
    ''' Listen for new events and schedule runbooks '''
    logger.info("Starting subscription to monitors channel")
    pubsub = dbc.subscribe("monitors")
    for msg in pubsub.listen():
        logger.debug("Got message: {0}".format(msg))
        try:
            item = dbc.process_subscription(msg)
            logger.debug("Received {0} notification for {1}".format(
                item['msg_type'], item['target']))
            target = dbc.get_target(target_id=item['target'])
            logger.debug("Found target: {0}".format(json.dumps(target)))
            job = schedule(scheduler, item['runbook'], target, config, dbc, logger)
            if job:
                name = "{0}:{1}".format(
                    target['runbooks'][item['runbook']]['name'],
                    target['hostname'])
                jobs.update({name : job})
            logger.info("Scheduled runbook {0} for target {1}".format(
                item['runbook'], item['target']))
        except Exception as e:
            logger.warn("Unable to process message: {0}".format(e.message))

def initialize(config, dbc, scheduler, logger):
    ''' Grab existing targets and setup monitors '''
    targets = dbc.get_target()
    scheduled = 0
    jobs = {}
    for target in targets.keys():
        for runbook in targets[target]['runbooks'].keys():
            job = schedule(scheduler, runbook, targets[target], config, dbc, logger)
            if job:
                name = "{0}:{1}".format(
                    targets[target]['runbooks'][runbook]['name'],
                    target)
                logger.debug("Scheduled runbook {0} for target {1}".format(runbook, target))
                jobs.update({name : job})
                scheduled = scheduled + 1
    return jobs, scheduled


def shutdown(signum, frame):
    ''' Shutdown this process '''
    dbc.disconnect()
    # Remove jobs
    for job in jobs:
        jobs[job].remove()
    if signum == 15 or signum == 2:
        logger.info("Received signal {0} shutting down".format(signum))
        sys.exit(0)
    elif signum == 0:
        sys.exit(1)
    else:
        logger.error("Received signal {0} shutting down".format(signum))
        sys.exit(1)

if __name__ == "__main__":
    config = core.common.get_config(description="Automatron: Monitoring")
    if config is False:
        print "Could not get configuration"
        sys.exit(1)

    # Setup Logging
    logs = core.logs.Logger(config=config, proc_name="monitoring")
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

    # Start Scheduler
    scheduler = BackgroundScheduler()
    scheduler.start()

    logger.info("Grabbing targets for initial scheduling")
    jobs, scheduled = initialize(config, dbc, scheduler, logger)
    logger.info("Scheduled {0} checks".format(scheduled))

    while True:
        listen(scheduler, config, dbc, logger)
