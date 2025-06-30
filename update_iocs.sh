#!/bin/bash

# Step 0: Prompt for family name
read -p "Enter threat family name: " family_name

# Step 1: Create directory structure
cd ~/github_repos/iocs/iocs
mkdir -p "${family_name,,}"  # Convert to lowercase
touch "${family_name,,}/${family_name,,}_iocs.txt"
echo "Created directory and IOC file for ${family_name}"

# Step 2: Add IOCs from hashes
cd ~/github_repos/iocs
python add_ioc.py "${family_name,,}" "$(cat /c/Users/PC/github_repos/hashes.txt)"
echo "Added IOCs from hashes.txt"

# Step 3: Check for duplicates
python check_duplicates.py

# Step 4: Commit changes
git add .
git commit -m "Add ${family_name} IOCs"
git push origin main
echo "Changes committed and pushed to repository"