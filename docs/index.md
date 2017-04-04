![Automatron](https://raw.githubusercontent.com/madflojo/automatron/master/docs/img/logo_huge.png)

Automatron is a framework for creating self-healing infrastructure. Simply put, it detects system events & takes action to correct them.

The goal of Automatron is to allow users to automate the execution of common tasks performed during system events. These tasks can be as simple as **send an email** to as complicated as **restarting services across multiple hosts**.

## Features

* Automatically detect and add new systems to monitor
* Monitoring is executed over SSH and completely **agent-less**
* Policy based Runbooks allow for monitoring policies rather than server specific configurations
* Supports Nagios compliant health check scripts
* Allows dead simple **arbitrary shell commands** for both checks and actions
* Runbook flexibility with **Jinja2** templating support
* Pluggable Architecture that simplifies customization

## Runbooks

The core of Automatron is based around **Runbooks**. Runbooks are policies that define health checks and actions. You can think of them in the same way you would think of a printed runbook. Except with Automatron, the actions are automated.

### A simple Runbook example

The below Runbook is a very basic example, it will check if NGINX is running (every 2 minutes) and restart it after 2 unsuccessful checks.

```yaml
name: Check NGINX
schedule: "*/2 * * * *"
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
actions:
  restart_nginx:
    execute_from: target
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: cmd
    cmd: service nginx restart
```

The above actions be performed every 300 seconds (5 minutes) until the health check returns an OK status. This delay allows time for NGINX to restart after each execution.

### A complex Runbook with Jinja2

This next Runbook example is a more complex version of the above. In this example we will use Jinja2 and Automatron's Facts to enhance our runbook further.

```yaml
name: Check NGINX
{% if "prod" in facts['hostname'] %}
schedule:
  second: */20
{% else %}
schedule: "*/2 * * * *"
{% endif %}
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
actions:
  restart_nginx:
    execute_from: target
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: cmd
    cmd: service nginx restart
  remove_from_dns:
    execute_from: remote
    trigger: 0
    frequency: 0
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: plugin
    plugin: cloudflare/dns.py
    args: remove test@example.com apikey123 example.com --content {{ facts['network']['eth0']['v4'][0] }}
```

The above example uses **Jinja2** and **Facts** to create a conditional schedule. If our target server has a hostname that contains the word "prod" within it. The schedule for the health check will be every 20 seconds. If not, it will be every 2 minutes.

Another addition is the `remove_from_dns` action, which will remove the target servers DNS entry using the **CloudFlare DNS** plugin.

By using **Facts** and **Jinja2** together you can customize a single runbook to cover unique actions for multiple hosts and environments.

## Deploying with Docker

Deploying Automatron within Docker is quick and easy. Since Automatron by default uses `redis` as a datastore we must first start a `redis` instance.

```console
$ sudo docker run -d --restart=always --name redis redis
```

Once `redis` is up and running you can start an Automatron instance.

```console
$ sudo docker run -d --link redis:redis -v /path/to/config:/config --restart=always --name automatron madflojo/automatron
```

The above uses Docker's volume mounts to present a config directory from the host to the container. You will need to configure Automatron before it is able to detect any new hosts. Instructions can be found by following the [Automatron in 10 Minutes](http://automatron.io/en/latest/automatron-in-10-minutes/) guide.

## Next Steps

* [![Twitter Follow](https://img.shields.io/twitter/follow/automatronio.svg?style=flat-square)](https://twitter.com/automatronio) for the latest Automatron news and join the community [![Gitter](https://badges.gitter.im/madflojo/automatron.svg)](https://gitter.im/madflojo/automatron?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).
* [![GitHub forks](https://img.shields.io/github/forks/madflojo/automatron.svg?style=social&label=Fork)](https://github.com/madflojo/automatron) and/or [![GitHub stars](https://img.shields.io/github/stars/madflojo/automatron.svg?style=social&label=Star)](https://github.com/madflojo/automatron) Automatron
* Follow our quick start guide: [Automatron in 10 minutes](automatron-in-10-minutes)
* Check out [example Runbooks](https://github.com/madflojo/automatron/tree/master/config/runbooks/examples) for automating common tasks
* Read our [Runbook Reference](Runbooks) documentation to better understand the anatomy of a Runbook
* Deploy a [Docker container](https://hub.docker.com/r/madflojo/automatron/) instance of Automatron
