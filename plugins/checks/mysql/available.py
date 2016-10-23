#!/usr/bin/env python

import pymysql
import sys
import argparse

def get_status(args):
    ''' Pull the status values from MySQL '''
    status = {}
    try:
        db = pymysql.connect(
            host=args.host,
            user=args.user,
            password=args.password,
            cursorclass=pymysql.cursors.DictCursor)
    except: #pylint disable=broad-except
        return False

    try:
        with db.cursor() as cursor:
            # Get Status
            cursor.execute("show status")
            for result in cursor.fetchall():
                try:
                    status[result['Variable_name']] = int(result['Value'])
                except: #pylint disable=broad-except
                    pass
    finally:
        db.close()

    if "Uptime" in status.keys():
        return status['Uptime']
    else:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--host",
        help="MySQL Host", required=True)
    parser.add_argument(
        "-u", "--user",
        help="MySQL User", required=True)
    parser.add_argument(
        "-p", "--password",
        help="MySQL User Password", required=True)
    args = parser.parse_args()


    if get_status(args):
        alert = "OK"
        status = "UP"
        exit_code = 0
    else:
        alert = "CRITICAL"
        status = "DOWN"
        exit_code = 2

    print "MYSQL_AVAILABLE {0} {1}".format(alert, status)
    sys.exit(exit_code)
