# Automatron

Automatron **(Ah-Tom-a-tron)** is an open source framework designed to detect and remediate IT systems issues.

[![Build Status]](https://travis-ci.org/madflojo/automatron.svg?branch=develop) [![Coverage Status](https://coveralls.io/repos/github/madflojo/automatron/badge.svg?branch=develop)](https://coveralls.io/github/madflojo/automatron?branch=develop)


## Overview

With a **pluggable** architecture everything from Health Checks to Datastores can be customized with a simple plugin and configuration change.

Automatron can be broken down into 4 main components:

* **Discovery**, Automated discovery of new systems
* **Runbooks**, Hostname based "runbooks" with Jinja2 template support.
* **Monitoring**, Agent-less monitoring via Nagios compliant scripts or command execution
* **Actioning**, Using rules from **Runbooks** to execute both on target and remote scripts/commands

With Automatron you can simple fire it up and watch as it autonomously discovers new hosts, performs health checks on them, and remediates issues it finds. All, out of the box.
