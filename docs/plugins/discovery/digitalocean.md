The `digitalocean` Discovery plugin is used to discover new Digital Ocean Droplets. This plugin will periodically perform an HTTP GET request against Digital Ocean's API. All droplets identified are then added to the "potential targets" queue.

## Configuration

This plugin does require some configuration in Automatron's master configuration file `config.yml`.

```yaml
discovery:
  plugins:
    digitalocean:
      url: http://example.com
      api_key: example
      interval: 60
```

The `digitalocean` plugin requires two configuration items.

* `url` - This is the URL of Digital Ocean's API
* `api_key` - This is the Digital Ocean API key
* `interval` - This is the frequency to query Digital Ocean's API
