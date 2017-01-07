The `linode` Discovery plugin is used to discover new Linode servers. This plugin will periodically perform an HTTP GET request against Linode's API. All servers identified are then added to the "potential targets" queue.

## Configuration

This plugin does require some configuration in Automatron's master configuration file `config.yml`.

```yaml
discovery:
  plugins:
    linode:
      url: http://example.com
      api_key: example
      interval: 60
```

The `linode` plugin requires three configuration items.

* `url` - This is the URL to Linode's API
* `api_key` - This is the Linode API key
* `interval` - This is the frequency to query Linode's API
