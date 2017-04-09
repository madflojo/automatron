## Discovery

Plugins for discovering new targets to monitor.

* [nmap](discovery/nmap) - Nmap wrapper for scanning Networks
* [Web Ping](discovery/webping) - Listen for POST or GET requests to identify new targets
* [DigitalOcean](discovery/digitalocean) - Query DigitalOcean's API


## Checks

Plugins used to perform health checks.

  * Systems
    * [Disk Free](checks/systems/disk_free) - Check file system disk space utilization
    * [Memory Free](checks/systems/mem_free) - Check memory utilization

It is also possible to import the [Monitoring Plugins Project](https://www.monitoring-plugins.org/) or plugins from [Nagios Exchange](https://exchange.nagios.org/) into Automatron by copying the plugins into the `plugins/checks` directory. Once included the executables can be referenced by Automatron's runbooks.

## Actions

Plugins used for Automatron actions.

  * CloudFlare
    * [DNS](actions/cloudflare/dns) - Modify, Add or Delete CloudFlare hosted DNS entries
  * Docker
    * [Docker Clean](actions/docker/clean) - Remove all Docker containers and images
  * Systems
    * [Services](actions/systems/services) - Perform an action on a specified services

## Vetting

Gather information from targets to populate `facts` values.

  * On Target
    * [Services](vetting/ontarget/services) - Identify system services and their current state
    * [System Info](vetting/ontarget/system-info) - Identify basic system information (i.e. Hostname, IP Address, etc.)
  * Remote
    * [Ping](vetting/remote/ping) - True or False value to determine if system is ping-able

## Datastores

Use custom datastores to store Automatrons internal data.

  * Redis - Redis data storage and retrieval

## Logging

Use custom logging modules for Automatron

  * [Syslog](logging/syslog) - Log to custom Syslog end points
  * [Console](logging/console) - Log to the executors console
