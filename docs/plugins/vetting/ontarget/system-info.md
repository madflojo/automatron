The `system-info` Vetting plugin is used to collect basic system information of monitoring targets. This information is then used to feed Automatron's **facts** system. This plugin works by copying the `system_info.py` executable and executing it on the monitoring target.

The below JSON output shows the expected results.

```json
{
    "hostname": "vagrant-ubuntu-trusty-64",
    "kernel": "3.13.0-55-generic",
    "network": {
        "docker0": {
            "v4": [
                "172.17.42.1"
            ],
            "v6": []
        },
        "eth0": {
            "v4": [
                "10.0.2.15"
            ],
            "v6": [
                "fe80::a00:27ff:fe3a:b5b"
            ]
        },
        "lo": {
            "v4": [
                "127.0.0.1"
            ],
            "v6": [
                "::1"
            ]
        }
    },
    "os": "Linux"
}
```

This information populates the `facts['hostname']`, `facts['kernel']`, `facts['network']` and `facts['os']` values.
