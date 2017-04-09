![Automatron](https://raw.githubusercontent.com/madflojo/automatron/master/docs/img/logo_huge.png)

Automatron is a framework for creating self-healing infrastructure. Simply put, it detects system events & takes action to correct them.

The goal of Automatron is to allow users to automate the execution of common tasks performed during system events. These tasks can be as simple as **sending an email** to as complicated as **restarting services across multiple hosts**.

## Features

  * Automatically detect and add new systems to monitor
  * Monitoring is executed over SSH and completely **agent-less**
  * Policy based [Runbooks](runbooks/index.md) allow for monitoring policies rather than server specific configurations
  * Supports Nagios compliant health check scripts
  * Allows dead simple **arbitrary shell commands** for both [checks](runbooks/checks.md) and [actions](runbooks/actions.md)
  * Runbook flexibility with **Jinja2** templating support
  * Pluggable Architecture that simplifies customization

## Runbooks

The core of Automatron is based around **Runbooks**. Runbooks are policies that define health checks and actions. You can think of them in the same way you would think of a printed runbook. Except with Automatron, the actions are automated.

### A simple Runbook example

The below runbook is a very basic example, it will check if NGINX is running (every 2 minutes) and restart it after 2 unsuccessful checks.

```yaml+jinja
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

The above actions will be performed every 300 seconds (5 minutes) until the health check returns an OK status. This delay allows time for NGINX to restart after each execution.

### A complex Runbook with Jinja2

This next runbook example is a more complex version of the above. In this example we will use Jinja2 and Automatron's Facts to enhance our runbook further.

```yaml+jinja
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

Another addition is the `remove_from_dns` action, which will remove the target server's DNS entry using the **CloudFlare DNS** plugin.

By using **Facts** and **Jinja2** together you can customize a single runbook to cover unique actions for multiple hosts and environments.

## Follow Automatron

[![Twitter Follow](https://img.shields.io/twitter/follow/automatronio.svg?style=flat-square)](https://twitter.com/automatronio) [![Gitter](https://badges.gitter.im/madflojo/automatron.svg)](https://gitter.im/madflojo/automatron?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) [![GitHub forks](https://img.shields.io/github/forks/madflojo/automatron.svg?style=social&label=Fork)](https://github.com/madflojo/automatron) [![GitHub stars](https://img.shields.io/github/stars/madflojo/automatron.svg?style=social&label=Star)](https://github.com/madflojo/automatron)
