Auomatron leverages the power of [Jinja2](http://jinja.pocoo.org/docs/2.9/), a popular Python based templating language to enhance how runbooks can be used. The below example is a runbook that leverages Jinja2.

```yaml+jinja
name: Check NGINX
{% if "prod" in facts['hostname'] %}
schedule:
  second: */20
{% else %}
schedule: "*/2 * * * *"
{% endif %}
checks:
  nginx_is_running:
    execute_from: target
    type: cmd
    cmd: service nginx status
  port_443_is_up:
    execute_from: target
    type: plugin
    plugin: network/tcp_connect.py
    args: --host={{ facts['network']['eth0']['v4'][0] }} --port 443
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
  remove_from_dns:
    execute_from: remote
    trigger: 0
    frequency: 0
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: plugin
    plugin: cloudflare/dns.py
    args: remove test@example.com apikey123 example.com --content {{ facts['network']['eth0']['v4'][0] }}
```

The above runbook leverages both Jinja2 and Automatron's internal **Facts**. Facts are variables that Automatron has collected during the Vetting process of each monitored system.

When Automatron discovers a new host it executes Vetting Plugins on the host. Some plugins are executed remotely, others are executed on the host itself. These plugins return information unique to each host.

An example of the type of information can be seen in the `ontarget/system_info.py` vetting plugin. This plugin creates facts for OS Distribution, Hostname, Kernel version and Network Information.

## A Deeper Look

To get a better understanding of facts, and how they can be used let's look at the facts used in the above example. The below example is an example of using the `hostname` fact to determine if the target is a "production" hostname or not.

```yaml+jinja
{% if "prod" in facts['hostname'] %}
schedule:
  second: */20
{% else %}
schedule: "*/2 * * * *"
{% endif %}
```

This next example uses another fact to determine the IPv4 address of the monitors host. This address is then used as an argument for the `tcp_connect.py` plugin.

```yaml+jinja
port_443_is_up:
  execute_from: target
  type: plugin
  plugin: network/tcp_connect.py
  args: --host={{ facts['network']['eth0']['v4'][0] }} --port 443
```

The above are simple examples of how Jinja and Facts used together can enable the creation of runbooks that can span multiple hosts and use cases.
