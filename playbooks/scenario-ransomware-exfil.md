# Scenario: Double Extortion Ransomware Exfiltration

## The Threat
Modern ransomware gangs (e.g., LockBit, Cl0p) do not just encrypt data; they **exfiltrate** it first to threaten public release. DLP is the *only* control that can detect this pre-encryption phase.

## 1. Detection Signals (Pre-Encryption)
*   **Alert:** "Massive Upload to Unknown IP" via Network DLP.
*   **Indicator:** 50GB+ outbound traffic via FTP/SFTP/Mega.nz.
*   **Time:** Often occurs at 2:00 AM - 4:00 AM (local time).
*   **User Account:** Service Accounts or Compromised Admin credentials.

## 2. Immediate Response (The "Golden Hour")
**Goal:** We must sever the connection *before* the upload completes.

1.  **Block at Perimeter:**
    *   Command Firewall/Proxy to blackhole the destination IP immediately.
2.  **Kill Process:**
    *   Identify the tool used (e.g., `rclone`, `filezilla`, `powershell`).
    *   Terminate process on the endpoint via EDR.
3.  **Isolate Host:**
    *   The machine is compromised. Move to a restricted VLAN.

## 3. Investigation
*   **Lateral Movement Check:**
    *   Did the attacker touch other File Shares?
    *   Check `smb` logs for access to "Finance" or "HR" directories.
*   **Payload Analysis:**
    *   What *exactly* left the building? (This determines the extortion leverage).
    *   Review PCA (Full Packet Capture) if available, or DLP Shadow Copies.

## 4. Remediation
*   Reset all Admin passwords.
*   Reimage affected hosts.
*   **Policy Update:** Block `rclone.exe` and `mega.nz` at the application/DNS level globally.
