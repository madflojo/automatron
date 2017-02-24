The `tcp_connect` plugin is used to identify if a `host` or `ip` is listening on a specified `port`. This is a simple check that is either `OK` for successful connections or `CRITICAL` for unsuccessful connections.

## Runbook Example

The below is an example of using the `network/tcp_connect` health check in a runbook.

```yaml
checks:
  mysql_up:
    execute_from: target
    type: plugin
    plugin: network/tcp_connect.py
    args: --host=localhost --port 3306
```

This plugin can be executed from either `target` or `remote` depending on the target being monitored.

### Required arguments

The `network/tcp_connect` plugin requires 2 arguments.

```yaml
args: -i <ip or hostname> -p <port> [-t <timeout value>]
```

The third value `-t` is an optional value, default is **5 seconds**.
