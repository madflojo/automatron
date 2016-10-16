The `mem_free` health check is used to check whether the available memory on a system is within threshold.

### OS Support

  * Linux
    * Debian Base (Debian, Ubuntu, etc.)
    * RedHat Base (RHEL, CentOS)
  * FreeBSD

For Linux systems this check script does take into consideration the memory used for cache and Linux's ability to reclaim that memory.

## Runbook example

The below is an example of the `mem_free` check used within a runbook.

```yaml
checks:
  mem_free:
    execute_from: ontarget
    type: plugin
    plugin: systems/mem_free.py
    args: --warn=20 --critical=10
```

In the above, the health check will return a `WARNING` status if the memory is below `20%` and return a `CRITICAL` status if the memory is below `10%`.

### Required Arguments

The `mem_free` check requires 2 arguments.

```yaml
args: --warn=<warning threshold %> --critical=<critical threshold %>
```
