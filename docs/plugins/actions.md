Actions can be as simple as a one-liner shell command or as complicated as a 1,000 line Python script. With Automatron's action plugins both of these scenarios can be covered.

Automatron action plugins are simply executables that are copied and executed on the specified target. There is no special language or coding syntax required other than the fact that the script should be executable without specifying the language.

## A simple example

To understand this further let's write a simple plugin that finds files that require a `dos2unix` conversion and converts them. Before getting into our script, let's start with a runbook for this example.

```yaml+jinja
name: Check if application has started
schedule:
  second: "*/30"
checks:
  port_443_is_up:
    execute_from: target
    type: plugin
    plugin: network/tcp_connect.py
    args: --host=localhost --port 443
actions:
  dos2unix_files:
    execute_from: target
    trigger: 0
    frequency: 900
    call_on:
      - WARNING
      - CRITICAL
      - UNKNOWN
    type: plugin
    plugin: custom/dos2unix.sh
    args: /application/path
```

The above runbook will verify if the application is listening on port 443 and if not execute the `dos2unix_files` action. This action is a plugin action which will copy the `plugins/actions/custom/dos2unix.sh` script to the target server and execute it with the argument of `/application/path`. To explain this better, the below command represents how this plugin would be executed on the target server.

```sh
$ custom/dos2unix.sh /application/path
```

This script itself can be very simple and only needs to accept the arguments passed.

### Sample code

The below script is a sample script that will perform a `dos2unix` conversion on any files within the specified path.

```bash
#!/bin/bash

if [ -z $1 ]
then
  echo "Usage: $0 /path"
  exit 1
fi

BEFORE=$(find $1 -type f -exec file {} \; | grep -c "with CRLF line terminators")

for FILE in `find $1 -type f -exec file {} \; | grep "with CRLF line terminators" | cut -d: -f1`
do
  dos2unix $FILE
done

AFTER=$(find $1 -type f -exec file {} \; | grep -c "with CRLF line terminators")

if [ $AFTER -lt $BEFORE ]
then
  exit 0
else
  exit 1
fi
```

The exit codes used by the action plugin will be used by Automatron to determine successful action execution or a failed action execution. A script that is successful should exit with a code of `0`. Any other exit code will show as a failed action execution.

!!! info
    Automatron action plugins are designed to be as simple as possible to allow users to use their existing scripts along with Automatron's automated action execution. Aside from appropriate exit code usage there is no coding required to use an existing script or utility.
