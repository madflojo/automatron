Automated host discovery is one of the key functions of Automatron. Like the majority of Automatron this functionality can be extended through a serious of plugins. However, unlike the **checks** or **actions** plugins the **discovery** plugins are a bit more complex.

To get started it is highly recommended to reference an existing plugin such as the [AWS Discovery](https://github.com/Automatron-Plugins/aws-autodiscovery/blob/master/aws/__init__.py) plugin.

To help understand the Discovery plugins, let's take a look at a simple example. The below is a copy of the **roster** discovery plugin.

```python
''' Roster file discovery plugin '''

import time
import json
import requests
from core.discover import BaseDiscover
import core.logs

class Discover(BaseDiscover):
    ''' Main Discover Class '''

    def start(self):
        ''' Start Discovery '''
        logs = core.logs.Logger(config=self.config, proc_name="discovery.roster")
        logger = logs.getLogger()
        logger = logs.clean_handlers(logger)
        logger.debug("Getting hosts from Roster")

        while True:
            found = []
            try:
                for ip in self.config['discovery']['plugins']['roster']['hosts']:
                    found.append(ip)
                    if self.dbc.new_discovery(ip=ip):
                        logger.debug("Added host {0} to discovery queue".format(ip))
                    else:
                        logger.debug("Failed to add host {0} to discovery queue".format(ip))
            except KeyError as e:
                logger.warn("Configuration syntax error: {0}".format(e.message))

            logger.info("Found {0} hosts".format(len(found)))
            if "unit_testing" in self.config.keys():
                # Break out of loop for unit testing
                break
            else:
                # Adding sleep() so master process doesn't exit after completion
                time.sleep(900)
        # Return true for unit testing
        return True
```

The above plugin is written in Python and has some basic requirements.

The first requirement is that the `class` name is always `Discover`. This is the class that will be dynamically loaded by Automatron, if this name is incorrect the plugin will not work.

The second requirement is that the plugin must add newly discovered target hosts via the `self.dbc.new_discovery()` function shown above. This function will add the target host to Automatron's internal queue for newly discovered hosts.
