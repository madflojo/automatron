The `nmap` Discovery plugin utilizes the **nmap** tool to scan a specified network for new target hosts. Each host found to be up will be added as a potential target system for Automatron to monitor. This plugin acts as a simple wrapper around `nmap` which is determining if a host is up or down based on the options provided.

## Configuration

This plugin does require some configuration in Automatron's master configuration file `config.yml`.


```yaml
discovery:
  plugins:
    nmap:
      target: 10.0.0.1/8
      flags: -sP
      interval: 40
```

The above configuration has three main elements.

* `target` - This is the target to pass on to `nmap`.

The value of `10.0.0.1/8` will scan the entire `10.0.0.0` class A network.

* `flags` - These are flags you would pass to `nmap` when run from command line.

The value of `-sP` will perform a Ping based scan.

* `interval` - The specified "interval" (in seconds) to wait before performing another scan.
