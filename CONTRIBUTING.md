# Contributing to Automatron

Community contributions are essential to the growth of Automatron. Both code and documentation contributions are not only welcomed, they are encouraged. The following guidelines will explain how to get started with contributing to this project.

## Accept our Contributor License Agreement

Before starting to contribute to Automatron please review and accept our [Contributor License Agreement](https://goo.gl/forms/44vauc2jjlNlln2t1)

## Core vs. Plugins

Contributing to the Core platform and contributing Plugins have two different guidelines and requirements. The below will explain some basic concepts of how to contribute different functionality.

### Contributing to Core

Automatron follows a pluggable architecture with the majority of features being provided by plugins located within the `plugins/` directory. This allows us to keep the Core framework minimal and simple.

At this time there are 4 primary core components of Automatron.

  * `discovery` - This component is used to launch node Discovery plugins which serve the purpose of finding new nodes to monitor.
  * `runbooks` - The Runbooks component is used to parse and update the monitoring and actioning "rules" applied to monitored nodes.
  * `monitoring` - Monitoring is a component that is used to schedule defined checks as well as launching and executing the defined check.
  * `actioning` - The Actioning component listen for events based on checks and performs actions specified within Runbooks.

These components are written in Python and as such should follow basic Python development practices.

### Contributing Plugins

Where the Automatron Core provides a monitoring and actioning framework, the functional features are all provided by Automatron Plugins. Plugins, are the fastest way to add features to Automatron. As such it is suggested that new contributors start by adding a plugin before adding core functionality.

Plugin contributions have been migrated to the [Automatron Plugins](https://github.com/Automatron-Plugins) project. Pull Requests for existing plugins should be opened against the appropriate repository in that project. Requests for new plugin repositories can be made via [Gitter](https://gitter.im/madflojo/automatron).

#### Executable Plugins

At this time there are 6 types of Plugins.

  * `actions` - Executables used to perform corrective actions.
  * `checks` - Executables used to check system health (Nagios compatible).
  * `datastores` - Python modules used by Automatron Core to access datastores.
  * `discovery` - Python modules used by Automatron to automatically detect new monitoring targets.
  * `logging` - Python modules used to provide custom logging mechanisms to Automatron Core.
  * `vetting` - Executables used to identify `facts` for discovered monitoring targets.

While `datastores`, `logging`, and `discovery` plugins are Python modules; `actions`, `checks` and `vetting` are simply executables.
These plugins may be written in Python, Perl, BASH or any language that results in a standalone executable.

## Contribution Workflow & Requirements

Automatron follows a workflow very similar to the GitHub flow.

Pull Requests for new features should be opened against the `develop` branch. It is recommended to create a feature branch on your local repository from the `develop` branch to avoid merge conflicts or and ease the integration process.

```console
$ git checkout develop
$ git checkout -b new-feature
```

Periodically the `develop` branch will be merged into the `master` branch to start the process of creating a new release. Prior to merging changes into `master` a release branch will be created for the previous release base.

When opening a Pull Request for a bug fix, if the fix is for the current release, the Pull Request should be opened to the `master` branch. If the fix is for a previous release, the Pull Request should be opened to the release specific branch.

If the bug fix should also be incorporated with the `develop` branch a second Pull Request should be opened to the `develop` branch.

### Tests are required for Core

Any Pull Requests for the Automatron core code base should include applicable `unit`, `integration` and `functional` tests. Automatron uses Coveralls to ensure code coverage does not decrease with each Pull Request.

### Documentation is required

Documentation of new functionality is important to increase the adoption of Automatron. As such, you may be asked to provide documentation for new functionality created by your Pull Request. This is especially true for major feature changes.

Documentation is just as important as new functionality, as such documentation based pull requests are encouraged.

## Developer environment

To ease the development and testing experience of Automatron a `docker-compose` environment has been created and is included within the repository.

To launch a local instance of Automatron simply execute the following `docker-compose` command.

```console
$ sudo docker-compose up --build automatron
```

If you wish to execute tests you can do so by running the following `docker-compose` command.

```console
$ sudo docker-compose up --build test
```

To test documentation updates you can launch a `mkdocs` container as well.

```console
$ sudo docker-compose up --build mkdocs
```

To wipe and reset the `docker-compose` environment simply run the following.

```console
$ sudo docker-compose down
```
