import os
import sys
import re

def is_valid_sha256(h):
    return re.match(r'^[a-f0-9]{64}$', h.lower()) is not None

def find_ioc_file(family_dir):
    for f in os.listdir(family_dir):
        if f.lower().endswith('_iocs.txt'):
            return os.path.join(family_dir, f)
    return None

def hash_exists(hash_to_check):
    hash_to_check = hash_to_check.lower()
    for root, _, files in os.walk("IOCs"):
        for file in files:
            if file.lower().endswith('_iocs.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    existing_hashes = {line.strip().lower() for line in f}
                    if hash_to_check in existing_hashes:
                        return os.path.basename(root)
    return None

def add_hashes(family, hashes):
    family_dir = os.path.join("IOCs", family)
    os.makedirs(family_dir, exist_ok=True)
    ioc_file = find_ioc_file(family_dir) or os.path.join(family_dir, f"{family.lower()}_iocs.txt")
    
    duplicates = []
    new_hashes = []
    
    for h in hashes:
        h = h.lower()
        if not is_valid_sha256(h):
            print(f"Invalid SHA256 skipped: {h}")
            continue
            
        if hash_exists(h):
            duplicates.append(h)
            continue
            
        new_hashes.append(h)
    
    if new_hashes:
        with open(ioc_file, 'a') as f:
            f.write('\n'.join(new_hashes) + '\n')
    
    return new_hashes, duplicates

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_ioc.py <family> <hash1> <hash2> ...")
        exit(1)
    
    family = sys.argv[1]
    hashes = sys.argv[2:]
    
    added, duplicates = add_hashes(family, hashes)
    
    if duplicates:
        print(f"\nWarning: {len(duplicates)} duplicates skipped:")
        print('\n'.join(duplicates[:5]))  # Show first 5 to avoid flooding
        if len(duplicates) > 5:
            print(f"...and {len(duplicates)-5} more")
    
    if added:
        print(f"\nSuccess: Added {len(added)} hashes to {family}:")
        print('\n'.join(added[:3]))  # Show first 3
        if len(added) > 3:
            print(f"...and {len(added)-3} more")
    else:
        print("No valid new hashes added")