#!/bin/bash

# Pull latest changes first
cd ~/github_repos/iocs
git pull origin main

# Prompt for family name
read -p "Enter threat family name: " family_name
family_lower=$(echo "$family_name" | tr '[:upper:]' '[:lower:]')

# Create directory structure
mkdir -p "iocs/$family_lower"
touch "iocs/$family_lower/${family_lower}_iocs.txt"

# Process cleaned hashes
python add_ioc.py "$family_lower" "$(cat /c/Users/PC/github_repos/hashes.txt)"

# Verify and commit
python check_duplicates.py
git add .
git commit -m "Add $family_name IOCs ($(wc -l < /c/Users/PC/github_repos/hashes.txt) hashes)"

# Push changes
git pull origin main  # Reintegrate any remote changes
git push origin main
echo "Successfully added $(wc -l < /c/Users/PC/github_repos/hashes.txt) IOCs"