The `status_metrics` plugin is used to query MySQL's internal status system and alert when the defined `metric` exceeds the `warning` and `critical` thresholds.

## Runbook Example

The below is an example of using the `status_metrics` health check in a runbook.

```yaml
checks:
  status_metrics:
    execute_from: ontarget
    type: plugin
    plugin: mysql/status_metrics.py
    args: --warn=20 --critical=10 --metric=slow_queries --host=localhost --user=USERNAME --password=YOURPASSWORD --type=greater
```

This plugin can be executed from either `ontarget` or `remote` depending on the MySQL service's configuration.

### Required arguments

The `mysql/status_metrics` plugin requires 7 arguments.

```yaml
args: -w <warning value> -c <critical value> -t {greater, lesser} -m <metric> -s <mysql host> -u <mysql user> -p <mysql password>
```

The `type` flag is used to define whether or not the alert is triggered when the `metric` value is "greater" or "lesser" than the values defined as `warn` and `critical`.
