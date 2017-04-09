Automatron determines whether a runbook action should be performed based on the results of a health check. There are two types of health checks within Automatron.  **Arbitrary shell commands** and **Plugin executables**. In this guide we will walk through defining two health checks, one of each type.

The below runbook is a sample that this guide will be based on.

```yaml+jinja
name: Check NGINX
schedule: "*/2 * * * *"
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
  port_443_is_up:
    execute_from: target
    type: plugin
    plugin: network/tcp_connect.py
    args: --host=localhost --port 443
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
    args: remove test@example.com apikey123 example.com --content 10.0.0.1
```

In the above example, there are two health checks defined `nginx_is_running` and `port_443_is_up`. In the below section we will break down each of these health checks to better understand how health checks are defined.

## A command based health check

Command based health checks are one of the simplest concepts in Automatron. This type of health check allows users to define a command that is executed to determine the health status of a target.

This is accomplished by Automatron simply logging into the target system over SSH and executing the defined command. The exit code of the executed command is then used to determine the status of the health check.

The below sample is the `nginx_is_running` command based health check.

```yaml+jinja
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
```

In this sample we can see that there are 3 values required for command based health checks. Those values are `execute_from`, `type`, and `cmd`. Let's go ahead and break down these values to gain a better understanding of what they mean and tell Automatron to do.

### Execute from

The `execute_from` field is used to specify where to run the health check. Acceptable values for this field are `target` which is used to execute the health check on the monitored node itself and `remote`. The `remote` setting will tell Automatron to execute the health check from the system running Automatron itself.

In our case the command we wish to execute can only be executed from the monitored system itself, as such the value of this field will be `target`.

### Type

The `type` field is used to specify what type of health check this check is. Acceptable values are `cmd` or `plugin`. In this case, since we are defining a command based health check our value is set to `cmd`.

### Command

The `cmd` field is used to specify the shell command to execute. In our example the command is simply `service nginx status`. However, this field can support much more complicated commands such as the below example.

```yaml+jinja
cmd: /usr/bin/curl -Lw "Response %{http_code}\\n" http://10.0.0.1 -o /dev/null | egrep "Response [200|301]"
```

It is not uncommon to use multiple commands connected with output redirection and conditionals within a runbook.

## A plugin based health check

Plugin based health checks are similar to Command Based health checks in that the exit code is used to determine status. Where these checks differ is that Automatron will copy an executable to the target system and then execute that executable with the specified arguments.

Below is an example Plugin health check.

```yaml+jinja
port_443_is_up:
  execute_from: target
  type: plugin
  plugin: network/tcp_connect.py
  args: --host=localhost --port 443
```

Plugin type health checks have 4 configuration items `execute_from`, `type`, `plugin` & `args`. Let's go ahead and break down these values to gain a better understanding of what they mean and tell Automatron to do.

### Execute from & Type

The `execute_from` and `type` fields are common fields for every runbook. The way they are applied for plugin health checks is the same as the way they are applied for command based health checks. As such we will skip repeating these fields in this section.

### Plugin

The `plugin` field is used to specify the location of the plugin executable. This is a relative file path starting from the value of the `plugin_path` parameter located within the `config/config.yml` configuration file.

For example, a plugin located at `/path/to/plugins/checks/mycheck/mycheck.pl` would require the value of `mycheck/mycheck.pl`.

### Plugin Arguments

The `args` field is used to specify the arguments to provide the plugin executable. In the example above the plugin will be executed as follows by Automatron

```sh
$ /path/to/plugins/checks/network/tcp_connect.py --host=localhost --port 443
```

## Using Exit Codes to relay health check status

Automatron follows the **Nagios** model for health check exit codes. When a health check is executed the exit code is used to inform Automatron of the results. The below list is a map of acceptable exit codes and how they relate to Automatron health check status.

  * `OK`: Requires a successful exit code of `0`
  * `WARNING`: Is indicated by an exit code of `1`
  * `CRITICAL`: Is indicated by an exit code of `2`
  * `UNKNOWN`: Is indicated by any other exit code

!!! tip
    Since Automatron supports the **Nagios** exit code strategy most Nagios compliant health checks can also be used with Automatron.
