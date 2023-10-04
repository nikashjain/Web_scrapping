#!/bin/bash

# Function to delete __pycache__ folders
delete_pycache() {
    local dir="$1"
    for d in "$dir"/*; do
        if [ -d "$d" ]; then
            if [ "$(basename "$d")" = "__pycache__" ]; then
                echo "Deleting $d"
                rm -rf "$d"
            else
                delete_pycache "$d"
            fi
        fi
    done
}



target_directory=$PWD

if [ -d "$target_directory" ]; then
    delete_pycache "$target_directory"
    echo "Cleanup completed."
else
    echo "Directory not found."
fi
