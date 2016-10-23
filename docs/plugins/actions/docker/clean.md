This plugin provides the ability to remove ("clean") all Docker containers and images. This plugin will first gather a list of Docker containers running and stopped, then cycle through that list removing and stopping each container. After the running containers are complete this plugin will then gather a list of container images and remove each image it finds.

This plugin should only be used to completely wipe all Docker containers and images.

## Runbook example

The Below is an example of using the `docker/clean.sh` action plugin.

```yaml
actions:
  cleanup_docker:
    execute_from: ontarget
    trigger: 0
    frequency: 300
    call_on:
      - CRITICAL
    type: plugin
    plugin: docker/clean.sh
```

This plugin does not require any arguments to be specified.
