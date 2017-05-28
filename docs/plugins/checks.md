While Automatron tries to make runbooks as simple as executing shell commands there is sometimes a need to take things a bit further than a simple one-liner.

To facilitate this Automatron also enables users to create custom health check plugins. These plugins are Nagios compatible executables that can be written a programming language of your choice.

## A simple example

In this walkthrough we will go ahead and create a custom health check plugin that pings a remote host to determine its availability. To get started, let's take a look at a runbook example of this.

```yaml+jinja
name: Ping Check
schedule: "*/2 * * * *"
checks:
  host_is_pingable:
    execute_from: target
    type: plugin
    plugin: ping/check.sh
    args: 10.0.0.1
```

This runbook uses the plugin system to copy the `ping/check.sh` script to the target host and executes it with the arguments of `10.0.0.1`. This is equivalent to the following command.

```sh
$ ping/check.sh 10.0.0.1
```

With the runbook understood, let's now start writing our plugin.

### Plugin code

This type of health check plugin is very simple to write. The following **BASH** script is a working example that could easily be used with Automatron.

```bash
#!/bin/bash
if [ -z $1 ]
then
    exit 1
fi

/bin/ping -c 1 $1 > /dev/null 2>&1
if [ $? -eq 0 ]
then
    echo "PING OK UP"
    exit 0
else
    echo "PING CRITICAL DOWN"
    exit 2
fi
```

This script follows the [Nagios Plugin API](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/pluginapi.html) specifications however the most important aspect of this health check is the exit code used. Automatron follows the same exit code mapping used by Nagios, as such the below list shows the mapping of exit code to health check status.

* `OK`: Requires a successful exit code of `0`
* `WARNING`: Is indicated by an exit code of `1`
* `CRITICAL`: Is indicated by an exit code of `2`
* `UNKNOWN`: Is indicated by any other exit code

!!! tip
    Since Automatron supports Nagios compliant scripts you can simply use existing [Nagios Plugins](https://exchange.nagios.org/directory/Plugins) and other plugins from any monitoring solution that follows the Nagios plugin model.

    Some additional sources are: [Icinga Exchange](https://exchange.icinga.com/dig/Plugins), [Sensu Plugins](https://github.com/sensu-plugins), and [Monitoring Plugins Project](https://www.monitoring-plugins.org/).

!!! info
    At this time Automatron ships with limited plugins available, in addition to the resources above additional Automatron plugins can be found at the [Automatron Plugins](https://github.com/Automatron-Plugins) project.
