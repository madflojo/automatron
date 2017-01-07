The `roster` Discovery plugin is used to discover new hosts via the Automatron base configuration file. This plugin allows users to simply specify hosts within the main configuration file `config/config.yml`.

## Configuration

This plugin requires configuration in Automatron's master configuration file `config.yml`.

```yaml
discovery:
  plugins:
    roster:
      hosts:
        - 10.0.0.1
        - 10.0.0.3
```

The `roster` plugin requires one configuration items.

* `hosts` - A list of target hosts.
