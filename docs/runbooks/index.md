The core of Automatron is based around **Runbooks**. Runbooks are policies that define health checks and actions. You can think of them in the same way you would think of a printed runbook. Except with Automatron, the actions are automated.

Below is a very simple Runbook example.

```yaml+jinja
name: Check NGINX
schedule: "*/2 * * * *"
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
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
```

This guide will walk through creating the above runbook as well as applying this runbook to all monitored hosts.

## Creating the Runbook YAML file

By default, Runbooks are specified within the `config/runbooks` directory. The runbook we will be creating is used to manage the NGINX service. We will want this runbook to be easy to find. An easy way to do that would be to create the runbook with a similar name as the service it manages. We can do so in one of two ways.

We can either create a file `config/runbooks/nginx.yml` or `config/runbooks/nginx/init.yml`. Either option are acceptable for the next steps. For this guide we will create the file as `config/runbooks/nginx/init.yml`.

```sh
$ mkdir -p config/runbooks/nginx
$ vi config/runbooks/nginx/init.yml
```

To get started let's go ahead and create the runbook by inserting our example runbook.

```yaml+jinja
name: Check NGINX
schedule: "*/2 * * * *"
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
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
```

## The Anatomy of a Runbook

A runbook consists of 4 major parameters; `name`, `schedule`, `checks`, & `actions`.

### Name

The `name` field is used to provide an arbitrary name for the runbook. This field is a required field and must have some value. It is required that this value be unique and not re-used by other runbooks as this name will be referenced internally within Automatron.

### Schedule

The `schedule` field is used to provide a cron formatted schedule for health check execution. A cron formatted schedule of `*/2 * * * *` will result in the health checks being executed every 2 minutes.

!!! warning
    Due to YAML formatting the cron schedule should be encased in single or double quotes such as `'*/2 * * * *'`. Failure to do so will result in a parsing error from YAML.

#### Alternative schedule format

It is also possible to define a schedule in a key/value based cron format such as the example below.

```yaml+jinja
schedule:
  second: '*/15'
  minute: '*'
  hour: '*'
  day: '*'
  month: '*'
  day_of_week: '*'
```

Using this format you may omit keys that have a value of `*` as this is the default value. For example, the above schedule could also be represented as the below.

```yaml+jinja
schedule:
  second: '*/15'
```

!!! warning
    When using the key/value based format it is important to specify the `second` parameter, as a default value of `*` would result in checks being run every second.

### Checks

The `checks` field is a YAML dictionary that contains the health checks to be executed against monitored hosts. The format of `checks` is as follows.

```yaml+jinja
checks:
  name_of_check:
    # health check options
  another_check:
    # health check options
```

For more details around required health check parameters please read the [Checks](checks.md) section.

### Actions

Like `checks`, the `actions` field is a YAML dictionary that contains actions to be executed based on health check status. The `actions` field also follows a similar format to the `checks` field.

```yaml+jinja
actions:
  name_of_action:
    # Action options
  another_action:
    # Action options
```

For more details around required action parameters please read the [Actions](actions.md) section.

## Applying the Runbook

By creating the `config/runbooks/nginx/init.yml` we have only defined the runbook itself. This runbook however will not be applied to any monitored hosts until we specify which hosts it should be applied to.

To do this we will need to edit the `config/runbooks/init.yml` file. This file is a master list of any runbook to host mappings. To apply our runbook to all hosts we can simply insert the following into this file.

```yaml+jinja
'*':
  - nginx
```

The first field `'*'` is a Glob based matching used against the target hostname. In this case since the value is `*`, all hosts will be matched.

If we wished to limit this runbook to severs with naming scheme of `web001.example.com` we could do so with the following modification.

```yaml+jinja
'web*':
  - nginx
```

### Specifying multiple targets and runbooks

It is possible to specify multiple host and runbook mappings such as the above. The below is an example of what an `runbooks/init.yml` may look like for a environment hosting a two tier web application.

```yaml+jinja
'*':
  - cpu
  - mem_free
  - disk_free
  - ntp
  - ssh
'web*':
  - nginx
  - uwsgi
'db*':
  - mysql
```

At this point we have a basic runbook that is being applied to all hosts. To make these changes take effect, simply restart Automatron.
