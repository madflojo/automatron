Runbooks within Automatron are used to define the health checks to run on target nodes and the actions to perform based on those health checks. This guide is a reference for the various options used when defining a runbook.

## Basic Runbook Example

The below example is a basic Runbook that monitors the status of **nginx** by executing the `service nginx status` command and restarts **nginx** if that command is not successful.

```yaml
name: Verify nginx is running
schedule: "*/5 * * * *"
nodes:
  - "*web*"
checks:
  nginx_is_running:
    # Check if nginx is running
    execute_from: ontarget
    type: cmd
    cmd: service nginx status
actions:
  restart_nginx:
    execute_from: ontarget
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
    type: cmd
    cmd: service nginx restart
```

The format of a Runbook is written in [YAML](http://yaml.org/). This format allows for simple parsing of Runbooks while retaining a human friendly format. YAML is also a very common configuration language used by many automation tools which should reduce the ramp up time for those who are experienced with other infrastructure automation tools.

## Runbook Reference

The below is a detailed reference for the available options within a Runbook. At this moment all fields specified within this reference are required fields.

### `name`

The `name` field is used to provide an arbitrary name to the Runbook. This field is a required field and must have some value. It is suggested that this value be unique and not re-used by other Runbooks.

### `schedule`

The `schedule` field is used to provide a cron formatted schedule for health check execution. The specified cron schedule will be used to establish the frequency for executing the health checks defined within the Runbook.

### `nodes`

The `nodes` field is a YAML list used to specify which target nodes this runbook should be applied to. This list is based on the hostname value of the nodes.

In the example above the value is `*web*`, since Automatron supports globbing for the `nodes` field this would mean this runbook is applied to any hosts that have the word "web" in their hostname.

Hostnames are obtained during the target vetting process from the systems itself. If the hostname changes from vetting time to execution time that change will not be reflected in runbook processing.

As previously mentioned this field is a YAML list which allows for multiple values to be added. The example below shows how to add multiple node targets.

```yaml
nodes:
  - "*web*"
  - "*caching*"
```

### `checks`

The `checks` field is a YAML dictionary that contains the health checks to be executed against the specified nodes in the `nodes` list.

The format of `checks` is as follows.

```yaml
checks:
  name_of_check:
    # health check options
  another_check:
    # health check options
```

The name key for each check is arbitrary and mainly used for logging, however it should be unique within the same Runbook.

#### Health Check Types

Automatron supports 2 types of health checks; `cmd` and `plugin`. The `cmd` type is used to execute arbitrary shell commands and the `plugin` type is used to upload and execute an executable.

Depending on the type used, the health check has different required options.

#### Command Execution

The `cmd` Check type is used to execute arbitrary shell commands as a health check. The results of this check is determined based on the exit code of the last command executed.

Below is an example of a `cmd` based health check.

```yaml
checks:
  nginx_is_running:
    # Check if nginx is running
    execute_from: ontarget
    type: cmd
    cmd: service nginx status
```

This health check will execute the `service nginx status` command and validate the exit code returned to determine the status of the health check.

With the `cmd` type health check there are 3 main options; `execute_from`, `type` and `cmd`.

##### `type`

The `type` field is used to specify what type of health check this check is. Acceptable values are `cmd` or `plugin`. This field is required for all health checks.

##### `execute_from`

The `execute_from` field is used to specify where to run the health check. Acceptable values for this field are `ontarget` which is used to execute the health check on the node itself and `remote`. The `remote` setting will tell Automatron to execute the health check from the system running Automatron's `monitoring.py` service.

##### `cmd`

The `cmd` field is used to specify the shell command to execute. In the example above the command is simply `service nginx status` however, this field support much more complicated commands such as the below example.

```yaml
checks:
  http_is_accessible:
    execute_from: remote
    type: cmd
    cmd: /usr/bin/curl -Lw "Response %{http_code}\\n" http://10.0.0.1 -o /dev/null | egrep "Response [200|301]"
```

#### Plugin Execution

The `plugin` health check is used to copy a health check plugin from Automatron's plugin path to the target and execute that plugin.

The below example shows a `plugin` based health check.

```yaml
checks:
  disk_free:
    # Check for the % of disk free create warning with 20% free and critical for 10% free
    execute_from: ontarget
    type: plugin
    plugin: systems/disk_free.py
    args: --warn=20 --critical=10 --filesystem=/var/log
```

This health check will login to the target node, upload the `systems/disk_free.py` file to a temporary location and execute it providing the arguments specified in the the `args` field.

With `plugin` health checks there are 4 parameters to be set; `execute_from`, `type`, `plugin` and `args`.

##### `type`

The `type` field is used to specify what type of health check this check is. Acceptable values are `cmd` or `plugin`. This field is required for all health checks.

##### `execute_from`

The `execute_from` field is used to specify where to run the health check. Acceptable values for this field are `ontarget` which is used to execute the health check on the node itself and `remote`. The `remote` setting will tell Automatron to execute the health check from the system running the `monitoring.py` service of Automatron.

##### `plugin`

The `plugin` field is used to specify the location of the plugin file. This is a relative file path starting from the value of the `plugin_path` parameter.

For example, a plugin located at `/path/to/plugins/checks/mycheck/mycheck.pl` would require the value of `mycheck/mycheck.pl`.

##### `args`

The `args` field is used to specify the arguments to provide the plugin executable. In the example above the plugin will be executed as follows by Automatron

```console
$ /path/to/plugin/disk_free.py --warn=20 --critical=10 --filesystem=/var/log
```

#### Exit Codes

Automatron follows the **Nagios** model for health check exit codes. When a health check is executed the exit code is used to inform Automatron of the results. The below list is a map of acceptable exit codes and how they relate to Automatron health check status.

  * `OK`: Requires a successful exit code of `0`
  * `WARNING`: Is indicated by an exit code of `1`
  * `CRITICAL`: Is indicated by an exit code of `2`
  * `UNKNOWN`: Is indicated by any other exit code

### `actions`

Like `checks` the `actions` field is a YAML dictionary that contains actions to be executed based on health check status. The `actions` field also follows a similar format to the `checks` field.

```yaml
actions:
  name_of_action:
    # Action options
  another_action:
    # Action options
```

Also like health checks the name of actions should be unique within a runbook but otherwise arbitrary.

#### Action Types

Actions also have two types, `cmd` and `plugin`. A `cmd` action is used to execute a shell command and `plugin` actions are used to execute an executable plugin file. Both `cmd` and `plugin` have unique options as well as common options. The below section covers the two action types and the options for those types.

#### Command Execution

The `cmd` action type is designed to execute an arbitrary shell command. The below is an example of a `cmd` action.

```yaml
actions:
  restart_nginx:
    execute_from: ontarget
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
    type: cmd
    cmd: service nginx restart
```

##### `execute_from`

The `execute_from` field is used to specify where to run the action. Acceptable values for this field are `ontarget` which is used to execute the health check on the node itself and `remote`. The `remote` setting will tell Automatron to execute the action from the system running the `actioning.py` service of Automatron.

##### `trigger`

The `trigger` field is used to specify the number of times a health check returns the state specified within `call_on`. This number must be reached consecutively. If for example, the health check returns `WARNING` and then `OK`; Automatron's internal counter will be reset.

##### `frequency`

The `frequency` field is used to specify the time (in seconds) between action execution. In the above example the action will be executed every `300` seconds until either the `call_on` or `trigger` conditions are no longer met.

If you wish to execute an action every time, simply set this value to `0` seconds.

##### `call_on`

The `call_on` field is a YAML list which is used to list the states that should trigger this action. Valid options are `OK`, `WARNING`, `CRITICAL` & `UNKNOWN`.

##### `type`

The `type` field is used to specify what type of action this action is. Acceptable values are `cmd` or `plugin`. This field is required for all actions.

##### `cmd`

The `cmd` field is used to specify the shell command to execute as part of this action. In the example above the command is simply `service nginx restart`.

#### Plugin Execution

A `plugin` action type is used to execute Automatron actioning plugins. These plugins are simply executables that are copied to a temporary location and then executed with the specified arguments.

Below is an example of a plugin action that adds a domain's DNS record to CloudFlare.

```yaml
actions:
  add_dns_record:
    execute_from: remote
    trigger: 0
    frequency: 300
    call_on:
      - OK
    type: plugin
    plugin: cloudflare/dns.py
    args: add email@example.com api_key example.com www.example.com A 10.0.0.1
```

##### `execute_from`

The `execute_from` field is used to specify where to run the action. Acceptable values for this field are `ontarget` which is used to execute the health check on the target node itself and `remote`. The `remote` setting will tell Automatron to execute the action from the system running Automatron's `actioning.py` service.

##### `trigger`

The `trigger` field is used to specify the number of times a health check returns the state specified within `call_on`. This number must be reached consecutively. If for example, the health check returns `WARNING` and then `OK`; Automatron's internal counter will be reset.

##### `frequency`

The `frequency` field is used to specify the time (in seconds) between action execution. In the above example the action will be executed every `300` seconds until either the `call_on` or `trigger` conditions are no longer met.

If you wish to execute an action every time, simply set this value to `0` seconds.

##### `call_on`

The `call_on` field is a YAML list which is used to list the states that should trigger this action. Valid options are `OK`, `WARNING`, `CRITICAL` & `UNKNOWN`.

##### `type`

The `type` field is used to specify what type of action this action is. Acceptable values are `cmd` or `plugin`. This field is required for all actions.

##### `plugin`

The `plugin` field is used to specify the location of the plugin file. This is a relative file path starting from the value of the `plugin_path` parameter.

For example, a plugin located at `/path/to/plugins/actions/myaction/myaction.pl` would require the value of `myaction/myaction.pl`.

##### `args`

The `args` field is used to specify the arguments to provide the plugin executable. In the example above the plugin will be executed as follows by Automatron

```console
$ /path/to/plugin/dns.py add email@example.com api_key example.com www.example.com A 10.0.0.1
```

## More Runbook Examples

### Check HTTP Status

This Runbook validates an HTTP service is accessible and will restart the system and remove DNS entries on failure.

```yaml+jinja
name: Verify HTTP is responding to GET requests on target system
schedule: "*/2 * * * *"
nodes:
  - "*"
checks:
  http_is_accessible:
    execute_from: remote
    type: cmd
    cmd: /usr/bin/curl -Lw "Response %{http_code}\\n" http://{{ facts['network']['eth0']['v4'][0] }} -o /dev/null | egrep "Response [200|301]"
actions:
  restart_http:
    execute_from: ontarget
    trigger: 0
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: cmd
    cmd: service nginx restart
  remove_dns:
    execute_from: remote
    trigger: 0
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: plugin
    plugin: cloudflare/dns.py
    args: remove someone@example.com 12345 example.com --content {{ facts['network']['eth0']['v4'][0] }}
  reboot:
    execute_from: ontarget
    trigger: 5
    frequency: 900
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: cmd
    cmd: reboot
```

### Check `/var/logs` available space

This example will validate the free space on the `/var/log` filesystem and if necessary execute a `logrotate` task

```yaml+jinja
name: Verify /var/log
schedule: "*/2 * * * *"
nodes:
  - "*"
checks:
  disk_free:
    # Check for the % of disk free create warning with 20% free and critical for 10% free
    execute_from: ontarget
    type: plugin
    plugin: systems/disk_free.py
    args: --warn=20 --critical=10 --filesystem=/var/log
actions:
  logrotate_nicely:
    execute_from: ontarget
    trigger: 0
    frequency: 300
    call_on:
      - WARNING
    type: cmd
    cmd: bash /etc/cron.daily/logrotate
  logrotate_forced:
    execute_from: ontarget
    trigger: 5
    frequency: 300
    call_on:
      - CRITICAL
    type: cmd
    cmd: bash /etc/cron.daily/logrotate --force
```