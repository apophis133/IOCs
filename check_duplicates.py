import os
from collections import defaultdict

def find_duplicates():
    hashes = defaultdict(list)
    for root, _, files in os.walk("IOCs"):
        for file in files:
            if file.endswith("_iocs.txt"):
                family = os.path.basename(root)
                with open(os.path.join(root, file), 'r') as f:
                    for line in f:
                        h = line.strip().lower()
                        if h:
                            hashes[h].append(family)
    return {h: families for h, families in hashes.items() if len(families) > 1}

if __name__ == "__main__":
    duplicates = find_duplicates()
    if duplicates:
        print("ERROR: Duplicate hashes found!")
        for h, families in duplicates.items():
            print(f"SHA256 {h} found in families: {', '.join(families)}")
        exit(1)
    print("No duplicates found.")
    exit(0)