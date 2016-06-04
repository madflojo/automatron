#!/usr/bin/env python
## Perform a specified action using systemctl or service command
## Supports both systemctl and non-systemctl Linux environments

import subprocess
import argparse
import os
import sys

def run_systemctl(service, action):
    ''' Run the systemctl command '''
    cmd = "/usr/bin/systemctl {0} {1}.service".format(action, service)
    return subprocess.call(cmd, shell=True)

def run_service(service, action):
    ''' Run the service command '''
    cmd = "/usr/bin/service {0} {1}".format(service, action)
    return subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    # Parse cmdline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--service",
        help="Service to perform the specified action against", required=True)
    parser.add_argument(
        "-a", "--action",
        help="Action to perform against the specified service", required=True)
    args = parser.parse_args()

    returncode = None
    if os.path.isfile("/usr/bin/systemctl"):
        returncode = run_systemctl(args.service, args.action)
    elif os.path.isfile("/usr/bin/service"):
        returncode = run_service(args.service, args.action)

    if returncode:
        sys.exit(returncode)
    else:
        sys.exit(3)
