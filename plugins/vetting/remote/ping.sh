#!/usr/bin/env bash
## Ping server then return true or false JSON

if [ -z $1 ]
then
    exit 1
fi

/bin/ping -c 1 $1 > /dev/null 2>&1
if [ $? -eq 0 ]
then
    echo '{"ping": true}'
else
    echo '{"ping": false}'
fi
