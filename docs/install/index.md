In this page you will be guided through a basic installation of Automatron. If you wish to deploy Automatron within a container, you can skip this guide and follow the [Docker deployment](docker.md) instructions.

## Basic Installation

Currently, the simplest method of installing Automatron is by either cloning the [GitHub Repository](https://github.com/madflojo/automatron/) or [downloading](https://github.com/madflojo/automatron/releases) a specific release and installing dependencies.

This guide will walk through cloning the GitHub repository and starting an Automatron instance.

### Prerequisites

The below list is a set of base requirements for installing and running an Automatron instance.

  * Python 2.7 or higher
  * Python-dev Package
  * Pip
  * Redis
  * nmap
  * git
  * libffi-dev
  * libssl-dev
  * build-essential

On Ubuntu systems these can be installed with the following command.

```sh
$ sudo apt-get install python2.7 python-dev \
                       python-pip redis-server \
                       nmap git libffi-dev \
                       build-essential libssl-dev
```

Once installed we can proceed to Automatron's installation

### Clone from Github

The first installation step is to simply clone the current repository from GitHub using `git` and change to the newly created directory.

```sh
$ git clone https://github.com/madflojo/automatron.git
$ cd automatron
```

This will place the latest `master` (production ready) branch into the `automatron` directory.

### Install required python modules

The second installation step is to install the required python modules using the `pip` command.

```sh
$ sudo pip install -r requirements.txt
$ sudo pip install honcho
```

With the above two steps complete, we can now move to [Configuration](/configure.md).

## Starting Automatron

In order to start Automatron you can simply execute the command below.

```sh
$ honcho start
```

To shut down Automatron you can use the `kill` command to send the `SIGTERM` signal to the running processes.

## Dashboard

To view the Automatron dashboard simply open up `http://<instance ip>:8000` in your favorite browser. As target nodes are identified and runbooks are executed, events will start to be reflected on the dashboard.
