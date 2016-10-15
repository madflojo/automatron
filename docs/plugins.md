## Discovery

Plugins for discovering new targets to monitor.

* [nmap](plugins/discovery/nmap) - Nmap wrapper for scanning Networks
* [Web Ping](plugins/discovery/webping) - Listen for POST or GET requests to identify new targets
* [DigitalOcean](plugins/discovery/digitalocean) - Query DigitalOcean's API


## Checks

Plugins used to perform health checks.

### Systems
* [Disk Free](plugins/checks/disk_free) - Check file system disk space utilization
* [Memory Free](plugins/checks/mem_free) - Check memory utilization

## Actions

Plugins used for Automatron actions.

### CloudFlare
* [CloudFlare DNS](plugins/actions/cloudflare-dns) - Modify, Add or Delete CloudFlare hosted DNS entries

### Docker
* [Docker Clean](plugins/actions/docker/clean) - Remove all Docker containers and images

## Vetting

Gather information from targets to populate `facts` values.

### On Target
* [Services](plugins/vetting/ontarget/services) - Identify system services and their current state
* [System Info](plugins/vetting/ontarget/system_info) - Identify basic system information (i.e. Hostname, IP Address, etc.)

### Remote
* [Ping](plugins/vetting/remote/ping) - True or False value to determine if system is ping-able

## Datastores

Use custom datastores to store Automatrons internal data.

* [Redis](plugins/datastores/redis) - Redis data storage and retrieval

## Logging

Use custom logging modules for Automatron

* [Syslog](plugins/logging/syslog) - Log to custom Syslog end points
* [Console](plugins/logging/console) - Log to the executors console
