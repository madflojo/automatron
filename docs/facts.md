Automatron provides the ability to use the Jinja templating language with [Runbooks](runbooks). To support this ability to use templates Automatron also has a **facts** facility. Facts are simply information that has been gathered from the target system. This includes information such as Hostname, OS, Services Running and Network information.

The below is an example runbook that utilizes the Automatron facts system.

```yaml+jinja
name: Verify nginx is running
schedule: "*/5 * * * *"
nodes:
  - "*web*"
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

In the example above the `facts['os']` value is checked to determine if the target system is Linux or not. For a full list of available facts please reference the [Vetting Plugins](plugins/#Vetting) documentation.
