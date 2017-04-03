[![Build Status](https://travis-ci.org/madflojo/automatron.svg?branch=master)](https://travis-ci.org/madflojo/automatron) [![Coverage Status](https://coveralls.io/repos/github/madflojo/automatron/badge.svg?branch=master)](https://coveralls.io/github/madflojo/automatron?branch=master)

![Automatron](https://raw.githubusercontent.com/madflojo/automatron/master/docs/img/logo_huge.png)

Automatron **(Ah-Tom-a-tron)** is an open source framework designed to detect and remediate IT systems issues. Meaning, it can be used to monitor systems and when it detects issues; correct them.

## Features

* Automatically detect and add new systems to monitor
* Monitoring is executed over SSH and completely agent-less
* Policy based Runbooks allow for monitoring policies rather than server specific configurations
* Supports Nagios compliant health check scripts
* Allows arbitrary shell commands for both checks and actions
* Runbook flexibility with **Jinja2** templating support
* Pluggable Architecture that simplifies customization

## Runbooks

Automatron's actions are driven by policies called **Runbooks**. These runbooks are used to define what health checks should be executed on a target host and what to do about those health checks when they fail.

### A simple Runbook

The below example is a Runbook that will execute a monitoring plugin to determine the amount of free space on `/var/log` and based on the results execute a corrective action.

```yaml
name: Verify /var/log
schedule: "*/5 * * * *"
checks:
  mem_free:
    # Check for the % of disk free create warning with 20% free and critical for 10% free
    execute_from: target
    type: plugin
    plugin: systems/disk_free.py
    args: --warn=20 --critical=10 --filesystem=/var/log
actions:
  logrotate_nicely:
    execute_from: target
    trigger: 0
    frequency: 300
    call_on:
      - WARNING
    type: cmd
    cmd: bash /etc/cron.daily/logrotate
  logrotate_forced:
    execute_from: target
    trigger: 5
    frequency: 300
    call_on:
      - CRITICAL
    type: cmd
    cmd: bash /etc/cron.daily/logrotate --force
```

### A Runbook with Jinja2

Jinja2 support was added to Runbooks to allow for extensive customization. The below example shows using Jinja2 to determine which `cmd` to execute based on Automatron's **facts** system.

This example will detect if `nginx` is running and if not, restart it.

```yaml
name: Verify nginx is running
schedule:
  second: "*/30"
checks:
  nginx_is_running:
    # Check if nginx is running
    execute_from: target
    type: cmd
    {% if "Linux" in facts['os'] %}
    cmd: service nginx status
    {% else %}
    cmd: /usr/local/etc/rc.d/nginx status
    {% endif %}
actions:
  restart_nginx:
    execute_from: target
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
    type: cmd
    {% if "Linux" in facts['os'] %}
    cmd: service nginx restart
    {% else %}
    cmd: /usr/local/etc/rc.d/nginx restart
    {% endif %}
```

For more examples and information on getting started checkout the Automatron [wiki](https://github.com/madflojo/automatron/wiki).

## Deploying with Docker

Deploying Automatron within Docker is quick and easy. Since Automatron by default uses `redis` as a datastore we must first start a `redis` instance.

```console
$ sudo docker run -d --restart=always --name redis redis
```

Once `redis` is up and running you can start an Automatron instance.

```console
$ sudo docker run -d --link redis:redis -v /path/to/config:/config --restart=always --name automatron madflojo/automatron
```

## Stay in the loop

Follow [@Automatronio on Twitter](https://twitter.com/automatronio) for the latest Automatron news and join the community in [#Automatron on Gitter](https://gitter.im/madflojo/automatron).

## License

   Copyright 2016 Benjamin Cane

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
