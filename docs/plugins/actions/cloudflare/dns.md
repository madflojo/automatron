# CloudFlare DNS Actions

This plugin provides the ability to `add`, `remove` and `modify` DNS records for CloudFlare protected domains.

With this plugin you could change a DNS record to a failover IP, remove IP's for round-robin DNS load balancing or even add new systems to DNS if services are running.

## Runbook example for CloudFlare DNS

The below is an example of using the CloudFlare DNS plugin within a Runbook.

```yaml
actions:
  add_dns_record:
    execute_from: remote
    trigger: 0
    frequency: 300
    call_on:
      - OK
    type: plugin
    plugin: cloudflare/dns.py
    args: add email@example.com api_key example.com www.example.com A 10.0.0.1
```

## Actions

The CloudFlare DNS Plugin has 3 actions

  * `add` - Add a new DNS record
  * `remove` - Remove existing DNS record
  * `modify` - Modify an existing DNS record

### Add Arguments

Adding a new DNS record can be called by specifying the following plugin arguments.

#### Syntax

```yaml
args: add <email> <api_key> <domain> <record_name> <record_type> <record_content>
```

#### Example

```yaml
args: add email@example.com api_key example.com www.example.com A 10.0.0.1
```

Supported record types are: `A`, `AAAA`, `CNAME`, & `MX`

#### Optional Arguments

 * `--ttl` - Specify the TTL value (default: 0)
 * `--noproxy` - Disable CloudFlare's proxying

### Remove Arguments

Removing a DNS record can be called by specifying the following plugin arguments.

#### Syntax

```yaml
args: remove <email> <api_key> <domain> --name <record_name> --content <record_content>
```

#### Example

```yaml
args: remove email@example.com api_key example.com --name test.example.com --content 10.0.0.1
```

#### Optional Arguments

The `--name` or `--content` flags can be used together or on their own to limit the number of records to be deleted. At least one flag must be used or no records will be deleted.

  * `--name` - Match records with a specified name
  * `--content` - Match records with a specified content

### Modify Arguments

DNS records can be modified using the following plugin Arguments

#### Syntax

```yaml
args: remove <email> <api_key> <domain> <old_record_content> <new_record_type> <new_record_content>
```

#### Example

```yaml
args: modify email email@example.com api_key example.com 10.0.0.1 A 10.0.0.2
```

#### Optional Arguments

If no `--name` is specified the CloudFlare DNS plugin will modify all records with the matching content. Specifying name will limit the modification to only the named record.

  * `--name` - Match records with a specified name
