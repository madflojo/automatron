#!/usr/bin/env python
'''
Automatron: Fact Finder

Identify facts about a specified host

  * Hostname
  * Networking

'''


import os
import json
import subprocess

def get_linux_networking():
    ''' Gather linux networking information '''
    interfaces = []
    if os.path.isdir("/sys/class/net/"):
        interfaces = os.listdir("/sys/class/net/")
    network_info = {}
    for interface in interfaces:
        network_info[interface] = { 'v4' : [], 'v6' : [] }
        results = subprocess.Popen("ip addr show {0}".format(interface), shell=True, stdout=subprocess.PIPE)
        for line in results.stdout.readlines():
            if "inet" in line:
                line_data = line.split()
                ip = line_data[1].split("/")[0]
                if line_data[0] == "inet6":
                    network_info[interface]['v6'].append(ip)
                elif line_data[0] == "inet":
                    network_info[interface]['v4'].append(ip)
    return network_info



if __name__ == "__main__":
    # pylint: disable=C0103
    system_info = {}


    # Add information from uname
    system_info.update({
        'hostname' : os.uname()[1],
        'os' : os.uname()[0],
        'kernel' : os.uname()[2],
    })

    if "Linux" in system_info['os']:
        system_info.update({
            'network' : get_linux_networking()
        })

    print json.dumps(system_info)
