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
                    status[result['Variable_name'].lower()] = int(result['Value'])
                except: #pylint disable=broad-except
                    pass
    finally:
        db.close()

    return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-w", "--warn", type=float,
        help="Warning threshold value", required=True)
    parser.add_argument(
        "-c", "--critical", type=float,
        help="Critical threshold value", required=True)
    parser.add_argument(
        "-m", "--metric",
        help="Metric to validate (i.e. slow-queries)", required=True)
    parser.add_argument(
        "-s", "--host",
        help="MySQL Host", required=True)
    parser.add_argument(
        "-u", "--user",
        help="MySQL User", required=True)
    parser.add_argument(
        "-p", "--password",
        help="MySQL User Password", required=True)
    parser.add_argument(
        "-t", "--type",
        help="Alert if metric's value is greater or lesser than thresholds",
        choices=('greater', 'lesser'),
        required=True)
    args = parser.parse_args()
    metric = args.metric.lower()


    # Get status
    status = get_status(args)
    alert = "OK"
    exit_code = 0

    if status and metric in status.keys():
        if args.type == "greater":
            if args.warn < status[metric]:
                alert = "WARNING"
                exit_code = 1
            if args.critical < status[metric]:
                alert = "CRITICAL"
                exit_code = 2
        else:
            if args.warn > status[metric]:
                alert = "WARNING"
                exit_code = 1
            if args.critical > status[metric]:
                alert = "CRITICAL"
                exit_code = 2
    else:
        print "Could not pull stats from MySQL"
        sys.exit(3)

    print "MYSQL_STATUS_HEALTH {0} {1} {2}".format(alert, metric, status[metric])
    sys.exit(exit_code)
