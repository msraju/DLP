import hashlib
import csv
import sys
import os

# usage: python fingerprint_gen.py employee_database.csv
# This script mimics how Enterprise DLP tools (Symantec/Forcepoint) create
# Exact Data Match (EDM) profiles. We strictly hash the data; we never store plain text.

def generate_edm_profile(input_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"[*] Loading structured data from {input_file}...")
    
    # We will accept a CSV where columns 0, 1, 2 might be (First, Last, SSN)
    # A "Match" usually requires matching 2 out of 3 columns in the same row.
    
    hashes = []
    
    try:
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            
            row_count = 0
            for row in reader:
                if len(row) < 2: continue
                
                # Create a "Row Hash" that represents the combination of data
                # In real DLP, we hash individual cells, but index them by row.
                # Here we simulate an indexed hash set.
                row_str = "".join(row)
                row_hash = hashlib.sha256(row_str.encode('utf-8')).hexdigest()
                
                hashes.append(row_hash)
                row_count += 1
                
        print(f"[*] Processed {row_count} records.")
        print("[*] Generating Hash Index...")
        
        # Save the index
        output_file = input_file + ".edm"
        with open(output_file, 'w') as out:
            for h in hashes:
                out.write(h + "\n")
                
        print(f"[+] EDM Profile saved to {output_file}")
        print("    (This file can now be safely pushed to the DLP Enforcer)")

    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    print("--- Exact Data Match (EDM) Generator ---")
    if len(sys.argv) < 2:
        print("Usage: python fingerprint_gen.py <csv_file>")
    else:
        generate_edm_profile(sys.argv[1])
