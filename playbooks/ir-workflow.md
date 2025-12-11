# DLP Incident Response Standard Operating Procedure (SOP)

## Workflow Overview
This document outlines the standard process for handling DLP alerts triggered by the Symantec/Forcepoint/McAfee/Oracle Security stack.

```mermaid
graph TD
    A[Alert Triggered] --> B{Severity Level?}
    B -- Low/Info --> C[Log for Analytics]
    B -- High/Critical --> D[Assign to Analyst]
    D --> E{True Positive?}
    E -- No --> F[Close as False Positive & Tune Policy]
    E -- Yes --> G[Determine Intent]
    G -- Accidental --> H[User Coaching/Notification]
    G -- Malicious --> I[Escalate to SOC/HR/Legal]
    I --> J[Containment (Disable Account/Revoke Access)]
    H --> K[Close Incident]
    J --> K
```

## Phase 1: Triage (Analyst Tier 1)
1.  **Validate content:** Review the matched data snippet. Is it actual PII/Source Code?
2.  **Context Check:**
    *   **Who:** Is the user authorized? (e.g., HR sending payroll data *is* normal).
    *   **Where:** Destination URL/Email. Is it a known partner domain?
    *   **How much:** Volume analysis. 1 record vs 10,000 records.

## Phase 2: Investigation (Analyst Tier 2)
*   **Cross-Reference:** Check logs in SIEM. Did the user recently download this data?
*   **Behavioral Analysis:** any other recent alerts? (e.g., "Resume upload", "Job search keywords").
*   **Asset Lookups:** Is the device compliant?

## Phase 3: Containment & Remediation
*   **Accidental:** Send automated email template: *"Hi, you recently violated policy X. Please use the authorized Secure Transfer Portal."*
*   **Malicious:**
    1.  Capture Evidence (Screenshots, PCAP).
    2.  Isolate Endpoint (Network Quarantine).
    3.  Engage Legal/HR for disciplinary action.

## Phase 4: Feedback Loop
*   Update Regex if false positive.
*   Update Allow-lists (White-listing) for new business partners.
