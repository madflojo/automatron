# Automatron

Automatron **(Ah-Tom-a-tron)** is an open source framework designed to detect and remediate IT systems issues. Meaning, it can be used to monitor systems and when it detects issues, correct them.

[![Build Status](https://travis-ci.org/madflojo/automatron.svg?branch=develop)](https://travis-ci.org/madflojo/automatron) [![Coverage Status](https://coveralls.io/repos/github/madflojo/automatron/badge.svg?branch=develop)](https://coveralls.io/github/madflojo/automatron?branch=develop)


## Overview

Automatron can be broken down into 4 main components:

* **Discovery**, Automated discovery of new systems
* **Runbooks**, Monitor and Action policies
* **Monitoring**, Agent-less monitoring via Nagios compliant scripts or command execution
* **Actioning**, Using Actions defined within Runbooks to execute both on target and remote scripts or commands

With Automatron and a few minutes you can setup a fully autonomous monitoring and remediation system. The below steps will show how to install and configure Automatron to monitor Nginx on all web servers and restart the service if it is not running.

### Install and Configure Automatron

Automatron is currently available by cloning the [GitHub Repository](https://github.com/madflojo/automatron/). With the first release candidate it will also be available via a Docker image.

#### Prerequisites

The below list is a set of base requirements for a running Automatron instance.

  * Python 2.7 or higher
  * Redis
  * nmap

#### Clone from Github

First, clone the current repository from GitHub.

```sh
$ git clone https://github.com/madflojo/automatron.git
$ cd automatron
```

#### Install required python modules

Second, install any required python modules.

```sh
$ sudo pip install -r requirements.txt
$ sudo pip install honcho
```

#### Setup a base configuration

Third, create a configuration file using the `config/config.yml.example` file as a base.

```sh
$ cp config/config.yml.example config/config.yml
$ vi config/config.yml
```

###### Defining an SSH Key

Automatron relies on SSH to perform both monitoring and actioning. To enable this a public SSH key must be deployed on all target servers and the private key stored within the `ssh` section of the configuration file.

```
ssh: # SSH Configuration
  user: root
  gateway: False
  key: |
        -----BEGIN RSA PRIVATE KEY-----
        fdlkfjasldjfsaldkjflkasjflkjaflsdlkfjs
        -----END RSA PRIVATE KEY-----
```

The `gateway` setting can be used to specify a "jump server" for Automatron to connect to. If left as `False` Automatron will simply login to each target host directly.

###### Setup the nmap Discovery plugin

Automatron discovers new hosts via two default methods, the first is a web "ping" which can be any HTTP request to the port specified within the configuration file.

The second method is a `nmap` scan. Within the config file you can specify a custom network subnet for Automatron to scan.

```
## Use NMAP to find new hosts
nmap:
  target: 10.0.0.1/8
  flags: -sP
  interval: 40
```

The `flags` configuration is used to pass command line arguments to `nmap`.

### Writing our first Runbook

A Runbook is a policy that defines health checks and automated actions to be performed when those health checks return specified states.

For this example we will create a new Runbook.

```sh
$ mkdir -p config/runbooks/base/check_nginx
$ vi config/runbooks/base/check_nginx/init.yml
```

Once the file is open simply paste the following Runbook policy.

```
name: Verify nginx is running
schedule: "*/5 * * * *"
nodes:
  - "*web*"
checks:
  nginx_is_running:
    # Check if nginx is running
    execute_from: ontarget
    type: cmd
    cmd: service nginx status
actions:
  restart_nginx:
    execute_from: ontarget
    trigger: 2
    frequency: 300
    call_on:
      - WARNING
      - CRITICAL
    type: cmd
    cmd: service nginx restart
```

The above policy will run the `service nginx status` command every 5 minutes on any target that has a hostname that matches `*web*`. If that command fails after 2 occurrences the `restart_nginx` action will be "triggered" and executed on the target server.

## Applying Runbooks to Target hosts

Within the Runbook above we specified the target nodes that the runbook applies to. There is another level of targeting available within the `config/runbooks/init.yml` file. This provides additional granularity to the application of Runbooks.

To get started we will replace the contents of this file with settings specific to our current task.

```
'*':
  - base/check_nginx
```

### Starting Automatron

Once our configuration and runbook is defined we can startup Automatron and watch as our webservers are discovered and monitored autonamously.

```sh
$ honcho start
```
