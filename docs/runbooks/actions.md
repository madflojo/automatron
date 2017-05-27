When a runbook health check returns a state; Automatron will check the runbooks definition to determine if an action should be taken. Like health checks, actions come in two flavors. **Arbitrary shell commands** and **Plugin executables**. In this guide we will be defining two actions, one of each type.

During this guide we will be building runbook actions for the below runbook.

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

Within this runbook there are two actions; `restart_nginx` and `remove_from_dns`. In this guide we will be breaking down these two actions to gain a better understanding of how they work.

## A command based actions

Like health checks, Automatron actions also support arbitrary shell commands. When executing this type of action Automatron simply logs into the target system and executes the defined command.

The below example is a simple action that logs into the target system and executes the `service nginx restart` command.

```yaml+jinja
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

This action has 6 main fields defined; `execute_from`, `trigger`, `frequency`, `call_on`, `type`, and `cmd`. Let's break down what each of these fields specify and control about action execution.

### Execute from

The `execute_from` field is used to specify where to run the action. Acceptable values for this field are `target`, `remote` and `host`.

  * `target` - This value will specify that the action should be executed on the monitored host.
  * `remote` - This value will specify that the action is executed from the Automatron server.
  * `host` - This value will specify that the action is executed from another specified host.

When using the `host` value, the alternative host must be specified via a key named `host`. Below is an example of a `host` based action.

```yaml+jinja
actions:
  restart_mysql:
    execute_from: host
    host: 10.0.0.2
    trigger: 0
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
    type: cmd
    cmd: service mysql restart
```

The above action will result in Automatron logging into `10.0.0.2` and executing `service mysql restart`.

### Trigger

The `trigger` field is used to specify the number of times a health check returns the state specified within `call_on`. This number **must be reached consecutively**. If for example, the health check returns `WARNING` and then `OK`; Automatron's internal counter will be reset.

### Frequecy

The `frequency` field is used to specify the time (in seconds) between action execution. In the above example the action will be executed every `300` seconds until either the `call_on` or `trigger` conditions are no longer met.

If you wish to execute an action every time, simply set this value to `0` seconds.

### Call on

The `call_on` field is a YAML list which is used to list the states that should trigger this action. Valid options are `OK`, `WARNING`, `CRITICAL` & `UNKNOWN`.

### Type

The `type` field is used to specify what type of action will be performed. Acceptable values are `cmd` or `plugin`. This field is required for all actions. Since our action above is a command based action we will specify `cmd`.

### Command

The `cmd` field is used to specify the shell command to execute as part of this action. In the example above the command is simply `service nginx restart`. When this action is executed, Automatron will login to the host specified and execute that command.

## A plugin based action

When a command based action is being executed Automatron will login to the target host and execute the command specified. With plugin based actions, Automatron will upload the plugin executable and execute it giving the specified arguments.

Below is a sample Runbook using a plugin based action.

```yaml+jinja
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

This action has 7 main fields defined; `execute_from`, `trigger`, `frequency`, `call_on`, `type`, `plugin` and `args`. Let's break down what each of these fields specify and control about action execution.

### Execute from, Trigger, Frequency, Call on & Type

As `execute_from`, `trigger`, `frequency`, `call_on`, and `type` are common fields for every runbook. The way they are applied for plugin actions is the same as the way they are applied for command based actions. As such we will skip repeating these fields in this section.

### Plugin

The `plugin` field is used to specify the location of the plugin executable. This is a relative file path starting from the value of the `plugin_path` parameter located within the `config/config.yml` configuration file.

For example, a plugin located at `/path/to/plugins/actions/myaction/myaction.pl` would require the value of `myaction/myaction.pl`.

### Plugin Arguments

The `args` field is used to specify the arguments to provide the plugin executable. In the example above the plugin will be executed as follows by Automatron

```sh
$ /path/to/plugins/checks/cloudflare/dns.py remove test@example.com apikey123 example.com --content 10.0.0.1
```
