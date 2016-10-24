#!/usr/bin/env python

import socket
import argparse
import sys

def check_connection(args):
    ''' Open TCP Connection and Return if successful '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(args.timeout)
    try:
        return not bool(s.connect_ex((args.host, args.port)))
    except socket.error:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--host",
        help="IP or Host Address", required=True)
    parser.add_argument(
        "-p", "--port",
        help="Port",
        type=int,
        required=True)
    parser.add_argument(
        "-t", "--timeout",
        help="Timeout in seconds",
        type=int,
        required=False,
        default=5
    )
    args = parser.parse_args()

    if check_connection(args):
        alert = "OK"
        status = "UP"
        exit_code = 0
    else:
        alert = "CRITICAL"
        status = "DOWN"
        exit_code = 2

    print "TCP_CONNECT {0} {1}".format(alert, status)
    sys.exit(exit_code)
