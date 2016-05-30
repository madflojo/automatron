#!/usr/bin/python
## Basic memory free health check for Automatron


import argparse
import sys
import os
import subprocess

def get_linux_freemem():
    ''' Grab memory stats for Linux systems '''
    memstats = {}
    with open("/proc/meminfo", "r") as fh:
        for entry in fh.readlines():
            key, value = entry.split(":")
            value = value.split()[0]
            memstats[key] = float(value)
    if "MemAvailable" in memstats:
        return (memstats['MemAvailable'] / memstats['MemTotal']) * 100.00
    else:
        ## Linux Free Memory Calculation
        return ((memstats['MemFree'] + memstats['Buffers'] + memstats['Cached']) /
                memstats['MemTotal']) * 100

def get_freebsd_freemem():
    ''' Grab memory stats for FreeBSD systems '''
    memstats = {}
    results = None
    cmd = "sysctl vm.stats.vm.v_free_count vm.stats.vm.v_page_size vm.stats.vm.v_page_count"
    try:
        results = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print "MEM_FREE UNKNOWN Error pulling sysctl information {0}".format(e.message)
        sys.exit("3")
    if results:
        for line in results.splitlines():
            key, value = line.split(":")
            value = value.split()[0]
            memstats[key] = float(value)
        free_mem = memstats['vm.stats.vm.v_free_count'] * \
                   memstats['vm.stats.vm.v_page_size']
        total_mem = memstats['vm.stats.vm.v_page_count'] * \
                    memstats['vm.stats.vm.v_page_size']
        return free_mem / total_mem * 100
    else:
        print "MEM_FREE UNKNOWN Error pulling sysctl information"
        sys.exit("3")

if __name__ == "__main__":
    # Parse cmdline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--warn", type=float,
        help="Warn if Free Memory is less than N percent", required=True)
    parser.add_argument(
        "-c", "--critical", type=float,
        help="Critical if Free Memory is less than N percent", required=True)
    args = parser.parse_args()

    memfree = 100.0
    if "Linux" in os.uname():
        memfree = get_linux_freemem()
    elif "FreeBSD" in os.uname():
        memfree = get_freebsd_freemem()

    alert = 'OK'
    exit_code = 0
    if memfree <= args.warn:
        alert = "WARNING"
        exit_code = 1
    if memfree <= args.critical:
        alert = "CRITICAL"
        exit_code = 2

    print "MEM_FREE {0} {1}".format(alert, memfree)
    sys.exit(exit_code)
