[![Build Status](https://travis-ci.org/madflojo/automatron.svg?branch=develop)](https://travis-ci.org/madflojo/automatron) [![Coverage Status](https://coveralls.io/repos/github/madflojo/automatron/badge.svg?branch=develop)](https://coveralls.io/github/madflojo/automatron?branch=develop)

# Automatron

Automatron **(Ah-Tom-a-tron)** is an open source framework designed to detect and remediate IT systems issues. Meaning, it can be used to monitor systems and when it detects issues, correct them.

This automated correction is driven by policies called **Runbooks**. These runbooks are used to define what health checks should be executed on a target host and what to do about those health checks when they fail.

### Runbook Example

```jinja
name: Verify nginx is running
schedule: "*/5 * * * *"
nodes:
  - "*web*"
checks:
  nginx_is_running:
    # Check if nginx is running
    execute_from: ontarget
    type: cmd
    {% if "Linux" in facts['os'] %}
    cmd: service nginx status
    {% else %}
    cmd: /usr/local/etc/rc.d/nginx status
    {% endif %}
actions:
  restart_nginx:
    execute_from: ontarget
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

The above runbook can be used to monitor the status of **nginx** and during failure; restart it.

## Design Principles

* Automatically detect and add new systems to monitor
* Provide Agent-less monitoring via SSH
* Use policy based Runbooks rather than host specific configurations
* Support Nagios compliant health check scripts
* Allow arbitrary commands for both checks and actions
* Provide user freedom with Jinja2 templating support for Runbooks
