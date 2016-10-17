#!/usr/bin/env python
## Check for disks space used
## Currently support Linux

import subprocess
import sys
import argparse
import os

def disk_free_linux(filesystem):
    ''' Grab filesystem usage '''
    result = None
    cmd = "df -h {0}".format(filesystem)
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print "DISK_FREE UNKNOWN Error pulling disk information {0}".format(e.message)
        sys.exit("3")
    if result:
        line = result.splitlines()[1]
        usage = line.split()[4]
        value = usage.rstrip("%")
        return 100 - int(value)
    else:
        print "DISK_FREE UNKNOWN Error pulling disk information {0}".format(e.message)
        sys.exit("3")

if __name__ == "__main__":
    # Parse cmdline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--warn", type=float,
        help="Warn if Free Disk Space is less than N percent", required=True)
    parser.add_argument(
        "-c", "--critical", type=float,
        help="Critical if Free Disk Space is less than N percent", required=True)
    parser.add_argument(
        "-f", "--filesystem",
        help="Filesystem to check", required=True)
    args = parser.parse_args()

    diskfree = 100
    if "Linux" in os.uname():
        diskfree = disk_free_linux(args.filesystem)

    alert = 'OK'
    exit_code = 0
    if diskfree <= args.warn:
        alert = "WARNING"
        exit_code = 1
    if diskfree <= args.critical:
        alert = "CRITICAL"
        exit_code = 2

    print "DISK_FREE {0} {1}".format(alert, diskfree)
    sys.exit(exit_code)
