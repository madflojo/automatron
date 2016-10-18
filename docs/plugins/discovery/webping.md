The `webping` Discovery plugins will start an HTTP listener and wait for incoming `GET` or `POST` requests. Whenever it receives a request, the `webping` plugin will extract the client's IP address and add that system to the "potential targets" queue.

This plugin provides an easy way to have targets notify Automatron of their existence.

## Configuration

This plugin does require some configuration in Automatron's master configuration file `config.yml`.

```yaml
discovery:
  plugins:
    webping:
      ip: 0.0.0.0
      port: 20000
```

The above configuration has two elements.

* `ip` - This is the IP address to bind to.
* `port` - This is the port the HTTP listener should bind and listen to.
