#!/bin/bash

# A simple log analyzer to grep for specific DLP keywords in log files
# Usage: ./log_analyzer.sh <log_file>

LOG_FILE=$1

if [ -z "$LOG_FILE" ]; then
    echo "Usage: $0 <log_file>"
    exit 1
fi

echo "=== DLP Incident Log Analysis Report ==="
echo "Target: $LOG_FILE"
echo "Date: $(date)"
echo "----------------------------------------"

# 1. Count occurrences of "BLOCK" actions
BLOCK_COUNT=$(grep -c "Action:Block" "$LOG_FILE")
echo "[+] Total Blocked Transactions: $BLOCK_COUNT"

# 2. Extract Top 5 Users violating policy
echo "[+] Top 5 High-Risk Users:"
grep "Action:Block" "$LOG_FILE" | awk -F "User:" '{print $2}' | awk '{print $1}' | sort | uniq -c | sort -nr | head -5

# 3. Check for specific sensitive keywords (case insensitive)
echo "[+] Keyword Trigger Checks:"
KEYWORDS=("Confidential" "Proprietary" "SSN" "Credit Card")
for KW in "${KEYWORDS[@]}"; do
    COUNT=$(grep -i -c "$KW" "$LOG_FILE")
    echo "  - '$KW': $COUNT events"
done

echo "----------------------------------------"
echo "Analysis Complete."
