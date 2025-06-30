#!/bin/bash

# Step 0: Prompt for family name
read -p "Enter threat family name: " family_name

# Step 0.5: Update local repo first
cd ~/github_repos/iocs
git pull origin main

# Step 1: Create directory structure
cd iocs
mkdir -p "${family_name,,}"
touch "${family_name,,}/${family_name,,}_iocs.txt"

# Step 2: Add IOCs
cd ..
python add_ioc.py "${family_name,,}" "$(cat /c/Users/PC/github_repos/hashes.txt)"

# Step 3: Check duplicates
python check_duplicates.py

# Step 4: Commit and push with retry
git add .
git commit -m "Add ${family_name} IOCs"
git pull origin main  # Reintegrate remote changes
git push origin main