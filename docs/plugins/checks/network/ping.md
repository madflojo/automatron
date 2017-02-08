The `ping` plugin is used to identify if a `host` is online by sending an ICMP packet. This plugin uses `bash` and the `ping` command, which should work on most Unix and Linux systems.

## Runbook Example

The below is an example of using the `network/ping` health check in a runbook.

```yaml
checks:
  host_up:
    execute_from: remote
    type: plugin
    plugin: network/ping.sh
    args: -i 10.0.0.1
```

This plugin can be executed from either `target` or `remote` depending on the goal of the runbook.

### Required arguments

The `network/ping` plugin requires 1 argument.

```yaml
args: -i <ip or hostname> [-t <timeout value>]
```

The second value `-t` is an optional value, default is **3 seconds**.
