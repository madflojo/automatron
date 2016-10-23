The `services` Vetting plugin is used to identify services available on monitoring targets and add those details to the targets **facts**. This plugin works by copying and executing the `services.py` plugin executable.

This plugin will output service status similar to the JSON data below.

```json
{
    "services": {
        "acpid": "running",
        "apparmor": "stopped",
        "apport": "running",
        "atd": "running",
        "chef-client": "running",
        "console-setup": "running",
        "cron": "running",
        "cryptdisks": "running",
        "cryptdisks-early": "stopped",
        "dbus": "running",
        "umountnfs.sh": "stopped",
        "umountroot": "stopped",
        "unattended-upgrades": "running",
        "urandom": "running",
        "virtualbox-guest-utils": "running",
        "virtualbox-guest-x11": "stopped",
        "x11-common": "running"
    }
}
```

This data will then be used to populate the `facts['services']` dictionary available within Automatron's facts system.

### OS Support

  * Linux
