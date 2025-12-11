# Incident Scenario: Insider Threat (Departing Employee)

**Scenario:** Employee gives 2 weeks notice. 3 days prior to departure, Endpoint DLP triggers on mass-copy to USB and upload to "personal-cloud.com".

## 1. Initial Detection
*   **Alert:** "High Volume Transfer - USB" & "Web Upload - Uncategorized Storage".
*   **Volume:** 4.5 GB of data.
*   **User Status:** "Terminating" (Flagged in HR Feed).

## 2. Investigation Steps
1.  **Verify Separation Status:** Confirm with HR that user is leaving.
2.  **File Analysis:**
    *   Review Shadow Copy of transferred files.
    *   *Finding:* Files matched "Proprietary Source Code" and "Customer Database".
3.  **Timeline Reconstruction:**
    *   10:00 AM: User plugged in USB "Kingston16GB".
    *   10:05 AM: Copied `Project_Omega_Source.zip`.
    *   10:15 AM: Uploaded `Contacts.xlsx` to Google Drive (Personal).

## 3. Response Actions
*   **Immediate:**
    *   Block USB write access via MDM/DLP Console.
    *   Reset Active Directory Password.
    *   Revoke VPN and SaaS (Salesforce/GitHub) access.
*   **Escalation:**
    *   Notify CISO and Legal Counsel.
    *   Notify HR Manager.

## 4. Post-Incident Forensic
*   Seize laptop for forensic imagining.
*   Interview user (conducted by HR/Legal) regarding the intent.
*   **Outcome:** Data recovered. User signed affidavit of deletion. Warning issued.
