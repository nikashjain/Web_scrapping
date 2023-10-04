#!/bin/bash

# Check if a branch name is provided as a command-line argument
if [ $# -eq 1 ]; then
  branch_to_skip="$1"
fi

# Navigate to the project directory
# cd path/to/project

# Fetch all branches from the remote repository
git remote update
git fetch --all

# Iterate over all branches
for branch in $(git branch -r | grep -v HEAD); do
  # Remove the remote prefix
  local_branch=$(echo $branch | sed 's|origin/||')
  
  # Check if the current branch matches the branch to skip
  if [ "$local_branch" != "$branch_to_skip" ]; then
    # Check out the local branch
    git checkout $local_branch
    # Hard reset the branch to its origin
    git reset --hard origin/$local_branch
  fi
done

# Check out the default branch
git checkout main