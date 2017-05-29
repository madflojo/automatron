Vetting plugins are used during the host discovery process to identify [facts](/facts.md) for target systems. These are simple executables that live in either `plugins/vetting/ontarget` or `plugins/vetting/remote`. The vetting plugins located within the `ontarget` directory are copied to the monitored host and executed. Plugins located within the `remote` directory are executed remotely from the Automatron instance.

Much like other plugins within Automatron these plugins are language agnostic. The only requirement for these executables is that they return a JSON structure with the identified facts specified.

The below example shows a simple `ping` status vetting plugin.

```bash
#!/usr/bin/env bash
## Ping server then return true or false JSON

if [ -z $1 ]
then
    exit 1
fi

/bin/ping -c 1 $1 > /dev/null 2>&1
if [ $? -eq 0 ]
then
    echo '{"ping": true}'
else
    echo '{"ping": false}'
fi
```

This plugin is designed to live within the `plugins/vetting/remote` path, as such it accepts a single argument `$1` which will be either the IP or Hostname of the desired target. All plugins in the `remote` directory are executed with this single argument, whereas plugins in the `ontarget` path are executed with no arguments.

This plugin will produce a single fact that is accessible as `{{ facts['ping'] }}`.

!!! tip
    Another, more complex example vetting plugin can be found with the [system_info.py](https://github.com/madflojo/automatron/blob/master/plugins/vetting/ontarget/system_info.py) plugin.
