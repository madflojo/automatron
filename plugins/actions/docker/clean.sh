#!/bin/bash
## Action for Automatron to remove all running containers and images

echo "Cleaning running containers"
echo "-------------------------------"
for CONTAINER in `/usr/bin/docker ps -qa`
do
  /usr/bin/docker rm --force $CONTAINER
done
echo "-------------------------------"
echo "Done"


echo "-------------------------------"


echo "Cleaning docker images"
echo "-------------------------------"
for IMAGE in `/usr/bin/docker images -q`
do
  /usr/bin/docker rmi --force $IMAGE
done
echo "-------------------------------"
echo "Done"
