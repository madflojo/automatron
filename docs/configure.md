Configuration of Automatron is fairly simple and contained within a single file; `config/config.yml`.

This guide will walk through configuring a basic Automatron instance.

## Copying the `config.yml.example` file

The fastest method to configure Automatron is to start with the example configuration file `config/config.yml.example`. This configuration file contains basic default values which can be used in most implementations of Automatron. To use this file we can simply rename it to the default Automatron configuration file `config/config.yml`.

```sh
$ cp config/config.yml.example config/config.yml
```

Once complete, we can now start customizing our configuration file.

## SSH Details

Automatron relies on SSH to perform both health checks and actions. Within `config.yml` there is an SSH section which will allow us to define the necessary SSH details such as; `user` to authenticate as, a `gateway` or "jump server" for SSH connections and a Private SSH `key`.

```yaml+jinja
ssh: # SSH Configuration
  user: root
  gateway: False
  key: |
        -----BEGIN RSA PRIVATE KEY-----
        this is an example
        -----END RSA PRIVATE KEY-----
```

If the `gateway` setting is left as `False` Automatron will login to each host directly. To specify a "jump server" simply specify the DNS or IP address of the desired server.

```yaml+jinja
  gateway: 10.0.0.1
```

!!! info
    At this time Automatron does not support using sudo or other privilege escalation tools. Any checks or actions will be performed via the user privileges specified in `user`.

## Enable Auto Discovery

By default, Automatron will listen on port `8000` for any HTTP requests. When an HTTP request is made to Automatron the IP will be captured and that server will then be identified as a monitoring target.

There are several plugins that enable other methods for host discovery, in this section we will enable the `nmap` discovery plugin. This configuration is within the `discovery` section of the `config.yml` file.

```yaml+jinja
discovery:
  upload_path: /tmp/
  vetting_interval: 30
  plugins:
    # Web Service for HTTP PINGs
    webping:
      ip: 0.0.0.0
      port: 8000
```

To enable the `nmap` plugin we simply need to append the `nmap` configuration within the `plugins` key.

```yaml+jinja
discovery:
  upload_path: /tmp/
  vetting_interval: 30
  plugins:
    # Web Service for HTTP PINGs
    webping:
      ip: 0.0.0.0
      port: 8000
    # NMAP Scanning
    nmap:
      target: 10.0.0.1/8
      flags: -sP
      interval: 40
```

Each plugin has unique configuration details, the specifics of these plugins can be found in the [plugin](plugins/index.md) documentation.

At this point Automatron has been configured. We can now move on to creating our own [Runbooks](runbooks/index.md).
