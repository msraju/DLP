import os
import re
import sys
import logging
from typing import List, Tuple

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PIIScanner:
    def __init__(self, target_directory: str):
        self.target_dir = target_directory
        # Compile patterns once
        self.patterns = {
            'SSN': re.compile(r'\b(?!000|666|9\d{2})[0-9]{3}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b'),
            'Email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'CreditCard': re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b')
        }
    
    def luhn_verify(self, cc_number: str) -> bool:
        """Simple Luhn Algorithm verify to reduce false positives on Credit Cards"""
        digits = [int(d) for d in cc_number]
        checksum = 0
        reverse_digits = digits[::-1]
        for i, digit in enumerate(reverse_digits):
            if i % 2 == 1:
                doubled = digit * 2
                checksum += doubled - 9 if doubled > 9 else doubled
            else:
                checksum += digit
        return checksum % 10 == 0

    def scan_file(self, file_path: str) -> List[str]:
        findings = []
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                
                for p_name, p_regex in self.patterns.items():
                    matches = p_regex.findall(content)
                    for match in matches:
                        # Extra validation
                        if p_name == 'CreditCard':
                            if not self.luhn_verify(match):
                                continue # Skip false positive
                        
                        # Redact output for safety
                        redacted = match[:2] + '*' * (len(match)-4) + match[-2:] if len(match) > 4 else "****"
                        findings.append(f"Found {p_name}: {redacted}")
                        
        except Exception as e:
            logging.error(f"Could not read {file_path}: {e}")
            
        return findings

    def run(self):
        logging.info(f"Starting scan on: {self.target_dir}")
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                full_path = os.path.join(root, file)
                # Skip self
                if file == os.path.basename(__file__): continue
                
                results = self.scan_file(full_path)
                if results:
                    logging.warning(f"File: {full_path}")
                    for res in results:
                        print(f"  - {res}")
        logging.info("Scan Complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pii_scanner.py <directory_to_scan>")
        sys.exit(1)
        
    scanner = PIIScanner(sys.argv[1])
    scanner.run()
