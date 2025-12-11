import os
import re
import sys
import logging
import concurrent.futures
from typing import List

# Configuring robust logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)

class EnterprisePIIScanner:
    def __init__(self, target_directory: str):
        self.target_dir = target_directory
        self.patterns = {
            # Standard SSN
            'SSN': re.compile(r'\b(?!000|666|9\d{2})[0-9]{3}-(?!00)[0-9]{2}-(?!0000)[0-9]{4}\b'),
            # Email Address
            'Email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            # Credit Card (Visa/Mastercard/Amex/Discover)
            'CreditCard': re.compile(r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b'),
            # AWS Access Key (High Entropy)
            'AWS_Key': re.compile(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])')
        }
    
    def luhn_verify(self, cc_number: str) -> bool:
        """Validates credit card numbers using Luhn checksum."""
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

    def scan_file_content(self, file_path: str) -> List[str]:
        findings = []
        try:
            # Check file size (Skip > 50MB to mimic DLP timeout)
            if os.path.getsize(file_path) > 50 * 1024 * 1024:
                return [f"Skipped {file_path} (Too Large)"]

            with open(file_path, 'r', errors='ignore', encoding='utf-8') as f:
                content = f.read()
                
                for p_name, p_regex in self.patterns.items():
                    matches = set(p_regex.findall(content)) # set for unique matches
                    for match in matches:
                        # Validation Logic
                        if p_name == 'CreditCard' and not self.luhn_verify(match):
                            continue # Skip bad Luhn
                        
                        if p_name == 'AWS_Key' and not match.startswith('AKIA'):
                            continue # Simple heuristic to reduce noise

                        # Masking data for log safety
                        masked = match[:4] + "***" + match[-2:] if len(match) > 6 else "***"
                        findings.append(f"[{p_name}] Found match: {masked}")
                        
        except Exception as e:
            logging.debug(f"Read Match Error {file_path}: {e}")
            
        return findings

    def run(self):
        logging.info(f"Initiating multi-threaded scan on: {self.target_dir}")
        all_files = []
        for root, _, files in os.walk(self.target_dir):
            for file in files:
                all_files.append(os.path.join(root, file))
        
        # Parallel Execution
        threat_detected = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self.scan_file_content, f): f for f in all_files}
            for future in concurrent.futures.as_completed(future_to_file):
                f_path = future_to_file[future]
                try:
                    results = future.result()
                    if results:
                        threat_detected = True
                        print(f"\n[!] ALERT: Sensitive Data in {f_path}")
                        for res in results:
                            print(f"    -> {res}")
                except Exception as exc:
                    logging.error(f"{f_path} generated an exception: {exc}")

        if not threat_detected:
            logging.info("Clean Scan: No PII detected.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pii_scanner.py <path>")
        sys.exit(1)
        
    scanner = EnterprisePIIScanner(sys.argv[1])
    scanner.run()
