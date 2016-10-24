#!/usr/bin/env bash

usage() {
  echo 'Usage: '`basename $0` '-i <host> [-t <timeout>]'
  exit 1
}

timeout=3 #Default value

# Parse command line arguments
while getopts ":i:t:" opts
do
  case $opts in
    i)
      host=${OPTARG}
      ;;
    t)
      timeout=${OPTARG}
      ;;
    *)
      echo "Unknown argument:" ${OPTARG}
      usage
      ;;
  esac
done

if [ -z $host ]
then
  usage
fi

ping $host -c 1 -w $timeout 2>&1 > /dev/null
if [ $? -eq 0 ]
then
  alert="OK"
  status="UP"
  exit=0
else
  alert="CRITICAL"
  status="DOWN"
  exit=2
fi

echo "PING $alert $status"
exit $exit
