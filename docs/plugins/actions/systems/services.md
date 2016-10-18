The `systems/services.py` plugin is used to perform actions on system services such as **nginx**, **docker** or **postfix**. You can use this plugin to perform any action supported by the underlying system management utility such as **Systemd**. This plugin is useful when you have an environment that has a mix of Linux versions and you wish to use one runbook to interact with system services.

### OS Support

  * Linux


## Runbook example

The below is an example of using the **systems/services.py** plugin.

```yaml
actions:
  restart_nginx:
    execute_from: ontarget
    trigger: 0
    frequency: 300
    call_on:
      - CRITICAL
    type: plugin
    plugin: systems/services.py
    args: --service nginx --action restart
```

The above would restart **Nginx** after a `CRITICAL` event.

### Required Arugments

This plugin requires 2 arguments.

```yaml
args: --service <service name> --action <aciton to perform>
```
