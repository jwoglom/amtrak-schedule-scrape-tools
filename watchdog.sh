#!/bin/bash

# give time for scraping to start
sleep 1000

while true; do

# Find files in the folder that were created within the past hour
recent_files=$(find "data/" -type f -mmin -60)

# Check if there are any recent files
if [ -n "$recent_files" ]
then
    echo "There are files in the folder that were created within the past hour:"
    echo "$recent_files"
else
    echo "There are no files in the folder that were created within the past hour."
    echo "Restarting container"
    docker container restart amtrak
fi

sleep 600
done
