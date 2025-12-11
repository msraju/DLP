# Incident Scenario: The "Flight Risk" Insider

## Context
A senior engineer has resigned. The "Exit Period" (2 weeks) is the highest risk window for IP theft. This scenario utilizes behavioral analytics (UEBA).

## 1. Behavioral Triggers (UEBA)
Instead of a single "Block", we look for a sequence of anomalies:
1.  **Preparation:** User accesses `Old_Projects` folders they haven't touched in 6 months.
2.  **Aggregation:** User creates a ZIP file named `Backup.zip` (5GB).
3.  **Exfiltration Attempt:**
    *   Tries USB (Blocked).
    *   Waits 10 minutes.
    *   Tries AirDrop (Blocked).
    *   Waits 10 minutes.
    *   Tries `weconfirm.com` (Allowed by default config? -> **Breach**).

## 2. Advanced Investigation
*   **Shadow IT Discovery:**
    *   If they used `weconfirm.com`, check DNS logs. Is this a net-new domain?
*   **Steganography Check:**
    *   Did they upload large `.jpg` files? (Could be code embedded in images).
    *   *Action:* Run entropy analysis on the images.

## 3. Forensic Artifacts
To prove "Malicious Intent" vs "Taking Personal Photos":
*   **Shellbags (Windows):** Proves they navigated to specific folders.
*   **LNK Files:** Proves they opened the files.
*   **Shimcache:** Proves they ran execution tools like `rar.exe` or `7zip.exe`.

## 4. Legal Hold
*   Immediately image the laptop.
*   Do *not* wipe the machine for re-issue until Legal signs off.
