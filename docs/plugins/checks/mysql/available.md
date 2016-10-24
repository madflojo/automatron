The `available` plugin is used to query MySQL's internal status system and determine whether the MySQL service is available or not.

## Runbook Example

The below is an example of using the `mysql/available` health check in a runbook.

```yaml
checks:
  mysql_up:
    execute_from: ontarget
    type: plugin
    plugin: mysql/available.py
    args: --host=localhost --user=USERNAME --password=YOURPASSWORD
```

This plugin can be executed from either `ontarget` or `remote` depending on the MySQL service's configuration.

### Required arguments

The `mysql/available` plugin requires 3 arguments.

```yaml
args: -s <mysql host> -u <mysql user> -p <mysql password>
```

If the `show status` query is unsuccessful or does not find the key it is looking for the check will return a `CRITICAL` status. There is no `WARNING` or `UNKNOWN` status for this check.
