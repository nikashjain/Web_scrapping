#!/bin/bash

log_directory="$PWD/logs"
deleted_count=0

# Check if the directory exists
if [ ! -d "$log_directory" ]; then
    echo "Directory does not exist: $log_directory"
    exit 1
fi

# Loop through all files in the directory
for log_file in "$log_directory"/*; do
    if [ -f "$log_file" ]; then
        # Check if the file is empty
        if [ ! -s "$log_file" ]; then
            echo "Deleting empty log file: $log_file"
            rm -f "$log_file"
            deleted_count=$((deleted_count + 1))
        else
            echo "Log file is not empty: $log_file"
        fi
    fi
done

echo "Cleanup completed. Deleted $deleted_count empty files."
