#!/usr/bin/env python
'''
Automatron: Service Facts

Identify facts about services running on a specified host

OS Support for:
    * Linux (services or systemd only)

'''


import os
import json
import subprocess
import re

def get_linux_service_services():
    ''' Gather linux services information '''
    services = {}
    results = subprocess.Popen("/usr/bin/service --status-all", shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for readme in [results.stdout, results.stderr]:
        for line in readme.readlines():
            service = line.split(" ")[5].rstrip("\n")
            try:
                status = subprocess.call("service %s status" % (service),
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if status == 0:
                    services[service] = "running"
                else:
                    services[service] = "stopped"
            except Exception:
                services[service] = "unknown"
    return services

def get_linux_systemd_services():
    ''' Gather linux services information '''
    services = {}
    results = subprocess.Popen("/usr/bin/systemctl --type service --all --no-pager", shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for readme in [results.stdout, results.stderr]:
        for line in readme.readlines():
            if ".service" in line:
                data = re.split(r'[ ]+', line)
                service_cleanup = data[0].split(".")
                service = ".".join(service_cleanup[:-1])
                status = data[3]
                services[service] = status
    return services


if __name__ == "__main__":
    # pylint: disable=C0103
    services = {}

    if "Linux" in os.uname()[0]:
        if os.path.isfile("/usr/bin/service"):
            services.update(get_linux_service_services())
        elif os.path.isfile("/usr/bin/systemctl"):
            services.update(get_linux_systemd_services())

    output = {'services' : services}
    print json.dumps(output)
