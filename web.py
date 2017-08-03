'''

Automatron: API Service
    * Act as backend to user interface
    * Provide REST API for Automatron

'''

import json
import sys
from flask import Flask, g, request, render_template
import core.common
import core.logs
import core.db

app = Flask(__name__)

def connect_db(config):
    ''' Connect to DB '''
    db = core.db.SetupDatastore(config=config)
    try:
        return db.get_dbc()
    except Exception as e:
        logger.error("Failed to connect to datastore: {0}".format(e.message))
        return None

@app.before_request
def before_request():
    ''' Pre-request hander '''
    logger.debug("Incoming Web Request: {0}".format(request.full_path))
    g.dbc = connect_db(app.config)

@app.teardown_request
def teardown_request(exc=None):
    ''' Post request handler '''
    if hasattr(g, 'dbc'):
        g.dbc.disconnect()

# Web UI Routes
@app.route('/', methods=['GET'])
def get_index():
    ''' Returns dashboard '''
    data = {
        'theme': 'slate'
    }
    # Set Bootswatch theme
    if 'theme' in app.config['web']:
        data['theme'] = app.config['web']['theme']
    return render_template("index.html", data=data), 200

# API Routes
@app.route('/api/status', methods=['GET'])
def get_status():
    ''' Returns JSON string summarizing current Automatron status '''
    status = {
        'targets': 0,
        'runbooks': {
            'OK': 0,
            'CRITICAL': 0,
            'WARNING': 0,
            'UNKNOWN': 0
        },
        'events': []
    }
    targets = g.dbc.get_target()
    for target in targets.keys():
        status['targets'] = status['targets'] + 1
        if 'runbooks' in targets[target]:
            for runbook in targets[target]['runbooks'].keys():
                if 'status' in targets[target]['runbooks'][runbook]:
                    for s in targets[target]['runbooks'][runbook]['status'].keys():
                        if targets[target]['runbooks'][runbook]['status'][s] > 0:
                            status['runbooks'][s] = status['runbooks'][s] + 1
                            status['events'].append({
                                'status': s,
                                'target': target,
                                'runbook': targets[target]['runbooks'][runbook]['name'],
                                'count': targets[target]['runbooks'][runbook]['status'][s]
                            })
    return json.dumps(status), 200

@app.route('/api/targets/<target>', methods=['GET'])
@app.route('/api/targets', methods=['GET'])
def get_targets(target=None):
    ''' Returns JSON string of target information from the database '''
    targets = g.dbc.get_target(target_id=target)
    return json.dumps(targets), 200

if __name__ == '__main__':
    config = core.common.get_config(description="Automatron: Web")
    if config is False:
        print "Could not get configuration"
        sys.exit(1)
    app.config.update(config)

    # Setup Logging
    if app.config['logging']['debug']:
        app.debug = True
    logs = core.logs.Logger(config=config, proc_name="api")
    logger = logs.getLogger()

    # Start Flask
    app.run(host=app.config['web']['listen'], port=app.config['web']['port'])
